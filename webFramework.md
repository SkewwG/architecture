# webFramework
web框架：为我们设计了技术流程，运用控制反转编程技术，来让使用者必须遵循某种流程。

控制反转即框架控制着整个流程，本来之前的程序都是程序员控制输入输出，此时被框架控制。

控制反转（IoC ）：框架对程序员说：不要调用我，我会调用你

自己编写一个简易的webFramework

**核心功能：**

* 核心之一：与web server对接

* 核心之二：根据web server传递过来的环境变量等等参数处理请求

* 核心之三：路由机制

* 核心之四：错误处理 try...except...

**扩充：**

* 1、http无状态，所以添加session、cookies

* 2、template

* 3、cache

* 4、security


## 核心之一：与web server对接
``` python
# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from skeFramework import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
```

## 核心之二：根据web server传递过来的环境变量等等参数处理请求

定义一个Application方法处理server传递过来的环境变量
``` python
# skeFramework.py

def application(environ, start_response):
    status = '200 OK'       # 状态码
    response_headers = [('Content-Type', 'text/html')]      # 响应头
    start_response(status, response_headers)
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')          # 返回内容
    return [body.encode('utf-8')]
```


如果我想处理多个url，将application封装成一个class比function更好。
``` python
# skeFramework.py

class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        status = '200 OK'       # 状态码
        response_headers = [('Content-Type', 'text/html')]      # 响应头
        self.start_response(status, response_headers)
        body = '<h1>Hello, %s!</h1>' % (self.environ['PATH_INFO'][1:] or 'web')          # 返回内容
        yield body.encode('utf-8')
```

此处封装的类用了迭代 `__iter__ `，下面简单介绍 `__iter__ `.demo如下：↓
``` python
class A:
    def __init__(self, num):
        self.num = num
        self.i = 0

    def __iter__(self):
        return self             # 返回迭代器对象本身

    def __next__(self):
        if self.i >= self.num:
            raise StopIteration
        else:
            self.i += 1
            return self.i       # 返回迭代器的下一个元素

for i in A(6):  # 程序先运行__iter__返回迭代器对象本身， 然后运行__next__，当值大于长度进来的数字时，程序中断。
    print(i)
```

## 核心之三：路由机制
将传递过来的url与方法一一对应。

``` python
# skeFramework.py

class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        path = self.environ['PATH_INFO']
        if path == '/':
            return self.GET_index()
        if path == '/hello':
            return self.GET_hello()
        else:
            return self.notfound()

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Hello world!\n".encode('utf-8')

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Not Found\n".encode('utf-8')
```

每一个路径就一个if else语句，代码太长，不好看。用list将url和function对应起来,把这个抽象出来.
``` python
# skeFramework.py

class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.urls = [('/', 'index'), ('/hello', 'hello')]

    def __iter__(self):
        path_info = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for path, name in self.urls:
            if path == path_info:
                funcName = method.upper() + '_' + name
                func = getattr(self, funcName)
                return func()
        return self.notfound()


    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Hello world!\n".encode('utf-8')

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Not Found\n".encode('utf-8')
```

现在是访问`/` `/index`会有对应的方法去处理，其他路径全被notfound()去处理了。如果多个url`/index/1`,`/index/2`,`/index/3`过来，每个url都要定义一个function，明显是不合理的。所以用re正则去解决这个问题。

``` python
# skeFramework.py
import re

class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.urls = [('/', 'index'), ('/hello/(.*)', 'hello')]

    def __iter__(self):
        path_info = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path_info)        # 如果匹配到.
            if m:
                funcName = method.upper() + '_' + name
                func = getattr(self, funcName)
                return func()          # 传递给function
        return self.notfound()


    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Hello!\n".encode('utf-8')

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Not Found\n".encode('utf-8')
```

对`__iter__`近一步优化，设置委托。

``` python
# skeFramework.py
import re

class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.urls = [('/', 'index'), ('/hello/(.*)', 'hello')]

    def __iter__(self):
        return self.delegate()
            
    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
                    
        return self.notfound()

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Hello!\n".encode('utf-8')

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Not Found\n".encode('utf-8')
```

通过之前的讲解，发现有大量的代码和application并没有直接的关系，所以可以把这些代码放到基类里，然后application去继承。
``` python
# skeFramework.py
import re

class wsgiApp:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        return self.delegate()

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()[0]
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)

        return self.notfound()

class application(wsgiApp):
    urls = [('/', 'index'), ('/hello/(.*)', 'hello')]

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self, name):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Hello!\n".encode('utf-8')

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield "Not Found\n".encode('utf-8')
```

