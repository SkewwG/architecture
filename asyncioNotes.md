# 异步编程

## 1. 概念（http://aju.space/2016/09/20/blocking-nonblocking-sync-async.html）

### 1.1 阻塞

程序在等待某个操作完成期间，自身无法继续干别的事情，则称该程序在该操作上是阻塞的。

常见的阻塞形式有：网络I/O阻塞、磁盘I/O阻塞、用户输入阻塞等。

阻塞是无处不在的，包括CPU切换上下文时，所有的进程都无法真正干事情，它们也会被阻塞。（如果是多核CPU则正在执行上下文切换操作的核不可被利用。）

### 1.2 非阻塞

程序在等待某操作过程中，自身不被阻塞，可以继续运行干别的事情，则称该程序在该操作上是非阻塞的

### 1.3 同步

同步意味着有序

### 1.4 异步

异步意味着无序

### 1.5 并发

以利用有限的计算机资源使多个任务可以被实时或近实时执行为目的。

### 1.6 并行

以利用富余计算资源（多核CPU）加速完成多个任务为目的。

### 1.7并发和并行：

简而言之就是一个人同时吃三个馒头还是三个人同时分别吃一个的情况，吃一个馒头算一个任务

或者：并发是两个队列同时使用一台咖啡机，并行是两个队列同时使用两台咖啡机，串行，一个队列使用一台咖啡机

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/asyncio_Concurrent.jpg)

* 并行是为了利用多核加速多任务完成的进度
* 并发是为了让独立的子任务都有机会被尽快执行，但不一定能加速整体进度
* 非阻塞是为了提高程序整体执行效率
* 异步是高效地组织非阻塞任务的方式

### 1.7同步阻塞 异步阻塞 同步非阻塞 异步非阻塞

* 同步阻塞 ： 自己取获取结果 这个过程不能干别的事情
* 同步非阻塞 ： 自己取结果，在没有取到结果之前你可以去干别的事情
* 异步阻塞 ： 不需要自己去取结果，别人送上门，在等的过程中自己不能干别的。
* 异步非阻塞：不需要自己取去结果， 别人把结果送上门，这个等结果的过程自己可干别的



## 2. Python的asyncio模块学习

### 2.1 函数解释

``` python
1、通过async关键字或者@asyncio.coroutine定义一个协程（coroutine）

2、async with叫做异步上下文管理器（asynchronous context manager）；async for叫做异步迭代器(asynchronous-iterators)。

2、asyncio.get_event_loop方法创建一个事件循环，

3、asyncio.ensure_future(coroutine) 和 loop.create_task(coroutine)都可以创建一个task，而task是future对象的子类

4、asyncio.gather(*tasks)或者asyncio.wait(tasks)都创建多个future对象。gather返回done，wait返回done和pending

5、run_until_complete 参数是一个futrue对象。但是如果当传入一个协程，其内部会自动封装成task，task是Future的子类。 将协程注册到事件循环，并启动事件循环。

6、run_until_complete 和 run_forever：run_until_complete 来运行 loop ，等到 future 完成，run_until_complete 也就返回了。future 结束，但是程序并不会退出。run_forever 会一直运行，直到 stop 被调用

7、r = yield from asyncio.sleep(1)    使用生成器yield，模拟IO操作等耗时的操作。目的也是让这些IO操作异步化。

8、并发和并行：简而言之就是一个人同时吃三个馒头还是三个人同时分别吃一个的情况，吃一个馒头算一个任务。

9、asyncio实现并发，就需要多个协程来完成任务，每当有任务阻塞的时候就await，然后其他协程继续工作。创建多个协程的列表，然后将这些协程注册到事件循环中。
```

### 2.2 asyncio的Methods

