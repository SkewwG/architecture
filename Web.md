# Web

## 1、什么是Web？
万维网(缩写为WWW或Web)是一种信息空间，其中文档和其他Web资源由统一资源定位符（URL)标识，通过超文本链接互连，并且可以通过因特网访问。

## 2、Web的核心技术点

* html：定义超文本文档的结构和格式

* http：规定客户端和服务端如何通信

* url：描述资源在因特网上的位置

其他的技术（缓存，Session等等）都是对上述体系的完善，核心结构至今未变。只要实现上述的三个核心技术点，就可以构造一个静态网页。

**接下来解释这三个核心技术点：**
Web framework最核心的技术点就是routing：Web Server能够根据请求过来的url找到对应的静态文件或者可执行文件，然后返回资源给客户端。至于客户端和Web Server的通信是通过主机名/域名:端口。

* html：找到静态html页面或者动态生成html页面，html页面可以是图片，json等其他类型的资源
* http：Web Server服务端接收客户端通过http协议传递过来的内容，内容可以是表单、文本等类型。然后对内容解析并作出相应的响应。
* url：routing路由，Web Server找到与url对应的资源。

## 3、Web的发展史
* 1990年Http协议诞生，12月发布第一个网页浏览器WorldWideWeb和第一个Web服务器CERN httpd
* 1993年CGI诞生
* 1995年Apache Web服务诞生，JavaScript发布，Html2.0发布
* 1996年Http/1.0发布
* 2002年FireFox浏览器发布
* 2003年WSGI1.0发布
* 2004年Nginx发布
* 2005年AJAX发布
* 2006年JQuery发布
* 2014年HTML5.0发布

## 4、Web Server 和 HTTP Server
* Web Server：Web服务器，在Web服务器上运行一个HTTP daemon（守护）进程，当有url请求进来的时候，该Web服务器能够根据url把服务器上与url对应的内容返回给客户端浏览器。
* HTTP Server：HTTP协议或其扩展/加强协议的支持下，Web才能够成为一种信息空间。所以也可以说HTTP Server是Web Server

## 5、CGI协议（Common Gateway Interface）
* CGI：通用网关接口
* CGI的目的：实时的执行某些程序并输出动态内容
* CGI协议：规定Web Server和可以生成动态内容的可执行程序如何进行交互

  既然CGI协议是规定Web Server和可执行程序进行交互，那么我们就需要Web Server支持CGI协议。前面我们已经知道Web Server有Apache和Nginx，那么通过添加CGI模块或者插件（mod_php,mod_python）开启CGI，就可以让Apache或者Nginx执行某些可执行程序（比如PHP脚本或者Python脚本），生成动态页面。

  当Web Server添加了CGI模块或插件后，接下来要配置CGI。比如：Web Server执行可执行的文件需要放在哪个目录下，放在（/cgi/bin）目录下；Web Server要执行哪种类型的文件（shell，PHP，Python，C/C++）。
  
  
## 6、Apache 使用CGI运行py文件
#### 安装python和apache2

 ``` apt-get install python```  安装Python,默认2.7

 ``` apt-get install apache2``` 安装apache2，默认根目录在/var/www/html 下

#### 开启CGI

``` a2enmod cgi```  启动CGI模块

返回如下内容则说明正常开启CGI

```
Your MPM seems to be threaded. Selecting cgid instead of cgi.
 Enabling module cgid.
 To activate the new configuration, you need to run:
 service apache2 restart
```


开启了CGI模块后，默认情况下，CGI脚本允许在"/usr/lib/cgi-bin"目录下执行。

所以只要在"/usr/lib/cgi-bin"目录下创建demo_py.py文件后，客户端访问"http://(Apache2 Server)/cgi-bin/demo_py.py"后，Apache就会执行demo_py.py文件，并把内容返回给客户端。

#### Writing a CGI program
编写demo_py.py文件保存在"/usr/lib/cgi-bin"目录下：
```
#!/usr/bin/python

print('Content-type: text/html\n\n')
print('Hello, World.')
```

* 第一行脚本解释器的路径：告诉Apache（或者你正在运行的任何shell），该程序可以通过将文件提供给在该位置找到的解释器来执行

* 第三行输出我们讨论的内容类型声明，后面跟着两个回车换行符对

* 第四行输出字符串

#### 赋予权限
服务器不像我们在终端上一样运行。也就是说，当服务器启动时，它将以非特权用户的权限运行。所以需要给文件赋予权限。

```
chmod 705 /usr/lib/cgi-bin/demo_py.py
```
#### 最后客户端访问即可:http://www.example.com/cgi-bin/demo_py.py

#### 题外话：STDIN和STDOUT
服务器和客户端之间的其他通信通过标准输入（STDIN）和标准输出（STDOUT）进行。在正常的日常情况下， STDIN意味着键盘或程序被赋予执行的文件，STDOUT 通常意味着控制台或屏幕。

