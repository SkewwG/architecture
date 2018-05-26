
# HTTP协议
全称:Hypertext Transfer Protocol(超文本转移协议)

**HTTP是一个无状态的协议**，每一次请求不会保存客户端和服务端的状态

## 1. 基于HTTP的交互过程
两幅图：↓
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP1.png)

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP2.png)

问：http协议在什么地方发挥作用？

答：在tcp/ip协议基础上，创造了http协议

问：http协议在通信中的主体是什么？

答：message(消息)

问：请求是什么？

答：发送一个http的request message

## 2. 属于应用层协议
先看一下OSI模型和TCP/IP模型

两幅图片：↓

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_OSI.png)

---

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_TCP_IP.png)

**【重点1】：HTTP协议属于应用层协议**

**【重点2】：tcp是传输层，数据报文的传输，不管数据的格式，不会解读数据报文。**

## 3.基于CS架构

Client端：即HTTP Agent的功能由浏览器(Browser)实现，又称BS架构

HTTP Server端：即提供超文本(已发展为超媒体)服务

超媒体：各种Link，各种图片音频等

请求一响应:只能由Client主动发起请求，Server再返回响应

## 4. 无状态和Cookie & Session
**【重点3】：为了使http有状态，使用Cookie和Session**

## 5. 基于文本
HTTP协议在应用层是基于文本的

## 6. 持久连接
什么是持久连接？就是"持久"的连接。

**【重点4】：传输报文是靠建立TCP连接**

为了完成一个HTTP事务，**服务器和客户端之间要建立一条TCP连接来传输报文**，这个事务结束以后一般都会直接把它关闭，这是正常的模式。可是这样**会造成网络使用效率的降低**。原因如下：↓

1、每次建立连接的时候都要经过三次握手等必须的程序，如果拥有一条可以一直使用的连接，也就意味着只需要进行一次连接的建立，这就省去了每次建立连接的时间。

2、使用过的连接会比新建立的连接速度会快一些，这是因为**TCP连接慢启动**的特性，每次建立新的连接，不如已经建立好的的连接速度快。

两幅图片：↓

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_chijiulianjie1.png)

---

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_chijiulianjie2.png)


**【重点5】：tcp连接复用**，请求一次响应一次，然后再请求一次响应一次，而不会关闭tcp连接。如上图。

问：如何建立持久连接？
答：使用**keep-alive**

客户端先发出请求，以connection：keep-alive的形式传向服务器，如果服务器接受的请求的话响应中就会带有connection：keep- alive.可以使用keep-alive首部传递一些关于持久连接的参数：**timeout表示持续时间，max表示希望还在这条持久连接上传输多少个HTTP服务**，但是这些都不是**承诺值，也就是说随时都可以反悔**。

注意点：如果要是用持久连接，那么就一定要有正确的content-length这个描述主体长度的首部，因为持久连接会连续的传输HTTP事务，而判断连续的HTTP事 务之间的分界点就是靠content-length告诉的主体的长度了，如果错误或没有告诉主体的长度的话，那么就没办法知道这个事务在哪里结束了。


## 7. 管线化 pipelining
即：**流水线技术**

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_pipelining.png)

**【重点6】：pipelining**：把多个HTTP请求放到一个TCP连接中一一发送，而在发送过程中客户端不需要等待服务器对前一个请求的响应。

**【重点7】：队头阻塞**：服务端要按照顺序处理请求，如果前一个请求非常耗时，那么后续请求都会受到影响。客户端要按照发送请求的顺序来接收响应。

**【重点8】：**相比于第六节的第二幅图，管线化改进之处就是不需要等待服务端对上一个请求作出响应之后才可以发送下一个请求。

## 8. URL
定位要进行通信的服务主机以及想要获取的资源

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_url.png)

## 9. HTTP_Method
**【重点9】：指示Server对请求的资源应做何种行为/操作**

* GET:服务端只检索既有资源返回给客户端，不应有其他副作用。

* POST:客户端将新建资源所需的数据携带在请求中，使服务端创建一个新资源。