此时还有一个问题，function里的很多代码重复了，同样将重复代码放到基类里。状态码存放到基类的init里，比如定义一个_headers列表存放响应头。定义headers方法往_headers列表里存放内容。

重点：`__iter__`方法返回iter(x)，必须让函数返回可迭代的对象，否则服务端会报错！前面的代码之所以不使用iter()是因为get_index()等方法返回的是yield，所以不需要。
``` python
# skeFramework.py
import re

class wsgiApp:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.status = '200 OK'
        self._headers = []

    def __iter__(self):
        x = self.delegate()
        self.start_response(self.status, self._headers)
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def headers(self, name, value):
        self._headers.append((name, value))


    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()[0]
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func()

        return self.notfound()

class application(wsgiApp):
    urls = [('/', 'index'), ('/hello/(.*)', 'hello')]

    def GET_index(self):
        self.headers('Content-type', 'text/plain')
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self):
        self.headers('Content-type', 'text/plain')
        yield "Hello!\n".encode('utf-8')

    def notfound(self):
        self.headers('Content-type', 'text/plain')
        yield "Not Found\n".encode('utf-8')
```

## 核心之四：错误处理 try...except...

如果服务端发生异常，程序该怎么处理呢？根据平时访问的网站发现，如果网站发生错位，会返回5XX状态码回来。那么我们可以用错误处理去实现，只要在__iter__()方法里加入try...except...即可。接下来还有一个问题，当服务端发生错误抛出异常，而我们想要知道哪个文件哪个函数哪一行发生错误，通过导入trackback去实现。

这是trackback的demo：↓
``` python
# format_exc()返回字符串，print_exc()则直接给打印出来。
# 即traceback.print_exc()与print(traceback.format_exc())效果是一样的。
# print_exc()还可以接受file参数直接写入到一个文件。比如: traceback.print_exc(file=open('tb.txt','w+'))
import traceback
import time

print('start')

time.sleep(1)

try:
    1/0
except Exception as e:
    print(traceback.format_exc())

time.sleep(1)

try:
    1/0
except Exception as e:
    traceback.print_exc()

time.sleep(1)

print('end!')
```

现在了解了trackback，那么就往`__iter__()`里加入错误异常处理。
``` python
# skeFramework.py
import re
import traceback

class wsgiApp:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.status = '200 OK'
        self._headers = []

    def __iter__(self):
        try:
            x = self.delegate()
            self.start_response(self.status, self._headers)
        except Exception as e:
            self.headers("Content-Type", "text/plain")
            self.start_response("500 Internal Error", self._headers)
            x = "Internal Error:\n\n" + traceback.format_exc()
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def headers(self, name, value):
        self._headers.append((name, value))


    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()[0]
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func()

        return self.notfound()

class application(wsgiApp):
    urls = [('/', 'index'), ('/hello/(.*)', 'hello')]

    def GET_index(self):
        self.headers('Content-type', 'text/plain')
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self):
        self.headers('Content-type', 'text/plain')
        yield "Hello!\n".encode('utf-8')

    def notfound(self):
        self.headers('Content-type', 'text/plain')
        yield "Not Found\n".encode('utf-8')

```



## 扩充之一：Session和Cookies

WEB应用都很依赖session这一功能，HTTP协议是无状态，每次访问一个资源，就发起一次连接，得倒资源后，就关闭了连接。浏览器和服务器就无法联系了。所以，服务器为了认证浏览器的身份，需要让浏览器携带一个独一无二的信令，其他人无法获取到，也没有办法猜测到，每次浏览器来访问自己的时候都带上这个信令，服务器判断这个信令是不是自己发出的，就可以知道浏览器是谁了。原理这就是这么简单。这个信令就是cookie了。

session的依赖浏览器的cookie。cookie的生命周期是服务器设置的。我们想要的效果是，如果用户关闭浏览器，离开了电脑，别人就不能再启动浏览器，打开之前的页面进入的系统了。

有了Cookie，为什么还需要Session呢？其实很多情况下，只使用Cookie便能完成大部分目的。但是人们发现，只使用Cookie往往是不够的，考虑用户登录信息或一些重要的敏感信息，用Cookie存储的话会带来一些问题，最明显的是由于Cookie会把信息保存到本地，因此信息的安全性可能受到威胁。Session的出现很好地解决的这个问题，Session与Cookie类似，但它们最明显的区别是，Session会将信息保存服务器端，客户端需要一个session_id，它一段随机的字符串，类似身份证的功能，从服务器端中根据这个凭证来获取信息。而这个session_id通常是保存在Cookie中的