``` python
import asyncio

print(dir(asyncio))
methods = ['ALL_COMPLETED', 'AbstractEventLoop', 'AbstractEventLoopPolicy', 'AbstractServer', 'BaseEventLoop',
           'BaseProtocol', 'BaseTransport', 'BoundedSemaphore', 'CancelledError', 'Condition', 'DatagramProtocol',
           'DatagramTransport', 'DefaultEventLoopPolicy', 'Event', 'FIRST_COMPLETED', 'FIRST_EXCEPTION', 'Future',
           'Handle', 'IncompleteReadError', 'InvalidStateError', 'IocpProactor', 'JoinableQueue', 'LifoQueue', 'Lock',
           'PriorityQueue', 'ProactorEventLoop', 'Protocol', 'Queue', 'QueueEmpty', 'QueueFull', 'ReadTransport',
           'SelectorEventLoop', 'Semaphore', 'StreamReader', 'StreamReaderProtocol', 'StreamWriter', 'SubprocessProtocol',
           'SubprocessTransport', 'Task', 'TimeoutError', 'TimerHandle', 'Transport', 'WriteTransport', '__all__',
           '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__',
           '__spec__', '_overlapped', 'as_completed', 'async', 'base_events', 'base_subprocess', 'constants', 'coroutine',
           'coroutines', 'create_subprocess_exec', 'create_subprocess_shell', 'events', 'futures', 'gather',
           'get_child_watcher', 'get_event_loop', 'get_event_loop_policy', 'iscoroutine', 'iscoroutinefunction', 'locks',
           'log', 'new_event_loop', 'open_connection', 'proactor_events', 'protocols', 'queues', 'selector_events',
           'selectors', 'set_child_watcher', 'set_event_loop', 'set_event_loop_policy', 'shield', 'sleep', 'sslproto',
           'start_server', 'streams', 'subprocess', 'sys', 'tasks', 'transports', 'wait', 'wait_for', 'windows_events',
           'windows_utils', 'wrap_future']

print(help(asyncio.get_event_loop))
```

### 2.3 Task
``` python
'''
创建task后，task在加入事件循环之前是pending状态，因为do_some_work中没有耗时的阻塞操作，task很快就执行完毕了。
后面打印的finished状态。

asyncio.ensure_future(coroutine) 和 loop.create_task(coroutine)都可以创建一个task，
run_until_complete 参数是一个futrue对象。但是如果当传入一个协程，其内部会自动封装成task，task是Future的子类。 将协程注册到事件循环，并启动事件循环。
isinstance(task, asyncio.Future)将会输出True。
'''
import asyncio
import threading
import time

@asyncio.coroutine
def do_some_work():
    print(threading.current_thread(), time.time())
    r = yield from asyncio.sleep(1)
    print(threading.current_thread(), time.time())

loop = asyncio.get_event_loop()
task = loop.create_task(do_some_work())    # 创建一个task
print(task) # <Task pending coro=<do_some_work() running at C:/Users/Asus/Desktop/py/demo/Python_demo/demo_asyncio/demo2.py:11>>
loop.run_until_complete(task)        # # 此时才是真正的开始执行do_some_work函数里的代码
print(task) # <Task finished coro=<do_some_work() done, defined at C:/Users/Asus/Desktop/py/demo/Python_demo/demo_asyncio/demo2.py:11> result=None>
print(isinstance(task, asyncio.Future)) # True
loop.close()
```

### 2.4 回调函数
假如协程是一个 IO 的读操作，等它读完数据后，我们希望得到通知，以便下一步数据的处理。这一需求可以通过往 future 添加回调来实现。

##### 2.4.1 绑定回调函数：↓

``` python
import asyncio
import time
import threading

@asyncio.coroutine
def do_some_work():
    print(threading.current_thread(), time.time())
    r = yield from asyncio.sleep(1)
    print(threading.current_thread(), time.time())
    return 'do_some_work Done'

# 回调
def callback(future):
    print(future)       # <Task finished coro=<do_some_work() done, defined at C:/Users/Asus/Desktop/py/demo/Python_demo/demo_asyncio/test.py:5> result='do_some_work Done'>
    print(dir(future))
    print('Callback : {}'.format(future.result()))          # Callback : do_some_work Done

loop = asyncio.get_event_loop()
task = loop.create_task(do_some_work())
'''
task = loop.create_task(do_some_work())
task            # <Task pending coro=<do_some_work() running at C:/Users/Asus/Desktop/py/demo/Python_demo/demo_asyncio/test.py:5>>      pending:在等待…期间
type(task)      # <class 'asyncio.tasks.Task'> create_task创建一个task对象
dir(task)
['__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
'__getattribute__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
'__weakref__', '_all_tasks', '_blocking', '_callbacks', '_copy_state', '_coro', '_current_tasks', '_exception', 
'_format_callbacks', '_fut_waiter', '_log_destroy_pending', '_log_traceback', '_loop', '_must_cancel', '_repr_info', 
'_result', '_schedule_callbacks', '_set_result_unless_cancelled', '_source_traceback', '_state', '_step', '_tb_logger', 
'_wakeup', 'add_done_callback', 'all_tasks', 'cancel', 'cancelled', 'current_task', 'done', 'exception', 'get_stack', 
'print_stack', 'remove_done_callback', 'result', 'set_exception', 'set_result']
'''
task.add_done_callback(callback)    # task和callback回调里的future对象，实际上是同一个对象
loop.run_until_complete(task)       # 此时才是真正的开始执行do_some_work函数里的代码
loop.close()
```