* PUT:客户端提供完整的资源信息给服务端，服务端据此更新既有资源或创建新资源。

* DELETE:服务端删除指定的资源。

* PATCH:客户端提供指定资源的部分信息，服务端据此对既有资源做局部更新。

* HEAD:服务端构造与GET方法一模一样的响应头部返回给客户端，便于客户端获取该资源的元信息，而非整体传输。常用于检查资源是否已改动。

* TRACE返回客户端请求经由哪些跃点到达了服务端，中间代理或网关在转发该请求时应将自己的IP或DNS名称添加到头部的Via字段中。常用于诊断。

* OPTIONS:服务端返回该URL支持的盯下P方法。通常请求’*’，而非具体资源。

**【重点10】：GET和HEAD，不管是哪个WEB SERVER 必须实现GET和HEAD，实现了这两个方法之后，才能称为HTTP SERVER，才能给别人提供资源**

![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_Method.png)

HTTP Server必须支持GET和HEAD方法，其他方法可选，也可以自定义进行扩展。

## 10. 状态码
* 1XX：信息，请求已被服务端收到，请继续。日丁丁P/1.1才支持

* 2XX：成功，请求已成功被服务端收到、理解并处理完毕

* 3XX：重定向，需要进一步的操作才能完成此请求

* 4XX：客户端错误，请求含有词法错误或者无法被执行

* 5XX：服务端错误，服务端在处理请求的过程中发生错误

---
**【重点11】：第九节和第十节小结：↓**

URL+HTTP Method可实现Client告诉Server该如何处理请求。比如让Server对数据的增删改查

Status Codes可实现Server告诉Client该如何解释响应。比如显示正确页面或者跳转到另一个url去。

---

## 11. 消息格式
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_MessageFormat.png)

<>尖括号是必选

**RequestMessage**
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_RequestMessage.png)


**ResponseMessage**
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_ResponseMessage.png)

## 12.HTTP头部

### **HTTP头部字段结构**

头部字段的结构为key-vlaue的结构。

> 头部字段名 : 字段值 
> 例如 Content-Length: 139

字段值对应单个头部字段名可以有多个值

> 头部字段名 : 字段值1,字段值2 … 
> 例如 Keep-Alive: timeout=15,max=100


### 通用头部字段

**请求报文和响应报文都用到的字段。**

头部字段名 | 说明
- | :-: 
Cache-Control | 控制缓存的行为 
Connection    | 逐跳首部、连接的管理 
Date | 创建报文的日期时间 
Pragma | 报文指令 
Trailer | 报文末端的头部一览 
Transfer-Encoding | 制定报文主体的传输编码方式 
Upgrade | 升级为其他协议 
Via | 代理服务器相关信息 
Warning | 错误通知 

### 实体头部字段

**针对请求和响应报文的头部字段，补充了资源更新时间以及实体的有关信息**

头部字段名 | 说明
- | :-: 
头部字段名 | 说明 
Allow | 资源可支持的HTTP方法 
Content-Encoding | 实体主体适用的编码方式 
Content-Language | 实体主体的自然语言 
Content-Length | 实体主体的大小（单位：字节） 
Content-Location | 替代对应资源的URI 
Content-MD5 | 实体主体的报文摘要 
Content-Range | 实体主体的位置范围 
Content-Type | 实体主体的媒体类型 
Expries | 实体主体过期的日期时间 
Last-Modified | 资源的最后修改日期 

### 请求头部字段

请求报文使用的头部字段，补充了请求的附加内容、客户信息、响应优先级等信息。


头部字段名 | 说明
- | :-: 
Accept | 用户代理可处理的媒体类型 
Accept-Charset | 优先的字符集 
Accept-Encoding | 优先的内容编码 
Accept-Language | 优先的语言（自然语言） 
Authorization | Web认证信息 
Expect | 期待服务器的特定行为 
From | 用户的电子邮箱地址 
Host | 请求资源所在服务器 
If-Match | 比较实体标记（Etag） 
If-Modified-Since | 比较资源的更新时间 
If-None-Match | 比较实体标记（与If-Match相反） 
If-Range | 资源未更新时发送实体Byte的范围请求 
If-Unmodified-Since | 比较资源的更新时间，与If-Modified-Since相反 
Max-Forwards | 最大传输逐跳数 
Proxy-Authorization | 代理服务器要求客户端的认证信息 
Range | 实体的字节范围请求 
Referer | 对请求中URI的原始获取方 
TE | 传输编码的优先级 
User-Agent | HTTP客户端程序的信息 

