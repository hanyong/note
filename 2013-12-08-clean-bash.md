clean bash
===

我一直觉得 linux shell (sh) 相当恶心,
在结构化和一致性上都做的相当差,
然而仔细思考一下, 发现这确实是操作计算机的 **最简洁** 方式.
当 **大量操作需要被手动重复执行** 时,
简洁确实成了一个第一重要因素.
我建议 bash 应该只用来做 "极其简单" 和 "用完即扔" 的事, 避免不容易理解的特性.
稍微复杂或者需要通用性的场景, 就应该考虑使用 python 或者 java.

本文的目标是梳理一下 bash 知识点,
尽量避开恶心和不一致,
使我们能够 **以一种相对简单、一致的方式来理解和使用 bash**.
同时作为个人学习的一个总结和今后使用 bash 时相关知识点的一个 **速查手册**.

## 什么是 shell

shell 提供用户使用字符串文本与计算机交互的方式.
linux 底层是基于字节的 (C 语言的 char), 更准确的说是使用字节串与计算机交互.
通常一行字符串表示一个命令, 所以叫命令行, 简称 CLI.

linux 区分终端和 shell, 终端提供字符串输入输出功能, 还支持快捷键.
而 shell 是一个终端程序, 是一个命令解释器.
最常见的 shell 就是 bash.
使用命令行登陆 (没有图形桌面) 时, 启动的第一个程序就是 shell,
shell 就像一层壳, 封装了计算机内部功能, 提供对外操作接口, 所以叫做 shell.

shell 的优点:
* 有些命令只有命令行接口, 比如 gcc, java.
* 一些命令需要运行时调配的参数太多, 使用 CLI 添加设置参数方便灵活很多.
* 有些命令的功能, 比如 "grep", "less", "tailf", GUI 没有同样方便的实现.
* shell 可以轻易组合命令实现一些功能, 即最简单的编程方式, GUI 缺乏这种支持.
* shell 命令可以记录到文本文件, 方便传播和自动化重复执行, 叫做 shell 脚本.
* 字符串命令交互界面只需要极低的硬件资源和网络资源, 很容易使用 ssh 远程登录操作服务器.

现在的计算机都有图形桌面操作系统, 
不同的操作 GUI 和 CLI 各有优劣.
最好的办法是把两者结合起来使用.
图形桌面下很容易启动一个终端窗口, 
如 ubuntu 下的 gnome-terminal, 
结合图形桌面和 bash 共同操作计算机.

## bash 和 sh

bash 是 sh 的扩展, 做了一些增强和接近 "C 语言" 的扩展，因此更加好用.
所有的 linux 机器都安装了 bash,
我们总是在使用增强的 bash,
我不想花精力去区分哪些功能是 bash 增强哪些是原始 sh.
不同版本的 bash 功能支持可能还会有所差异,
确定一个功能是否支持和行为方式的最好办法, 就是亲自测试一下.
再次强调, 如果需要通用, 请考虑 java.
我用的操作系统是 "Ubuntu 12.04 LTS", bash 版本是 "4.2.25".

## 为什么说 bash 最简洁

一条命令是一个字符串列表, 执行一条命令的 bash 语法如下:

```sh
observer.hany@ali-59375nm:~/tmp$ ll a.txt
-rw-r--r-- 1 observer.hany han 4735 12月 16 18:18 a.txt
```

而即使模仿最简洁的 clojure, 也要写成:

```clojure
(ll "a.txt")
```

bash 比 clojure 还简洁.
bash 中字符串是一等公民, 简单字符串不需要引号.
每行输入都是命令调用, 不需要圆括号.
上述写法在 bash 种也合法,
但是圆括号表示子 shell, 将在一个新的 bash 子进程中执行.
bash 的重定向, 管道, 命令行扩展等, 使 bash 可以用最简洁的方式实现特定操作.

## 当前目录

一个进程有一个当前目录, 使用相对路径访问目录和文件时, 即是相对当前目录.
bash 下通常会提示当前目录 (完整路径或最后一层路径).
使用 `pwd` 命令可以查看当前目录,
也可以使用 `PWD` 环境变量引用当前目录.
`cd` 命令切换当前目录, 无任何参数时切换到用户 HOME 目录,
`cd -` 切换到上一次当前目录, 连续使用 `cd -` 则在两个目录间切换.