``` python
import asyncio
import time
import threading
import functools

@asyncio.coroutine
def do_some_work():
    print(threading.current_thread(), time.time())
    r = yield from asyncio.sleep(1)
    print(threading.current_thread(), time.time())
    return 'do_some_work Done'

# 回调, 传递多参数
def callback(t, future):
    print(future)       # <Task finished coro=<do_some_work() done, defined at C:/Users/Asus/Desktop/py/demo/Python_demo/demo_asyncio/test.py:5> result='do_some_work Done'>
    print(dir(future))
    print('Callback : {} {}'.format(t, future.result()))          # Callback : 2 do_some_work Done

loop = asyncio.get_event_loop()
task = loop.create_task(do_some_work())
'''
task = loop.create_task(do_some_work())
task            # <Task pending coro=<do_some_work() running at C:/Users/Asus/Desktop/py/demo/Python_demo/demo_asyncio/test.py:5>>      pending:在等待…期间
type(task)      # <class 'asyncio.tasks.Task'> create_task创建一个task对象
dir(task)
['__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
'__getattribute__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
'__weakref__', '_all_tasks', '_blocking', '_callbacks', '_copy_state', '_coro', '_current_tasks', '_exception', 
'_format_callbacks', '_fut_waiter', '_log_destroy_pending', '_log_traceback', '_loop', '_must_cancel', '_repr_info', 
'_result', '_schedule_callbacks', '_set_result_unless_cancelled', '_source_traceback', '_state', '_step', '_tb_logger', 
'_wakeup', 'add_done_callback', 'all_tasks', 'cancel', 'cancelled', 'current_task', 'done', 'exception', 'get_stack', 
'print_stack', 'remove_done_callback', 'result', 'set_exception', 'set_result']
'''
task.add_done_callback(functools.partial(callback, 2))  # task和callback回调里的future对象，实际上是同一个对象
loop.run_until_complete(task)       # 此时才是真正的开始执行do_some_work函数里的代码
loop.close()
```

##### 2.4.2 不绑定回调函数：↓

``` python
import asyncio
import time
import threading
import functools

@asyncio.coroutine
def do_some_work():
    print(threading.current_thread(), time.time())
    r = yield from asyncio.sleep(1)
    print(threading.current_thread(), time.time())
    return 'do_some_work Done'

loop = asyncio.get_event_loop()
task = loop.create_task(do_some_work())
loop.run_until_complete(task)      
print(task.result())                # do_some_work Done    task此时fiinished状态。在这个时候，可以直接读取task的result方法。
loop.close()
```


### 2.5 阻塞和await
使用async可以定义协程对象，使用await可以针对耗时的操作进行挂起，

就像生成器里的yield一样，函数让出控制权。

协程遇到await，事件循环将会挂起该协程，执行别的协程，直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行。

耗时的操作一般是一些IO操作，例如网络请求，文件读取等。我们使用asyncio.sleep函数来模拟IO操作。协程的目的也是让这些IO操作异步化。

* 把@asyncio.coroutine替换为async；
* 把yield from替换为await。

``` python
import time
import threading
import asyncio

async def hello():
    print(threading.current_thread(), time.time())
    r = await asyncio.sleep(1)
    print(threading.current_thread(), time.time())

loop = asyncio.get_event_loop()     # 创建一个事件循环
loop.run_until_complete(hello())        # 将协程注册到事件循环，并启动事件循环
loop.close()
```

在 sleep的时候，使用await让出控制权。即当遇到阻塞调用的函数的时候，使用await方法将协程的控制权让出，以便loop调用其他的协程。现在我们的例子就用耗时的阻塞操作了。