当客户端登录成功后，服务端会根据用户的登录信息在Session中生成一个加密的”容器”，名称是一个随机的字符串，在这个”容器”中存储了一些重要的信息，例如：用户名，邮箱等，存储完成后，服务端会将这个字符串传给客户端，客户端会将这个字符串，存储在cookie中，并且每次客户端访问的时候，服务端都会验证这个字符串。

**上面的四段摘自他人博客，个人认为这个解释挺详细的，故摘取下来。**

下面demo把访问的路径hex化，值存到session里，并作为cookies返回。下次访问如果有session值，就会直接去执行GET_Session函数。

``` python
# skeFramework.py
import re
import codecs

class wsgiApp:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.status = '201 OK'
        self._headers = []
        self._cookie = []

    def __iter__(self):
        x = self.delegate()
        self.start_response(self.status, self._headers)
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def headers(self, name, value):
        self._headers.append((name, value))

    def hasSession(self, http_cookie):
        for each in http_cookie.split(';'):
            if 'session' in each:
                return each.split('=')[1]
        return None


    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        http_cookie = self.environ['HTTP_COOKIE']
        session_value = self.hasSession(http_cookie)
        if session_value:
            func = getattr(self, 'GET_Session')
            return func(session_value)

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()[0]
                session = 'session={}'.format(codecs.encode(args.encode('utf-8'), 'hex_codec').decode())
                self.headers('Set-Cookie', session)
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(args)

        return self.notfound()

class application(wsgiApp):
    urls = [('/', 'index'), ('/hello/(.*)', 'hello')]

    def GET_index(self, args):
        self.headers('Content-type', 'text/plain')
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self, args):
        self.headers('Content-type', 'text/plain')
        yield "Hello {}!\n".format(args).encode('utf-8')

    def notfound(self):
        self.headers('Content-type', 'text/plain')
        yield "Not Found\n".encode('utf-8')

    def GET_Session(self, args):
        self.headers('Content-type', 'text/plain')
        value = codecs.decode(args, 'hex_codec').decode('utf-8')
        yield "wow {}, you're here again.\n".format(value).encode('utf-8')
```

结果如图：↓

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_session.png)

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_session2.png)

## 扩充之三：cache缓存机制

如何使用Python实现缓存机制呢？用字典去存放值，定义MyCache类，成员变量cache是字典，存放缓存值，max_cache_size定义缓存值的个数。

`__contain__`实现根据该键是否存在于缓存当中返回True或者False。`update`更新该缓存字典，主要存放两个，一个是存入时间，还有一个就是要存放的内容。`remove_oldest`迭代缓存列表，将最先存入的值删除。

``` python
# -*- coding: utf-8 -*-
import datetime
import codecs

class MyCache:
    def __init__(self):
        self.cache = {}
        self.max_cache_size = 3

    def __contains__(self, key):
        return key in self.cache

    def update(self, key, value):
        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()
        self.cache[key] = {'date_accessed': datetime.datetime.now(),
                           'value': value}

    def remove_oldest(self):
        oldest_entry = None
        for key in self.cache:
            if oldest_entry == None:
                oldest_entry = key
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key
        self.cache.pop(oldest_entry)


if __name__ == '__main__':
    keys = ['test', 'red', 'test',  'fox', 'fence', 'test', 'fence', 'junk', \
            'other', 'alpha', 'bravo', 'cal', 'alpha','devo', 'ele']
    s = 'abcdefghijklmnop'
    cache = MyCache()
    for i, key in enumerate(keys):
        if key in cache:
            print('[{}] [{} -> in cache] -> [cache : {}]\n'.format(i, key, cache.cache))
        else:
            print('[{}] [{} -> not in cache] -> [cache : {}]\n'.format(i, key, cache.cache))
            value = codecs.encode(key.encode('utf-8'), 'hex_codec').decode('utf-8')
            cache.update(key, value)
```

打印结果如下：↓

