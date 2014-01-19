操作系统下运行命令分析
===

## shell 下执行外部命令

运行命令最简便的办法就是将命令所在目录加入 `PATH` 环境变量,
然后在命令行 shell 下输入执行.
外部程序在 shell 下叫做外部命令.
外部命令分为二进制可执行文件 (以下简称二进制) 和脚本两种.
windows 下是 "cmd" 命令解释器, linux 下通常是 "bash" shell.
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

在底层实现上,
linux 运行新进程使用的是 `fork()` + [exec*][] 系列函数.
`exec*` 系列函数自动实现了找到脚本对应的解释器等操作, 可以直接执行脚本.

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

windows 下运行新进程使用的是 [CreateProcess][] 函数,
函数参数必须指定二进制可执行文件, 不能执行脚本.
python `subprocess.call()` 函数的 executable 参数与 CreateProcess 一致,
如果没有指定 executable, 则从命令行参数第一个 token 查找二进制可执行文件.

java 中可以用 `ProcessBuilder` 实现类似的功能.
通常子进程会继承父进程的标准输入输出,
与常规行为不同, `ProcessBuilder` 默认重定向了输入输出,
并且直到 jdk7 才支持设置成继承,
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

windows 和 linux 还有一个差别, 
linux 将命令行解析成一个字符串列表, 再传递给应用程序.
而 windows 直接将整个命令行输入作为一个字符串传递给应用程序,
应用程序自己完成解析.
C 语言规范定义了 main 函数接受一个字符串数组参数,
windows 下实际是由应用程序入口函数完成参数解析, 再调用 C 的 main 函数.
应用也可以手动调用解析函数, 解析规则与 cmd 命令行参数的解析规则一致.
有些 windows 程序不按常规方式解析命令行, 
而直接使用整个命令行字符串进行操作, 如 echo, explorer, (notepad?).
使用字符串列表传递参数更结构化, 更清晰和方便,
所以 python, java 等语言都使用字符串列表作为进程参数.

为了查看 java 启动外部进程的命令行参数, 
增加调试参数使外部进程暂停:

```bat
D:\home\observer.hany\workspace\test>java -jar target\test.jar java -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000 -version
Listening for transport dt_socket at address: 8000
```

使用 [procexp][] 看到进程启动命令行参数为:

```bat
"java" -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000 -version
```

java 的实现应该跟 python 是类似的,
将参数字符串列表转成一个命令行参数, 
使用命令名做为命令行的第一个 token.
但java (截止到 jdk6) 不支持设置 executable.

## windows 上 ProcessBuilder bug

测试了一下发现 jdk6 在 windows 上将字符串列表转成命令行参数时还有 bug .

如执行 jvm 的命令行如下:

```bat
java -jar target\test.jar cmd /c pause "\"a b\""
```

jvm 调用 windows 解析命令行函数后应该得到以下参数:

```python
["cmd", "/c", "pause", '"a b"']
```

jvm 使用 ProcessBuilder 启动 cmd 进程时
应该再将字符串 `'"a b"'` 再转义成 cmd 命令行的表示法,
即与启动 jvm 的原命令行等价.
从 [procexp][] 看到 jvm 启动 cmd 的命令行参数是不正确的:

```bat
"cmd" /c pause "a b"
```

而 python 使用 `subprocess.call()` 完成相同的功能, 可以得到正确的结果.

```bat
python.exe -c "import sys, subprocess; subprocess.call(sys.argv[1:])" cmd /c pause "\"a b\""
```

[[run-command-in-os/java-process-builder-bug.png]]

## windows 上调用脚本问题

[CreateProcess][] 函数不支持直接运行脚本,
在 `cmd` 命令解释器下调用脚本时, 
定位命令文件, 查找脚本解释器等这些事都是由 `cmd` 完成的,
操作系统没有提供完成类似功能的 API.

文档上有一段说明, 可以使用 `cmd /c` 执行批处理脚本文件.

>To run a batch file, you must start the command interpreter; 
set lpApplicationName to cmd.exe 
and set lpCommandLine to the following arguments: 
/c plus the name of the batch file.

开发人员有几种选择:

0. 执行脚本时指定解释器, 即不要直接执行脚本.
	
	脚本不只是批处理文件, 还可能有 python, js 等.
windows 区分 CLI 程序和 GUI 程序,
解释器也有两个版本, 如 "python" 和 "pythonw", "java" 和 "javaw".
手动指定解释器时, 还需要开发人员确定知道需要使用那个版本的解释器.

	但有时开发人员也不能知道解释器是哪个, 比如 js 解释器?	

0. 实现类似 `cmd` 执行脚本的逻辑.

	这样要使用 windows 的一些特性和函数, 代价比较大, 而且不一定完善.
目前看到的一些程序库都没有这样做的.

0. 使用 `cmd` 间接调用脚本.

	`cmd /c` 执行命令时的行为跟在 cmd 命令解释器中执行命令一样.
`cmd` 有两层功能, 一是作为批处理文件的解释器,
二是为其他脚本找到对应的解释器.
不只是批处理文件, 所有脚本和二进制文件, 都可以用 `cmd /c` 执行.


	甚至可以用 `cmd /c` 作为 windows 下调用外部命令的通用方式,
但是这样也有一些问题.

	* `cmd` 是 CLI 程序 (没有 GUI 版), GUI 下调用 cmd 产生一个多余的黑框
(TODO: 重定向输入输出后黑框是否还在 ?)
	* 调用二进制文件和其他脚本增加一个调用层次

使用 `cmd /c` 执行外部脚本:

```bat
D:\home\observer.hany\workspace\test>java -jar target\test.jar cmd /c mvn -version
Apache Maven 2.2.1 (r801777; 2009-08-07 03:16:01+0800)
Java version: 1.6.0_45
Java home: D:\opt\jdk1.6.0_45\jre
Default locale: zh_CN, platform encoding: GBK
OS name: "windows xp" version: "5.1" arch: "x86" Family: "windows"
```

## windows 下执行命令的几个问题

cmd shell 下启动 GUI 程序直接返回,
但批处理脚本中会等待.

start 新开一个窗口执行命令.
GUI 没有命令行窗口, 有无 start 一样, 
但是 `start /WAIT` 可以等待 GUI 程序退出再返回.

cmd 语法, 冒号表示字符串, 
冒号内部可以冒号转义冒号, 即冒号内部两个冒号是一个冒号.
冒号内部也可以使用 `'\"'` 转义冒号, 似乎更清晰点, 避免混淆.
cmd 语法功能有限, 无法表达一些特殊参数, 
比如 `"a > b"` 总是导致重定向.

[exec*]: http://man7.org/linux/man-pages/man3/execl.3.html
[CreateProcess]: http://msdn.microsoft.com/en-us/library/windows/desktop/ms682425%28v=vs.85%29.aspx
[procexp]: http://technet.microsoft.com/en-us/sysinternals/bb896653.aspx