### 2.6 并发和并行
asyncio实现并发，就需要多个协程来完成任务，每当有任务阻塞的时候就await，然后其他协程继续工作。创建多个协程的列表，然后将这些协程注册到事件循环中。

用wait和gather方法

* asyncio.wait(tasks) 也可以使用 asyncio.gather(*tasks) ,前者接受一个task列表，后者接收一堆task。
* asyncio.wait(tasks)
* asyncio.gather(*tasks)

``` python
# asyncio实现并发，就需要多个协程来完成任务，每当有任务阻塞的时候就await，然后其他协程继续工作。
# 创建多个协程的列表，然后将这些协程注册到事件循环中。
import aiohttp
import asyncio

async def func(url):    # async定义一个协程
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print('curl : [{}]'.format(url))
            await asyncio.sleep(1)      # 模拟IO操作或者网络请求
            print('[{}] sleep 1s'.format(url))

urls = ['http://0xsafe.org/', 'https://www.bugbank.cn/', 'http://sec.baidu.com/views/main/index.html#home',
        'http://security.jd.com/', 'https://sec.ctrip.com/', 'http://sec.sina.com.cn/',
        'http://www.robam.com', 'http://www.ximalaya.com', 'http://www.ztgame.com/', 'http://www.omegatravel.net',
        'http://www.zhiye.com', 'http://www.tita.com', 'http://www.beisen.com']

# task = func('http://0xsafe.org/')
# print(type(task))       # coroutine

loop = asyncio.get_event_loop()
tasks = [func(url) for url in urls]
# loop.run_until_complete(asyncio.gather(*tasks)) # gather传递多参数
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
```

### 2.7 协程的嵌套、gather、wait

gather 起聚合的作用，把多个 futures 包装成单个 future，因为 loop.run_until_complete 只接受单个 future。

``` python
# 协程嵌套
import asyncio
import aiohttp

urls = ['http://0xsafe.org/', 'https://www.bugbank.cn/', 'http://sec.baidu.com/views/main/index.html#home',
        'http://security.jd.com/', 'https://sec.ctrip.com/', 'http://sec.sina.com.cn/',
        'http://www.robam.com', 'http://www.ximalaya.com', 'http://www.ztgame.com/', 'http://www.omegatravel.net',
        'http://www.zhiye.com', 'http://www.tita.com', 'http://www.beisen.com']

async def func(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print('[{}] : {}'.format(res.status, res.url))
            await asyncio.sleep(1)
            return '[{}] : sleep 1'.format(url)

async def main():
    tasks = [func(url) for url in urls]

    dones, pending = await asyncio.wait(tasks)
    for task in dones:
        print('task ret :{}'.format(task.result()))

    # 如果使用的是 asyncio.gather创建协程对象，那么await的返回值就是协程运行的结果。
    # rets = await asyncio.gather(*tasks)
    # for ret in rets:
    #     print('task ret :{}'.format(ret))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### 2.8 run_until_complete 和 run_forever

用 gather 把多个协程合并成一个 future，并添加回调，然后在回调里再去停止 loop。

run_until_complete 和 run_forever：run_until_complete 来运行 loop ，等到 future 完成，run_until_complete 也就返回了。future 结束，但是程序并不会退出。run_forever 会一直运行，直到 stop 被调用

``` python
# run_until_complete 和 run_forever的区别

# run_until_complete
import asyncio
import aiohttp
import functools

urls = ['http://0xsafe.org/', 'https://www.bugbank.cn/', 'http://sec.baidu.com/views/main/index.html#home',
        'http://security.jd.com/', 'https://sec.ctrip.com/', 'http://sec.sina.com.cn/',
        'http://www.robam.com', 'http://www.ximalaya.com', 'http://www.ztgame.com/', 'http://www.omegatravel.net',
        'http://www.zhiye.com', 'http://www.tita.com', 'http://www.beisen.com']