### 响应头部字段

响应报文使用的头部字段，补充了响应的附加内容。

头部字段名 | 说明
- | :-: 
头部字段名 | 说明 
Accept-Ranges | 是否接受字节范围请求 
Age | 推算资源创建经过时间 
Etag | 资源的匹配信息 
Location | 令客户端重定向至制定URI 
Proxy-Authenticate | 代理服务器对客户端的认证信息 
Retry-After | 对再次发起请求的时机要求 
Server | 代理服务器缓存的管理信息 
WWW-Authenticate | 服务器对客户端的认证信息 



# 13. HTTP的缺点和瓶颈
* 基于明文文本的通信内容可能被窃听

* 不验证通信双方的身份可能遭伪装

* 无法证明报文完整性可能遭篡改

* 一条连接上只可发一个请求

* 队头阻塞

* 请求只能由客户端发起，客户端不可接受响应之外的指令

* 请求和响应的首部未经压缩就发送，首部信息越多延迟越大

* 发送冗长的首部，多次来回之间首部大部分字段都未改变，浪费资源

* 可选择任意压缩格式，不强制压缩后发送

**【重点12】：基于明文文本的通信内容可能被窃听: 比如内网渗透里的C段嗅探，嗅探数据库的账号密码。**

**前三条与安全相关，后六条与传输性能相关**

# 14. HTTP/2
The focus of the protocol is on performance; specifically, end-user perceived latency, network and server resource usage. One major goal is to allow the use of a single connection from browsers to a Web site.


主要特性:

* 二进制分帧

* 多路复用(一源一个TCP，一TCP多个请求一响应，消除队头阻塞)

* 流量控制(拥塞控制与优先级控制)

* 服务端推送：
一个请求多个响应，一个request message对应多个response message。而不是一个 request 对应一个response。但是前提是client先发起request请求。

* 头部压缩：

* 管线化请求

* TLS义务化

### 14.1 二进制分帧
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_BinaryFraming.png)
HTTP 2.0最大的特点： 不会改动HTTP 的语义，HTTP 方法、状态码、URI 及首部字段，等等这些核心概念上一如往常，却能致力于突破上一代标准的性能限制，改进传输性能，实现低延迟和高吞吐量。而之所以叫2.0，是在于新增的二进制分帧层。

既然又要保证HTTP的各种动词，方法，首部都不受影响，那就需要**在应用层(HTTP2.0)和传输层(TCP or UDP)之间增加一个二进制分帧层。**

在二进制分帧层上，HTTP 2.0 会将所有传输的信息分割为更小的消息和帧,并对它们采用二进制格式的编码 ，其中HTTP1.x的**【重点13】：首部信息会被封装到Headers帧，request body则封装到Data帧里面。**

### 14.2 数据流、消息、帧
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_Stream.png)

HTTP/2将HTTP协议通信分解为二进制编码帧的交换，这些帧对应着特定数据流中的消息。所有这些都在一个TCP连接内复用。这是HTTP/2协议所有其他功能和性能优化的基础。


**【重点14】：每个数据流以消息的形式发送，而消息由一或多个帧组成**

HTTP2.0所有通信都是在一个TCP连接上完成。HTTP 2.0 把 HTTP 协议通信的基本单位缩小为一个一个的帧，这些帧对应着逻辑流中的消息。


**【重点15】：HTTP性能的关键在于低延迟而不是高带宽！**大多数HTTP 连接的时间都很短，而且是突发性的，但TCP 只在长时间连接传输大块数据时效率才最高。HTTP 2.0 通过让所有数据流共用同一个连接，可以更有效地使用TCP 连接，让高带宽也能真正的服务于HTTP的性能提升。