``` python
[0] [test -> not in cache] -> [cache : {}]

[1] [red -> not in cache] -> [cache : {'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[2] [test -> in cache] -> [cache : {'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[3] [fox -> not in cache] -> [cache : {'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[4] [fence -> not in cache] -> [cache : {'fox': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '666f78'}, 'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[5] [test -> in cache] -> [cache : {'fence': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '66656e6365'}, 'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[6] [fence -> in cache] -> [cache : {'fence': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '66656e6365'}, 'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[7] [junk -> not in cache] -> [cache : {'fence': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '66656e6365'}, 'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[8] [other -> not in cache] -> [cache : {'junk': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6a756e6b'}, 'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[9] [alpha -> not in cache] -> [cache : {'red': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '726564'}, 'other': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6f74686572'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[10] [bravo -> not in cache] -> [cache : {'alpha': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '616c706861'}, 'other': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6f74686572'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[11] [cal -> not in cache] -> [cache : {'bravo': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '627261766f'}, 'other': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6f74686572'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[12] [alpha -> not in cache] -> [cache : {'cal': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '63616c'}, 'other': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6f74686572'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[13] [devo -> not in cache] -> [cache : {'alpha': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '616c706861'}, 'other': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6f74686572'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]

[14] [ele -> not in cache] -> [cache : {'devo': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6465766f'}, 'other': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '6f74686572'}, 'test': {'date_accessed': datetime.datetime(2018, 6, 16, 18, 6, 21, 344344), 'value': '74657374'}}]
```

现在已经知道如何实现缓存机制，那么结合web Framework试试：↓

``` python
# skeFramework.py
import re
import datetime
import codecs

class MyCache:
    def __init__(self):
        self.cache = {}
        self.max_cache_size = 3

    def __contains__(self, key):
        return key in self.cache

    def update(self, key, value):
        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()
        self.cache[key] = {'date_accessed': datetime.datetime.now(),
                           'value': value}

    def remove_oldest(self):
        oldest_entry = None
        for key in self.cache:
            if oldest_entry == None:
                oldest_entry = key
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key
        self.cache.pop(oldest_entry)

cache = MyCache()

class wsgiApp:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.status = '201 OK'
        self._headers = []
        self._cookie = []

    def __iter__(self):
        x = self.delegate()
        self.start_response(self.status, self._headers)
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def headers(self, name, value):
        self._headers.append((name, value))

    def getSession(self, http_cookie):
        for each in http_cookie.split(';'):
            if 'session' in each:
                return each.split('=')[1]
        return None

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        http_cookie = self.environ['HTTP_COOKIE']
        session_value = self.getSession(http_cookie)

        if session_value:
            func = getattr(self, 'Session_Deal')
            return func(session_value)

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()[0]
                if args in cache.cache:
                    func = getattr(self, 'cache_Deal')
                    return func(args)
                else:
                    session = 'session={}'.format(codecs.encode(args.encode('utf-8'), 'hex_codec').decode())
                    cache.update(args, session)
                    self.headers('Set-Cookie', session)
                    funcname = method.upper() + "_" + name
                    func = getattr(self, funcname)
                    return func(args)

        return self.notfound()

class application(wsgiApp):
    urls = [('/', 'index'), ('/hello/(.*)', 'hello')]

    def GET_index(self, args):
        self.headers('Content-type', 'text/plain')
        yield "Welcome!\n".encode('utf-8')

    def GET_hello(self, args):
        self.headers('Content-type', 'text/plain')
        yield "Hello {}!\n".format(args).encode('utf-8')

    def notfound(self):
        self.headers('Content-type', 'text/plain')
        yield "Not Found\n".encode('utf-8')

    # 当带有session时的处理
    def Session_Deal(self, args):
        self.headers('Content-type', 'text/plain')
        value = codecs.decode(args, 'hex_codec').decode('utf-8')
        yield "wow {}, you're here again.\n".format(value).encode('utf-8')

    # 请求内容在缓存中的处理
    def cache_Deal(self, args):
        self.headers('Content-type', 'text/plain')
        # value = codecs.decode(args, 'hex_codec').decode('utf-8')
        yield "wow {}, you're in cache.\n".format(args).encode('utf-8')
```

缓冲机制流程介绍：↓

前三张图片是张三1，张三2，张三3对服务器进行访问，他们的session值都被记录在缓存里。

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_cache1.png)
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_cache2.png)
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_cache3.png)

现在张三1重新访问，发现服务器返回的是wow zhangsan1， you're in cache。说明此时张三1访问服务器时，服务器是在缓存里处理数据

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_cache4.png)

此时张三14访问服务器，服务器的缓存机制会将张三14的session值保存到缓存字典里，把最先存入缓存字典的张三1的值删除掉

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_cache5.png)

最后，当张三1重新访问服务器时，服务器返回的是hello, zhangsan1。说明张三1的值已经从缓存里被删除掉，现在重新处理并重新存入缓存字典里

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/webFramework_cache6.png)