async def func(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print('[{}] : {}'.format(res.status, res.url))
            await asyncio.sleep(1)
            return '[{}] : sleep 1'.format(url)

def callback(t, future):
    loop.stop()

tasks = [func(url) for url in urls]
loop = asyncio.get_event_loop()
futus = asyncio.gather(*tasks)
futus.add_done_callback(functools.partial(callback, loop)) # 用 gather 把多个协程合并成一个 future，并添加回调，然后在回调里再去停止 loop。
loop.run_forever()
```

### 2.9 线程协程
``` python
# 新线程协程
import asyncio
import time
import threading
from threading import Thread

def start_loop(loop):
    print(threading.current_thread())
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def do_some_work(x):
    print(threading.current_thread())
    print('Waiting {}'.format(x))
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

start = time.time()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()
print('TIME: {}'.format(time.time() - start))

ret1 = asyncio.run_coroutine_threadsafe(do_some_work(2), new_loop)
ret2 = asyncio.run_coroutine_threadsafe(do_some_work(3), new_loop)

print(ret1.result())
print(ret2.result())
```

## 3. 异步爬取网站标题 demo：

优点：`for i, url in enumerate(f):` 和 `del urls[:]` 可以减小内存的消耗

``` python
import asyncio
import requests
from bs4 import BeautifulSoup
import chardet
from threading import current_thread
import datetime

# 打印时间
def nowTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 定义异步方法：获取标题
async def searchTitle(url):
    html_doc = await getHtml(url)
    try:
        soup = BeautifulSoup(html_doc, 'html.parser')
        Title = soup.title.string.strip()                   # 利用bs4获取title内容，用strip去掉两边空格符
        return current_thread(), url, Title
    except Exception as e:
        return None

# 定义异步方法：获取网页源码
async def getHtml(url):
    print('[{}] : request {}'.format(nowTime(), url))
    res = requests.get(url, timeout=5)
    # print('[{}] : {} return response'.format(nowTime(), url))
    try:
        cont = res.content
        # 获取网页的编码格式
        charset = chardet.detect(cont)['encoding']
        # 对各种编码情况进行判断
        html_doc = cont.decode(charset)
    except Exception as e:
        html_doc = res.text
    return html_doc

if __name__ == '__main__':
    urls = []                   # 存放coroutineNums数量的url
    coroutineNums = 10          # 定义协程数
    coroutineNums_1 = coroutineNums - 1
    loop = asyncio.get_event_loop()     # 创建一个事件循环

    with open('urls.txt', 'rt') as f:
        for i, url in enumerate(f):             # 不用f.readlines(),因为f是生成器，用for迭代取出每个值。这样避免过度占用内存
            if i % coroutineNums != coroutineNums_1:        # 每coroutineNums个一组
                urls.append(url.strip())
            else:
                urls.append(url.strip())
                print(urls)                     # 打印每次请求的url
                tasks = [searchTitle(url) for url in urls]      # 创建多个协程的列表
                results = loop.run_until_complete(asyncio.gather(*tasks))       # run_until_complete 参数是一个futrue对象。但是如果当传入一个协程，其内部会自动封装成task，task是Future的子类。 将协程注册到事件循环，并启动事件循环。
                titles = filter(lambda title : title, results)        # 使用flter和lambda 过滤了结果为None的值
                for title in titles:          # 打印标题
                    print('[{}] : {}'.format(nowTime(), title))
                print('-'*50)
                del urls[:]         # 清除缓存
```

结果打印：↓ 可以看到很快速的就爬取了网站的标题

``` python
C:\Python36\python36.exe C:/Users/Asus/Desktop/py/demo/Python_demo/demo_asyncio/tset_asyncio/demo.py
['http://y.qq.com', 'http://guanjia.qq.com', 'http://dlied6.qq.com', 'http://soft.qq.com', 'http://pingjs.qq.com', 'http://id.qq.com', 'https://admin.qidian.qq.com', 'http://qidian.qq.com', 'https://pingjs.qq.com', 'https://wpa.qidian.qq.com']
[2018-06-23 14:24:14] : request https://wpa.qidian.qq.com
[2018-06-23 14:24:14] : request http://guanjia.qq.com
[2018-06-23 14:24:14] : request https://admin.qidian.qq.com
[2018-06-23 14:24:15] : request http://dlied6.qq.com
[2018-06-23 14:24:15] : request http://y.qq.com
[2018-06-23 14:24:15] : request http://soft.qq.com
[2018-06-23 14:24:16] : request https://pingjs.qq.com
[2018-06-23 14:24:16] : request http://pingjs.qq.com
[2018-06-23 14:24:16] : request http://qidian.qq.com
[2018-06-23 14:24:17] : request http://id.qq.com
[2018-06-23 14:24:17] : (<_MainThread(MainThread, started 28276)>, 'http://y.qq.com', 'QQ音乐-千万正版音乐海量无损曲库新歌热歌天天畅听的高品质音乐平台！')
[2018-06-23 14:24:17] : (<_MainThread(MainThread, started 28276)>, 'http://guanjia.qq.com', '一键杀毒_盗号保护_垃圾清理_软件管理-腾讯电脑管家官网')
[2018-06-23 14:24:17] : (<_MainThread(MainThread, started 28276)>, 'http://dlied6.qq.com', '403 Forbidden')
[2018-06-23 14:24:17] : (<_MainThread(MainThread, started 28276)>, 'http://soft.qq.com', '软件管理下载 - 腾讯软件管理官方网站')
[2018-06-23 14:24:17] : (<_MainThread(MainThread, started 28276)>, 'http://id.qq.com', '我的QQ中心')
[2018-06-23 14:24:17] : (<_MainThread(MainThread, started 28276)>, 'https://admin.qidian.qq.com', '腾讯企点账户中心')
[2018-06-23 14:24:17] : (<_MainThread(MainThread, started 28276)>, 'http://qidian.qq.com', '腾讯企点 - 数字化全渠道客户沟通互动平台')
--------------------------------------------------
['https://a.gdt.qq.com', 'https://xui.ptlogin2.qq.com', 'http://kf.qq.com', 'http://crm2.qq.com', 'http://110.qq.com', 'https://imgcache.qq.com', 'http://xui.ptlogin2.qq.com', 'http://isdspeed.qq.com', 'http://pinghot.qq.com', 'http://i.qq.com']
[2018-06-23 14:24:17] : request https://imgcache.qq.com
[2018-06-23 14:24:17] : request http://xui.ptlogin2.qq.com
[2018-06-23 14:24:17] : request https://a.gdt.qq.com
[2018-06-23 14:24:17] : request http://isdspeed.qq.com
[2018-06-23 14:24:17] : request http://kf.qq.com
[2018-06-23 14:24:17] : request http://pinghot.qq.com
[2018-06-23 14:24:17] : request http://crm2.qq.com
[2018-06-23 14:24:17] : request http://i.qq.com
[2018-06-23 14:24:18] : request https://xui.ptlogin2.qq.com
[2018-06-23 14:24:18] : request http://110.qq.com
[2018-06-23 14:24:18] : (<_MainThread(MainThread, started 28276)>, 'http://kf.qq.com', '腾讯客服官网首页')
[2018-06-23 14:24:18] : (<_MainThread(MainThread, started 28276)>, 'http://crm2.qq.com', '403 Forbidden')
[2018-06-23 14:24:18] : (<_MainThread(MainThread, started 28276)>, 'http://110.qq.com', '腾讯安全服务平台-帐号安全、QQ/微信诈骗举报受理综合服务平台')
[2018-06-23 14:24:18] : (<_MainThread(MainThread, started 28276)>, 'https://imgcache.qq.com', 'QQ空间-分享生活，留住感动')
[2018-06-23 14:24:18] : (<_MainThread(MainThread, started 28276)>, 'http://i.qq.com', 'QQ空间-分享生活，留住感动')
--------------------------------------------------
['https://qzs.qzone.qq.com', 'http://qzone.qzone.qq.com', 'http://blog.qq.com', 'http://money.qq.com', 'http://stockhtm.finance.qq.com', 'http://gongyi.qq.com', 'http://ssl.gongyi.qq.com', 'http://pay.gongyi.qq.com', 'http://thinker.qq.com', 'http://cul.qq.com']
[2018-06-23 14:24:18] : request http://stockhtm.finance.qq.com
[2018-06-23 14:24:18] : request http://money.qq.com
[2018-06-23 14:24:20] : request http://qzone.qzone.qq.com
[2018-06-23 14:24:20] : request http://pay.gongyi.qq.com
[2018-06-23 14:24:20] : request https://qzs.qzone.qq.com
[2018-06-23 14:24:21] : request http://blog.qq.com

Process finished with exit code 1
```