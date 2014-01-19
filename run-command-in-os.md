操作系统下运行命令分析
===

## shell 下执行外部命令

运行命令最简便的办法就是将命令所在目录加入 `PATH` 环境变量,
然后在命令行 shell 下输入执行.
外部程序在 shell 下叫做外部命令.
外部命令分为二进制可执行文件 (以下简称二进制) 和脚本两种.
windows 下 "shell" 是 "cmd", windows 叫法是命令解释器, 
linux 下通常是 "bash".
两者语法和功能差异很大, 但执行命令的基本方式是相似的.

执行脚本时大概流程如下:

0. 命令行输入是一个字符串列表, 第一个元素是命令名.
0. 根据命令名找到命令文件, 这时会搜索 `PATH`.
0. 找到命令脚本文件对应的解释器.
0. 运行解释器执行脚本.

执行二进制文件时前两步是一样的，第三步相对简单一点, 直接运行二进制文件.

以二进制文件 `java` 和脚本 `mvn` 为例.

linux bash 下执行结果:

```sh
observer.hany@ali-59375nm:~$ java -version
java version "1.7.0_40"
Java(TM) SE Runtime Environment (build 1.7.0_40-b43)
Java HotSpot(TM) Server VM (build 24.0-b56, mixed mode)

observer.hany@ali-59375nm:~$ mvn -version
Apache Maven 3.0.5 (r01de14724cdef164cd33c7c8c2fe155faf9602da; 2013-02-19 21:51:28+0800)
Maven home: /opt/apache-maven-3.0.5
Java version: 1.7.0_40, vendor: Oracle Corporation
Java home: /opt/jdk1.7.0_40/jre
Default locale: zh_CN, platform encoding: UTF-8
OS name: "linux", version: "3.5.0-45-generic", arch: "i386", family: "unix"
```

windows cmd 下执行结果:

```bat
C:\Documents and Settings\observer.hany>java -version
java version "1.6.0_45"
Java(TM) SE Runtime Environment (build 1.6.0_45-b06)
Java HotSpot(TM) Client VM (build 20.45-b01, mixed mode, sharing)

C:\Documents and Settings\observer.hany>mvn -version
Apache Maven 2.2.1 (r801777; 2009-08-07 03:16:01+0800)
Java version: 1.6.0_45
Java home: D:\opt\jdk1.6.0_45\jre
Default locale: zh_CN, platform encoding: GBK
OS name: "windows xp" version: "5.1" arch: "x86" Family: "windows"
```

### windows cmd 下执行命令的几个问题

cmd "shell" 下启动 GUI 程序直接返回,
但批处理脚本中会等待.

start 新开一个窗口执行命令.
GUI 没有命令行窗口, 有无 start 一样, 
但是 `start /WAIT` 可以等待 GUI 程序退出再返回.

cmd 语法, 冒号表示字符串, 
字符串内部可以冒号转义冒号, 即字符串内部两个连续冒号表示一个冒号.
字符串内也可以使用 `'\"'` 转义冒号, 似乎更清晰点, 避免混淆.
cmd 语法功能有限, 无法表达一些特殊参数, 
比如 `"a > b"` 总是导致重定向.

## 程序代码执行外部命令

python 中可以使用 `subprocess.call()` 函数实现相同的功能.
运行二进制文件命令时没有问题.

linux 下执行结果:

```python
>>> import subprocess
>>> subprocess.call(["java", "-version"])
java version "1.7.0_40"
Java(TM) SE Runtime Environment (build 1.7.0_40-b43)
Java HotSpot(TM) Server VM (build 24.0-b56, mixed mode)
0
```

windows 下执行结果:

```python
>>> import subprocess
>>> subprocess.call(["java", "-version"])
java version "1.6.0_45"
Java(TM) SE Runtime Environment (build 1.6.0_45-b06)
Java HotSpot(TM) Client VM (build 20.45-b01, mixed mode, sharing)
0
```

但执行脚本命令时, 
在 linux 下没有问题:

```python
>>> subprocess.call(["mvn", "-version"])
Apache Maven 3.0.5 (r01de14724cdef164cd33c7c8c2fe155faf9602da; 2013-02-19 21:51:28+0800)
Maven home: /opt/apache-maven-3.0.5
Java version: 1.7.0_40, vendor: Oracle Corporation
Java home: /opt/jdk1.7.0_40/jre
Default locale: zh_CN, platform encoding: UTF-8
OS name: "linux", version: "3.5.0-45-generic", arch: "i386", family: "unix"
0
```

在 windows 下就会有问题:

```python
>>> subprocess.call(["mvn", "-version"])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "D:\opt\Python3\App\lib\subprocess.py", line 470, in call
    return Popen(*popenargs, **kwargs).wait()
  File "D:\opt\Python3\App\lib\subprocess.py", line 744, in __init__
    restore_signals, start_new_session)
  File "D:\opt\Python3\App\lib\subprocess.py", line 977, in _execute_child
    startupinfo)
WindowsError: [Error 2] 系统找不到指定的文件。
```

java 中实现类似的功能的类是 `ProcessBuilder`.
通常子进程会继承父进程的标准输入输出.
与常规行为不同, `ProcessBuilder` 默认重定向了输入输出,
并且直到 jdk7 才支持设置成继承.
java 在这方面的支持是比较差.

示例代码如下:

```java
package test;

import org.apache.commons.exec.PumpStreamHandler;

public class Main {

	public static void main(String[] args) throws Exception {
		ProcessBuilder builder = new ProcessBuilder(args);
		Process process = builder.start();

		PumpStreamHandler streams = new PumpStreamHandler(System.out, System.err, System.in);
		streams.setProcessInputStream(process.getOutputStream());
		streams.setProcessOutputStream(process.getInputStream());
		streams.setProcessErrorStream(process.getErrorStream());
		streams.start();

		process.waitFor();
		streams.stop();
	}

}
```

windows 上执行结果如下:

```bat
D:\home\observer.hany\workspace\test>java -jar target\test.jar java -version
java version "1.6.0_45"
Java(TM) SE Runtime Environment (build 1.6.0_45-b06)
Java HotSpot(TM) Client VM (build 20.45-b01, mixed mode, sharing)

D:\home\observer.hany\workspace\test>java -jar target\test.jar mvn -version
Exception in thread "main" java.io.IOException: Cannot run program "mvn": CreateProcess error=2, ?????????
        at java.lang.ProcessBuilder.start(Unknown Source)
        at test.Main.main(Main.java:9)
Caused by: java.io.IOException: CreateProcess error=2, ?????????
        at java.lang.ProcessImpl.create(Native Method)
        at java.lang.ProcessImpl.<init>(Unknown Source)
        at java.lang.ProcessImpl.start(Unknown Source)
        ... 2 more
```

与 `subprocess.call()` 一样, 在 windows 下不能直接执行脚本.

### linux exec 系列函数

在底层实现上,
linux 运行新进程使用的是 `fork()` + [exec*][] 系列函数.
`exec*` 系列函数实现了搜索 `PATH`, 找到脚本解释器等操作, 可以直接执行脚本.

如下示例代码 "subprocess_call.c":

```c
#include <unistd.h>

void subprocess_call(char* const argv[]) {
	pid_t pid = fork();
	if (pid > 0) {
		// parent
		int status;
		waitpid(pid, &status, 0);
	} else {
		// child
		execvp(argv[0], argv);
	}
}

int main(int argc, char* argv[]) {
	subprocess_call(argv + 1);
	return 0;
}
```

运行结果如下:

```sh
observer.hany@ali-59375nm:~/tmp$ ./subprocess_call mvn -version
Apache Maven 3.0.5 (r01de14724cdef164cd33c7c8c2fe155faf9602da; 2013-02-19 21:51:28+0800)
Maven home: /opt/apache-maven-3.0.5
Java version: 1.7.0_40, vendor: Oracle Corporation
Java home: /opt/jdk1.7.0_40/jre
Default locale: zh_CN, platform encoding: UTF-8
OS name: "linux", version: "3.5.0-45-generic", arch: "i386", family: "unix"
```