```sh
observer.hany@ali-59375nm:~/workspace/note.wiki$ pwd
/home/observer.hany/workspace/note.wiki
observer.hany@ali-59375nm:~/workspace/note.wiki$ echo $PWD
/home/observer.hany/workspace/note.wiki
observer.hany@ali-59375nm:~/workspace/note.wiki$ cd
observer.hany@ali-59375nm:~$ cd -
/home/observer.hany/workspace/note.wiki
observer.hany@ali-59375nm:~/workspace/note.wiki$ 
```

子进程启动时继承父进程的当前目录.
许多命令的默认操作目录即为当前目录, 如 `ls`.

```sh
observer.hany@ali-59375nm:~/workspace/note.wiki$ ls
2013-11-17-use-wx-make-gui.md  2013-12-10-git-svn.md    home.md    scala
2013-12-08-clean-bash.md       2013-12-19-bash-misc.md  README.md
```

* 进程启动后可能会意外改变当前目录 (如 windows 下打开文件对话框),
因此应该只在程序最初启动时, 如处理文件路径参数时, 使用相对路径,
程序运行时应该总是使用绝对路径, 
可以把程序启动时的当前目录保存下来, 用来定位相对于启动目录的相对路径.

* 一个 bash 所在的当前目录可能被其他进程意外删掉,
这时一些程序可能不能正常工作.

```sh
observer.hany@ali-59375nm:~/tmp/aaa$ pwd
/home/observer.hany/tmp/aaa
observer.hany@ali-59375nm:~/tmp/aaa$ ls
observer.hany@ali-59375nm:~/tmp/aaa$ ls $PWD
ls: 无法访问/home/observer.hany/tmp/aaa: 没有那个文件或目录
observer.hany@ali-59375nm:~/tmp/aaa$ java -version
Error occurred during initialization of VM
java.lang.Error: Properties init: Could not determine current working directory.
	at java.lang.System.initProperties(Native Method)
	at java.lang.System.initializeSystemClass(System.java:1118)
```

如果其他进程又重新创建了删掉的目录:

```sh
observer.hany@ali-59375nm:~/tmp$ mkdir aaa
observer.hany@ali-59375nm:~/tmp$ touch aaa/a.txt
```

子进程可能还是无法正常获取当前目录. 
"/proc/<pid>/cwd" 是当前目录的软连接, 显示已被删除.

```sh
observer.hany@ali-59375nm:~/tmp/aaa$ ls $PWD
a.txt
observer.hany@ali-59375nm:~/tmp/aaa$ ls
observer.hany@ali-59375nm:~/tmp/aaa$ java -version
Error occurred during initialization of VM
java.lang.Error: Properties init: Could not determine current working directory.
	at java.lang.System.initProperties(Native Method)
	at java.lang.System.initializeSystemClass(System.java:1118)

observer.hany@ali-59375nm:~/tmp/aaa$ ll -d /proc/$$/cwd
lrwxrwxrwx 1 observer.hany han 0 12月 19 01:27 /proc/3915/cwd -> /home/observer.hany/tmp/aaa (deleted)
```

使用 `cd .` 可以切换到重新建立的当前目录.

```sh
observer.hany@ali-59375nm:~/tmp/aaa$ cd .
observer.hany@ali-59375nm:~/tmp/aaa$ ls
a.txt
observer.hany@ali-59375nm:~/tmp/aaa$ ll -d /proc/$$/cwd
lrwxrwxrwx 1 observer.hany han 0 12月 19 01:27 /proc/3915/cwd -> /home/observer.hany/tmp/aaa
```

当前目录不存在时使用 `cd .` 会报错.

```sh
observer.hany@ali-59375nm:~/tmp/aaa$ cd .
cd: 获取当前目录时出错: getcwd: 无法访问父目录: 没有那个文件或目录
observer.hany@ali-59375nm:~/tmp/aaa/.$ 
```

## type 和 help

bash 命令分为内部命令, 外部命令, 关键字等类型, 
使用 `type` 命令可以查看一个符号 (Symbol) 是什么类型,
`type` 本身是一个内部命令.