### 14.3 请求与响应复用
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_multiplexing.png)

客户端和服务器可以将HTTP消息分解为互不依赖的帧，然后(各种姿势)交错发送，最后再在另一端把它们重新组装起来

**【重点16】：这些帧可以乱序发送，然后再根据每个帧首部的流标识符重新组装。**

**多路复用，解决了队头阻塞**

#### 【重点17】：与管线化相比，优点是Client不用按顺序一次次的发送请求，可以交错发送请求！

### 14.4 数据流优先级
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_priority.png)

数据流依赖关系和权重的组合让客户端可以构建和传递“优先级树”，表明它倾向于如何接收响应。反过来，服务器可以使用此信息通过控制CPU、内存和其他资源的分配设定数据流处理的优先级，在资源数据可用之后，带宽分配可以确保将高优先级响应以最优方式传输至客户端。

**【重点18】**：比如加载一个网页，网页里面有100张图片和其对应的缩略图，那么使用优先级，先加载出这100张的缩略图，然后再加载原图。

### 14.5 流控制
流控制是一种阻止发送方向接收方发送大量数据的机制，以免超出后者的需求或处理能力。

与**TCP协议的流控制**类似，但由于HTTP/2数据流在一个TCP连接内复用，TCP流控制既不够精细，也无法提供必要的应用级API来调节各个数据流的传输。

**应用层流控制**允许浏览器仅提取一部分特定资源，通过将数据流流控制窗口减小为零来暂停提取，稍后再行恢复。
**例如，只先获取图片预览然后暂停下载图片，再请求JS脚本，再恢复图片下载。**

**【重点19】：在应用层流控制里，请求可以暂停处理，即一个stream可以暂停！**

### 14.6 服务端推送
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_Push.png)

服务器可以对一个客户端请求发送多个响应。即，除了对最初请求的响应外服务器还可以向客户端推送额外资源，而无需客户端明确地请求。

### 14.7 头部压缩
![](https://raw.githubusercontent.com/SkewwG/architecture/master/Picture/HTTP_headerCompress.png)

通过静态Huffman代码对传输的标头字段进行编码，从而减小了各个传输的大小。要求客户端和服务器同时维护和更新一个包含之前见过的标头字段的索引列表，对之前传输的值进行有效编码。

## 15 HTTPS
安全和信任感
加密+认证+完整性保护
SSL vs TLS，后者取代前者

## 16 RESTful

RESTful, 全称Representational State Transfer。是一种设计风格，提供了一组设计原则和约束条件，主要用于客户端与服务器的交互。**【重点20】：通俗的讲：URL定位资源，用HTTP动词（GET,POST,DELETE,DETC）描述操作**

**【重点21】**：
* Representational：某种表现形式，比如用JSON，XML，JPEG等；

* State Transfer：状态变化。通过HTTP动词实现。


**【重点22】：建立API时要遵守的一种规则/风格。主要工作是设计 RESTful API（REST风格的网络接口。是一种优秀的规范、指导原则，但也不是教条！**

* GET 用来获取资源，

* POST 用来新建资源（也可以用于更新资源），

* PUT 用来更新资源，

* DELETE 用来删除资源。


**【重点23】：Server和Client之间传递某资源的一个表现形式，比如用JSON，XML传输文本，或者用JPG，WebP传输图片等。**

前后端用JSON或XML传输的是代表资源的数据结构，而非一个完整的HTML文档，尤其是一个复杂页面肯定由多个资源构成。


用 HTTP Status Code传递Server的状态信息。

**【重点24】：为什么要用RESTful结构？**
以前基本就用http的post和get。restful就是让你把delete put patch这些method给用起来，而不是通过post加上参数action=delete来实现删除操作。



参考文献：
https://www.cnblogs.com/icelin/p/3974935.html
https://blog.csdn.net/qq_28885149/article/details/52922107
https://blog.csdn.net/u010369338/article/details/65627999
https://blog.csdn.net/u011904605/article/details/53012844
https://www.zhihu.com/question/28557115/answer/48094438