### windows CreateProcess 函数

windows 下运行新进程使用的是 [CreateProcess][] 函数,
函数参数必须指定二进制可执行文件, 不能直接执行脚本.
python `subprocess.call()` 函数的 executable 参数与 CreateProcess 一致,
如果没有指定 executable, 则从命令行参数第一个 token 查找二进制可执行文件.

在 `cmd` 命令解释器下调用脚本时, 
搜索 `PATH`, 找到脚本解释器等这些事都是由 `cmd` 完成的,
操作系统没有提供完成类似功能的 API.

为了查看 java 启动外部进程的命令行参数, 
增加调试参数使外部进程暂停:

```bat
D:\home\observer.hany\workspace\test>java -jar target\test.jar java -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000 -version
Listening for transport dt_socket at address: 8000
```

使用 [procexp][] 看到 ProcessBuilder 启动进程的命令行为:

```bat
"java" -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000 -version
```

java 的实现应该跟 python 是类似的,
使用命令名 `java` 作为命令行第一个 token, 并且加了引号.
但 java (截止到 jdk6) 不支持设置 executable.

## windows 上命令行转换和 ProcessBuilder bug

windows 和 linux 还有一个差别, 
linux 使用字符串列表作为进程参数, 
shell 将命令行解析成字符串列表, 再启动进程.
而 windows 直接将整个命令行作为一个字符串传递给应用程序,
应用程序自己完成解析.

C 语言规范定义了 main 函数接受一个字符串数组参数,
windows 下实际是由程序入口函数完成解析, 再调用 C 的 main 函数.
应用也可以手动调用解析函数, 解析规则与 cmd 执行命令行的解析规则一致.
有些 windows 程序不按常规方式解析命令行, 
而直接使用整个命令行字符串进行操作, 如 echo, explorer, (notepad?).

使用字符串列表传递参数更结构化, 更清晰和方便,
所以 python, java 等语言都使用字符串列表作为进程参数.
这些语言在 windows 上的实现通常是由入口函数解析命令行得到参数列表,
启动子进程时 (如 subprocess.call() 或 ProcessBuilder) 
再将参数列表转成一个命令行字符串.

测试了一下发现 jdk6 在 windows 上将字符串列表转成命令行时还有 bug .
如执行 jvm 的命令行如下:

```bat
java -jar target\test.jar cmd /c pause "\"a b\""
```

jvm 调用 windows 命令行解析函数后应该得到以下参数:

```python
["cmd", "/c", "pause", '"a b"']
```

jvm 使用 ProcessBuilder 启动 cmd 进程时,
应该再将字符串 `'"a b"'` 转义成 cmd 命令行的表示法,
即与启动 jvm 的原命令行等价.
从 [procexp][] 看到 jvm 启动 cmd 的命令行参数是不正确的:

```bat
"cmd" /c pause "a b"
```

而使用 python 的 `subprocess.call()` 完成相同功能:

```bat
python.exe -c "import sys, subprocess; subprocess.call(sys.argv[1:])" cmd /c pause "\"a b\""
```

可以得到正确结果:

```bat
cmd /c pause "\"a b\""
```

[[run-command-in-os/java-process-builder-bug.png]]

## windows 上调用脚本问题

linux 下调用命令和 windows 下调用可执行二进制文件的方式都是统一的.
实现跨平台调用命令, 主要是解决 windows 下调用脚本命令的问题.

### 实现类似 `cmd` 执行命令的逻辑.

这样要使用一些 windows 的特性和函数, 代价比较大, 而且不一定完善.
目前看到的一些程序库都没有这样做.

windows 下 "Win + R" 运行命令也不能执行脚本,
只能在 cmd "shell" 下执行, 或者通过文件关联打开.
(TODO: [ShellExecute][] 是否可以实现通用的命令调用 ?).

### 直接调用 `cmd` 执行命令

文档上有一段说明, 可以使用 `cmd /c` 执行批处理脚本文件,