```sh
observer.hany@ali-59375nm:~/tmp$ type ls
ls 是 `ls --color=auto' 的别名
observer.hany@ali-59375nm:~/tmp$ type ll
ll 是 `ls -Al' 的别名
observer.hany@ali-59375nm:~/tmp$ type java
java 是 /opt/jdk1.7.0_40/bin/java
observer.hany@ali-59375nm:~/tmp$ type '!'
! 是 shell 关键字
observer.hany@ali-59375nm:~/tmp$ type test
test 是 shell 内嵌
observer.hany@ali-59375nm:~/tmp$ type [
[ 是 shell 内嵌
observer.hany@ali-59375nm:~/tmp$ type '[['
[[ 是 shell 关键字
observer.hany@ali-59375nm:~/tmp$ type type
type 是 shell 内嵌
```

还有一些有特殊含义的记号不能用 `type` 命令查看.
如表示 C 语言风格数值计算的 "((" 和表示语句结束的 ";".

```sh
observer.hany@ali-59375nm:~/tmp$ ((xx = 100))
observer.hany@ali-59375nm:~/tmp$ echo $xx
100
observer.hany@ali-59375nm:~/tmp$ ((xx = 3 + 8))
observer.hany@ali-59375nm:~/tmp$ echo $xx
11
observer.hany@ali-59375nm:~/tmp$ for (( i = 0; i < 3; ++i )); do
> echo $i
> done
0
1
2
observer.hany@ali-59375nm:~/tmp$ type '(('
bash: type: ((: 未找到
observer.hany@ali-59375nm:~/tmp$ type ';'
bash: type: ;: 未找到
```

使用 `help` 命令可以查看内部命令或关键字的帮助文档,
按照提示, 使用 `man` 或 `man -k` 可以查看或者搜索外部命令的相关文档.

```sh
observer.hany@ali-59375nm:~/tmp$ help type
type: type [-afptP] 名称 [名称 ...]
    显示命令类型的信息。
    
    对于每一个 NAME 名称，指示如果作为命令它将如何被解释。
    
    选项：
... ...

observer.hany@ali-59375nm:~/tmp$ help '[['
[[ ... ]]: [[ 表达式 ]]
    执行条件命令。
    
    根据条件表达式 EXPRESSION 的估值返回状态0或1。表达式按照
    `test' 内嵌的相同条件组成，或者可以有下列操作符连接而成：
... ...

observer.hany@ali-59375nm:~/tmp$ help java
bash: help: 没有与 `java' 匹配的帮助主题。尝试 `help help' 或者 `man -k java' 或者 `info java'。
observer.hany@ali-59375nm:~/tmp$ man -k java
ant (1)              - a Java based make tool.
appletviewer (1)     - The Java Applet Viewer
c++filt (1)          - Demangle C++ and Java symbols.
idlj (1)             - The IDL-to-Java Compiler
java (1)             - the Java application launcher
javac (1)            - Java programming language compiler
... ...
```

## 字符串

与 C, java 等其他常规语言不一样,
在其他语言中关键字和变量是一等公民, 可以直接写, 字符串则要用引号括起来.
在 bash 中关键字和字符串是一等公民, 可以直接写, 变量则要用 "$" 表示.

bash 中有特殊含义的符号也要用引号括起来, 或者使用 "\" 转义.

```sh
observer.hany@ali-59375nm:~/tmp$ echo *.txt
a.txt b.txt
observer.hany@ali-59375nm:~/tmp$ echo "*.txt"
*.txt
observer.hany@ali-59375nm:~/tmp$ echo \*.txt
*.txt
observer.hany@ali-59375nm:~/tmp$ echo "&<>;"
&<>;
```

如果特殊符号已经在引号中, 就不需要用 "\" 转义.
这时 "\" 会被当作原始字符串直接打印出来,
但是双引号本身却可以被转义.

```sh
observer.hany@ali-59375nm:~/tmp$ echo "\*.txt"
\*.txt
observer.hany@ali-59375nm:~/tmp$ echo "a\nb"
a\nb
observer.hany@ali-59375nm:~/tmp$ echo "\""
"
observer.hany@ali-59375nm:~/tmp$ echo "\;"
\;
observer.hany@ali-59375nm:~/tmp$ echo "\'"
\'
```

字符串也可以用单引号括起来,
与双引号的区别在于,
双引号禁止了特殊符号含义和绝大多数命令行扩展,
但是还保留了变量扩展和命令替换扩展.
单引号则禁用一些扩展和转义,
相当于 python 中的原始字符串, 连对单引号和续行符的转义也禁用了.