当POST请求时，表单中的数据将被捆绑成一种特殊的格式并传递给CGI程序中STDIN。然后程序可以像处理来自键盘或文件一样处理该数据。

### 6.2 前面介绍的是默认目录，如果不想使用默认的cgi-bin目录，使用自己创建的目录
例如：想让cgi脚本在"/var/www/html/cgi-enabled"目录下

#### 在conf-available目录下新建一个cgi-enabled.conf文件
```vi /etc/apache2/conf-available/cgi-enabled.conf``` 

cgi-enabled.conf文件内容：
```
<Directory "/var/www/html/cgi-enabled">
    Options +ExecCGI
    AddHandler cgi-script .py .cgi .pl
</Directory></pre>
```

#### 启动新建的cgi-enabled.conf文件
```a2enconf cgi-enabled```

#### 创建"/var/www/html/cgi-enabled"目录,并新建一个测试文件demo_py.py
```mkdir /var/www/html/cgi-enabled```

```vi demo_py.py```

demo_py.py文件内容为：

```
#!/usr/bin/python

print "Content-type: text/html\n\n"
print "<html>\n<body>\n"
print "<div style=\"width: 100%; font-size: 40px; font-weight: bold; text-align: center;\">\n"
print "CGI Test Page"
print "\n</div>\n"
print "</body>\n</html>\n"
```

#### 修改权限
```
chmod 705 /var/www/html/cgi-enabled/demo_py.py
```

### 6.3 不使用a2enmod开启CGI模块
#### 1、 在httpd.conf文件里确保 LoadModule 指令没有被注释掉
```LoadModule cgid_module modules/mod_cgid.so```

#### 2、 ScriptAlias指令
告诉Apache为CGI程序预留了一个特定的目录。Apache会假定这个目录中的每个文件都是一个CGI程序，并且当客户端请求该特定资源时将尝试执行它。

任何对/cgi-bin/开始的资源请求都应该从该目录"/usr/local/apache2/cgi-bin/"中寻找，如果URL http://www.example.com/cgi-bin/test.pl 被请求，Apache将尝试执行"/usr/local/apache2/cgi-bin/test.pl"该文件，并返回输出。当然，文件必须存在，并且可执行，并以特定方式返回输出，否则Apache将返回错误消息。

#### 3、Options指令、AddHandler指令

下面的指令告诉Apache允许执行CGI文件

```
<Directory "/usr/local/apache2/htdocs/somedir">
    Options +ExecCGI
</Directory>
```

AddHandler指令告诉服务器将所有带有cgi、pl或py扩展名的文件视为CGI程序

```AddHandler cgi-script .cgi .pl .py```

## 7、CGI的流程图及执行步骤：
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/CGI.png)

* 客户端发送请求给Web Server（Apache）

* Apache接收到客户端发送的请求，解析传递过来的内容。如果是动态请求，那么就会启动脚本解释器，并传递CGI的环境变量。

* 脚本解释器启动后，就会在刚才传递过来的CGI目录下找到客户端请求的那个文件，然后去执行该脚本。执行完后将内容返回给Apache或者直接返回给客户端。


## 8、WSGI
WSGI（Web Server Gateway Interface，Web 服务器网关接口）则是[Python](http://lib.csdn.net/base/python "Python知识库")语言中所定义的Web服务器和Web应用程序之间或框架之间的**通用接口标准**。

WSGI诞生的背景是各种Python Web框架各自为政，如有的使用Python实现Server功能，有的则靠FastCGl之类的网关协议调用Python，为了普通用户在选择框架时不受太多限制，也为了隔离serer开发和framework开发。

## 9.Apache
由NCSA httpd 1.3演进而来的Web Server

* mod_python已停更

* mod_fastcgi有点问题，市场占有率小

* mod_fcgid用于代替mod_ fastcgi，结合flup使用

* mod_wsgi支持嵌入Apache Server或运行独立的守护进程与FastCGl结合使用

## 10.Nginx
Nginx诞生的初衷是为了解决C10k问题，基于异步事件驱动架构,现今它已集HTTP Server,  Reverse Proxy Server,  Mail Proxy,  Server,  Generic TCP/UDP Proxy Server于一身。常用它做HTTP Server，反向代理(流量转发、HTTP缓存服务器，软负载均衡器)

## 11.Web Application&Web Framework
* 可以使用Web Framework去建立Web Application

* Web Application可以生成动态内容，而不仅仅返回静态内容。例如Flask的app就是Web Application

* Web Framework主要搞定类似MVC架构、routing、session、authentication、security等方面，为日益复杂和规模庞大的Web Application开发提供便利。例如Django、Flask、Tornado


参考资料：
https://httpd.apache.org/docs/2.4/howto/cgi.html
https://www.server-world.info/en/note?os=Ubuntu_14.04&p=httpd&f=2