>To run a batch file, you must start the command interpreter; 
set lpApplicationName to cmd.exe 
and set lpCommandLine to the following arguments: 
/c plus the name of the batch file.

```bat
D:\home\observer.hany\workspace\test>java -jar target\test.jar cmd /c mvn -version
Apache Maven 2.2.1 (r801777; 2009-08-07 03:16:01+0800)
Java version: 1.6.0_45
Java home: D:\opt\jdk1.6.0_45\jre
Default locale: zh_CN, platform encoding: GBK
OS name: "windows xp" version: "5.1" arch: "x86" Family: "windows"
```

`cmd /c` 执行命令时的行为跟在 cmd 命令解释器中执行命令一样.
不只是批处理文件, 所有脚本和二进制文件, 都可以用 `cmd /c` 执行.
甚至可以用 `cmd /c` 作为 windows 下调用外部命令的通用方式,
但是这样也有一些问题.

* `cmd` 是 CLI 程序 (没有 GUI 版), 
GUI 下调用 cmd 可能会产生一个多余的黑框, 即新建控制台.
是否新建控制台可由 CreateProcess 的参数控制.
不同语言与库实现有关, 
python 有, 输入输出全部重定向后依然有.
jdk6 没有.
* 调用二进制文件和其他脚本时增加了一个调用层次

### 执行脚本时指定解释器

脚本不只是批处理文件, 还可能有 python, js 等.
`cmd` 有两层功能, 一是作为批处理文件的解释器,
二是搜索 `PATH` 及找到其他脚本的解释器.

[CreateProcess][] 搜索 `PATH` 时, 只会查找二进制文件, 不会搜索脚本.
如果知道脚本路径, 可以指定解释器调用脚本, 避免 `cmd /c` 的部分缺点.
调用指定路径脚本的场景很罕见, 通常我们都只通过命令名调用命令,
这相当于手动实现了搜索 `PATH` 及找到解释器的功能.

windows 区分 CLI 程序和 GUI 程序,
解释器也有两个版本, 如 "python" 和 "pythonw", "java" 和 "javaw".
手动指定解释器时, 需要开发人员确定需要使用哪个版本的解释器.

有时开发人员也不能知道执行脚本的解释器是哪个, 比如 js 解释器?	

## 跨平台调用命令

实现跨平台调用命令需要针对 windows 平台进行一些特殊处理.
判断操作系统是否 windows 可以检查
`System.getProperty("os.name").toLowerCase(Locale.US)` 
是否包含字符串 `"windows"`.

0. 如果是可执行二进制文件, 直接调用, 不需要特殊处理.
0. 如果知道脚本路径和解释器, 可以指定解释器执行脚本. 
等同于执行二进制文件的方式.
注意 CLI 和 GUI 要用不同的解释器版本.
0. 其他情况, 包括不确定的情况, 通过 `cmd /c` 调用.
GUI 程序可能会产生黑框问题.

最后, 还要确认一下一些特殊参数处理在 windows 上是否正确.

apache "commons-exec" 库提供了启动进程的一些便捷功能和工具类,
简单测试了下到目前为止的最新 "1.2" 版本,
这个库还是有一些问题.

0. 默认的 `PumpStreamHandler` 及 `DefaultExecutor` 
没有复制标准输入, 导致子进程标准输入被关闭.
需要显示设置 `new PumpStreamHandler(System.out, System.err, System.in)`.

0. windows 下直接执行脚本也是有问题的. 
没有很好的处理加 `cmd /c` 的规则.
这个逻辑最好还是留给应用开发者去处理.

所以 java 下最好还是直接使用 ProcessBuilder,
使用 3 方工具库最好 review 一下相关代码逻辑.

[exec*]: http://man7.org/linux/man-pages/man3/execl.3.html
[CreateProcess]: http://msdn.microsoft.com/en-us/library/windows/desktop/ms682425%28v=vs.85%29.aspx
[procexp]: http://technet.microsoft.com/en-us/sysinternals/bb896653.aspx
[ShellExecute]: http://msdn.microsoft.com/en-us/library/windows/desktop/bb762153%28v=vs.85%29.aspx