```sh
observer.hany@ali-59375nm:~/tmp$ echo "$HOME"
/home/observer.hany
observer.hany@ali-59375nm:~/tmp$ echo "$(seq 3)"
1
2
3
observer.hany@ali-59375nm:~/tmp$ echo '$HOME'
$HOME
observer.hany@ali-59375nm:~/tmp$ echo '$(seq 3)'
$(seq 3)
observer.hany@ali-59375nm:~/tmp$ echo '\'
\
observer.hany@ali-59375nm:~/tmp$ echo 'a\
> b'
a\
b
```

双引号保留变量扩展的特点, 
使我们可以很直观的把变量和其他字符串拼在一起,
得到一个目标字符串, 这也是最简单的字符串模板语法.
变量后面直接拼字符串时, 为了区分变量名的终点, 必须使用 "${HOME}" 这样的语法.

```sh
observer.hany@ali-59375nm:~/tmp$ echo "$HOME"
/home/observer.hany
observer.hany@ali-59375nm:~/tmp$ echo "${JAVA_HOME}xx"
/opt/jdk1.7.0_40xx
```

单引号中可以直接使用双引号, 双引号中可以直接单引号.

```sh
observer.hany@ali-59375nm:~/tmp$ echo "'abc'"
'abc'
observer.hany@ali-59375nm:~/tmp$ echo '"def"'
"def"
```

linux 终端是面向字节的, 因此还可以直接输入 '\x01', '\x02' 等字节,
方法是先按一次 "Ctrl + V" 快捷键, 
下一次 "Ctrl + [A-Z]" 就会输入 "chr(1)" 至 "chr(26)" 的字节.
为了更加可视化, 
可以用 "`python -c 'import sys; print sys.argv'`" 打印出具体的输入参数.

```sh
observer.hany@ali-59375nm:~/tmp$ python -c 'import sys; print sys.argv' a^A^Zb
['-c', 'a\x01\x1ab']
```

输入的字节会在终端上会以可视化形式显示为 "^A", "^B", 
有时我们也直接把这些字节叫做 "Ctrl-A", "Ctrl-B".

**最佳实践** bash 双引号字符串的转义规则很奇怪,
不要在双引号字符串中使用专业字符, 
需要特殊字节最好使用 C 语言风格的字符串.
bash 还支持按 C 语言的风格来使用字符串, 
语法是 "$" 加一对单引号, 如 $'a\nb'.
**注意** 是字符串参数在 linux 底层是以 "char*" 传递, 
以 "\x00" 为字符串结束符, 所以 "\x00" 后面的内容都会被丢掉.

```sh
observer.hobserver.hany@ali-59375nm:~/tmp$ python -c 'import sys; print sys.argv' $'a\x01\x02b'
['-c', 'a\x01\x02b']
observer.hany@ali-59375nm:~/tmp$ python -c 'import sys; print sys.argv' $'abc\x00def'
['-c', 'abc']
any@ali-59375nm:~/tmp$ python -c 'import sys; print sys.argv' $'a\x01\x02b'
['-c', 'a\x01\x02b']
observer.hany@ali-59375nm:~/tmp$ python -c 'import sys; print sys.argv' $'abc\x00def'
['-c', 'abc']
```

**字符串拼接**, bash 字符串拼接很简单, 直接把两个字符串写挨到一起, 
中间不要留任何空白, 就可以拼成一个更长的字符串.
各种字符串表示法可以交替使用拼接起来.
缺点就是单引号字符处和双引号字符串拼接点可能会看的很晕.

```sh
observer.hany@ali-59375nm:~/tmp$ echo "'abc'"'"def"'$'a\tb'"${HOME}"
'abc'"def"a	b/home/observer.hany
```

## 内部命令与外部命令

bash 命令分为内部命令与外部命令.
两者的调用方式一致,
但内部命令是在 bash 进程内直接执行,
外部命令是启动一个子进程运行外部程序.
理论上内部命令没有新建进程的代码, 会快很多.
子进程默认会继承父进程的设置 (环境变量和 limit 等),
但是子进程启动后, 子进程与父进程的设置完全独立,
子进程无法修改父进程的设置, 只有内部命令才能修改 shell 本进程的设置.

使用 bash 内部命令修改进程设置, 再启动子进程, 
子进程默认继承了父进程 bash 的设置, 
间接实现了使用 bash 定义程序运行设置.

直接运行 shell 脚本时会启动一个 bash 子进程运行脚本.
要将 shell 脚本的设置命令应用到当前 bash 进程,
应该会 source 命令导入脚本, 
source 是一个内部命令, 表示直接在当前进程中运行指定脚本文件中的命令.

一些子进程想要将一些设置应用到 shell, 
因为子进程无法修改父进程设置, 只能输出一段脚本,
使用 eval 在 bash 进程中执行脚本内容.

```sh
observer.hany@ali-59375nm:~$ eval "$(ssh-agent)"
Agent pid 6103
observer.hany@ali-59375nm:~$ env | grep SSH
SSH_AGENT_PID=6103
SSH_AUTH_SOCK=/tmp/ssh-HhKrNlTD6102/agent.6102
```

启动 `ssh-agent` 的更好做法是将输出脚本保存到一个文件,
每次登陆后 `source` 文件.

```sh
observer.hany@ali-59375nm:~$ ssh-agent > ~/.ssh/ssh-agent.sh
observer.hany@ali-59375nm:~$ source ~/.ssh/ssh-agent.sh 
Agent pid 6112
```

## eval 与非登陆 ssh 命令

eval 命令在当前 bash 进程中执行一段字符串表示的 shell 脚本.

eval 接受一个 bash 源码字符串参数, 对 bash 源码进行解析执行.
为了方便书写, eval 可以接受一个参数列表, 
但这个参数列表不是 eval 执行的命令的参数列表,

0. bash 对 eval 命令的参数列表进行解析
0. eval 把解析后的参数列表用空格连成一个字符串
0. eval 对字符串进行解析执行, 可能得到新的字符串列表

如使用 eval 输出一个双引号的命令如下:

```sh
observer.hany@ali-59375nm:~$ eval echo \' '"' \'
 " 
```

第一次解析之后得到 

```python
["echo", "'", '"', "'"]
```

空格连起来后 eval 执行的源码是 

```
r"""echo ' " '"""
```

再次解析得到 

```python
["echo", ' " ']
```

所以双引号前后还多了一个空格.
执行了两次 bash 命令行解析.

使用非登陆 ssh 在远程机器上执行命令时过程与 eval 相同,
会进程两次 bash 解析,
本机执行一次, 评出一个 bash 源码字符串, 再在远程机器上执行 bash 解析.

为了避免第一次解析, 直观输入要执行的源码, 可以用单引号把参数引起来.

```sh
observer.hany@ali-59375nm:~$ echo "$HOME"
/home/observer.hany
observer.hany@ali-59375nm:~$ ssh admin@localhost echo '"$HOME"'
admin@localhost's password: 
/home/admin
```

## 启动进程

通常一行字符串表示一条命令,
被 bash 解析后拆分成一个字符串列表.
第一个元素表示命令, 其他所有元素表示命令参数.

bash 最重要的功能之一就是启动一个进程, 即调用外部命令.
linux 下进程间就是使用字符串列表来传递参数,
对应 C 语言 main 函数如下:

```c
int main(int argc, char** argv) {
	return 0;
}
```

程序返回值一个整数, 表示命令是否执行成功, bash 可以拿到这个值.

为什么说 bash 是最简洁的编程方式呢?
调用一条命令的 bash 语法是:

```sh
ls -l a.txt
```

而即使模拟最简单的 clojure 语法也要写成 (只是模拟, clojure 不支持这样调 shell 命令):

```clojure
("ls" "-l" "a.txt")
```

在 bash 里字符串和进程是一等公民.
直接写出来就是字符串, 简单字符串不用加引号,
调用命令也不用加括号.

上述写法在 bash 里也是合法的,
但含义不一样, 圆括号表示子 shell, 子 shell 包含多条命令时会新起一个进程.
而简单字符串加不加引号都可以.

```sh
observer.hany@ali-59375nm:~/tmp$ ("ls" "-l" "a.txt")
-rw-r--r-- 1 observer.hany han 4735 12月 16 18:18 a.txt
```

使用 python 启动一个进程的代码与 bash 很接近, 略微麻烦一点.

```python
import subprocess
subprocess.call(["ls", "-l", "a.txt"])
```

## 变量

## 命令行扩展

## 重定向

## 控制结构

## 后台运行

## 管道与 xargs

