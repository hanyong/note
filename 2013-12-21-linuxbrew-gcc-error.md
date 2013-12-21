linuxbrew 安装 icu4c 时 gcc 报错排查
===

使用 linuxbrew 安装 icu4c 出现如下错误:

```sh
[admin@v125205215 .linuxbrew]$ brew install icu4c | cat
==> Downloading http://download.icu-project.org/files/icu4c/52.1/icu4c-52_1-src.tgz
Already downloaded: /home/admin/.cache/Homebrew/icu4c-52.1.tgz
==> ./configure --prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1 --disable-samples --disable-tests --enable-static
checking whether to build release libraries... yes
checking whether the C compiler works... no
configure: error: in `/tmp/icu4c-7278/icu/source':
configure: error: C compiler cannot create executables
See `config.log' for more details
/home/admin/local/lib/ruby/2.0.0/open-uri.rb:353:in `open_http': 404 Not Found (OpenURI::HTTPError)
	from /home/admin/local/lib/ruby/2.0.0/open-uri.rb:708:in `buffer_open'
	from /home/admin/local/lib/ruby/2.0.0/open-uri.rb:210:in `block in open_loop'
... ...
```

手动将 brew 下载的包解压, 进入 source 目录执行同样的 configure 命令却没有问题.

```
./configure --prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1 --disable-samples --disable-tests --enable-static
```

brew 报错后 "/tmp/icu4c-7278/" 整个目录也删除了,
**发生错误后为什么不能保留现场给用户排查问题呢?**
为了想办法让 brew 保留报错现场, 
真是费了老大的劲, 用尽各种 HACK 和投机取巧.
排查完问题查看 ruby 进程文件句柄,
看到原来 brew 把日志打在 "$HOME/Library/Logs/Homebrew/icu4c" 下面,
"config.log" 错误日志这里也有一份.
fuck, 害我折腾这么久, 以下是折腾过程.

查看 brew 命令帮助有一条 edit 命令:

```sh
Brewing:
  brew create [URL [--no-fetch]]
  brew edit [FORMULA...]
  open https://github.com/mxcl/homebrew/wiki/Formula-Cookbook
```

执行 `brew edit icu4c` 打开了 icu4c 的安装脚本.
找到下面这段脚本是执行编译安装的地方:

```ruby
  def install
    ENV.universal_binary if build.universal?
    ENV.cxx11 if build.cxx11?

    args = ["--prefix=#{prefix}", "--disable-samples", "--disable-tests", "--enable-static"]
    args << "--with-library-bits=64" if MacOS.prefer_64_bit?
    cd "source" do
      system "./configure", *args
      system "make", "VERBOSE=1"
      system "make", "VERBOSE=1", "install"
    end
  end
```

尝试在 configure 前插入如下代码, 以启动 bash 手动检查测试环境.

```ruby
      puts args
      system "bash"
```

重新安装 icu4c:

```sh
[admin@v125205215 source]$ brew install icu4c
==> Downloading http://download.icu-project.org/files/icu4c/52.1/icu4c-52_1-src.
Already downloaded: /home/admin/.cache/Homebrew/icu4c-52.1.tgz
--prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1
--disable-samples
--disable-tests
--enable-static
==> bash
```

脚本执行到 bash 命令, 但没看到正常的命令行.
在另一个终端查到 bash 命令的 pid,
发现是 bash 输出被重定向到管道了.

```sh
[observer.hany@v125205215 ~]$ pschain -C bash f
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss     2:00 init [3]                               
 1233 ?        Ss     3:32 /usr/sbin/sshd
26490 ?        Ss     0:00  \_ sshd: observer.hany [priv]
26492 ?        S      0:02  |   \_ sshd: observer.hany@pts/1
26493 pts/1    Ss     0:00  |       \_ -bash
 8310 pts/1    S      0:00  |           \_ su admin
 8311 pts/1    S      0:00  |               \_ bash
22570 pts/1    Sl+    0:00  |                   \_ ruby -W0 /home/admin/.linuxbr
22588 pts/1    SNl+   0:00  |                       \_ /home/admin/local/bin/rub
22605 pts/1    SN+    0:00  |                           \_ bash
... ...
[observer.hany@v125205215 ~]$ sudo -u admin ls -l /proc/22605/fd/
[sudo] password for observer.hany: 
总计 0
lrwx------ 1 admin admin 64 12-21 19:41 0 -> /dev/pts/1
l-wx------ 1 admin admin 64 12-21 19:42 1 -> pipe:[108382114]
l-wx------ 1 admin admin 64 12-21 19:42 2 -> pipe:[108382114]
```

在另一个终端手动进入编译目录执行 configure, 仍然执行成功没有报错.

```sh
[admin@v125205215 ~]$ ll /proc/22605/cwd
lrwxrwxrwx 1 admin admin 0 12-21 19:48 /proc/22605/cwd -> /tmp/icu4c-2599/icu/source
[admin@v125205215 ~]$ cd /tmp/icu4c-2599/icu/source
[admin@v125205215 source]$ ./configure --prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1 --disable-samples --disable-tests --enable-static
checking for ICU version numbers... release 52.1, library 52.1, unicode version 6.3
checking build system type... x86_64-unknown-linux-gnu
checking host system type... x86_64-unknown-linux-gnu
... ...
```

bash 的父进程是没有重定向的, 看看能不能不重定向执行 bash, 

```sh
[admin@v125205215 source]$ ll /proc/22588/fd
总计 0
lrwx------ 1 admin admin 64 12-21 19:41 0 -> /dev/pts/1
lrwx------ 1 admin admin 64 12-21 19:53 1 -> /dev/pts/1
lrwx------ 1 admin admin 64 12-21 19:44 2 -> /dev/pts/1
```

直接测试 `system` 函数默认是不重定向的, 没有找到 bash 被重定向的地方.
查看当前终端设备:

```sh
[admin@v125205215 source]$ tty
/dev/pts/1
```

修改 icu4c 脚本直接指定重定向到当前终端.

```ruby
      system "bash >/dev/pts/1 2>&1"
```

再运行 `brew install icu4c`, 这回可以进入 bash 了.
执行 configure, 果然失败了.

```sh
[admin@v125205215 ~]$ brew install icu4c
==> Downloading http://download.icu-project.org/files/icu4c/52.1/icu4c-52_1-src.
Already downloaded: /home/admin/.cache/Homebrew/icu4c-52.1.tgz
--prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1
--disable-samples
--disable-tests
--enable-static
==> bash >/dev/pts/1 2>&1
[admin@v125205215 source]$ ./configure --prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1 --disable-samples --disable-tests --enable-static
checking for ICU version numbers... release 52.1, library 52.1, unicode version 6.3
checking build system type... x86_64-unknown-linux-gnu
checking host system type... x86_64-unknown-linux-gnu
checking whether to build debug libraries... no
checking whether to build release libraries... yes
checking whether the C compiler works... no
configure: error: in `/tmp/icu4c-1582/icu/source':
configure: error: C compiler cannot create executables
See `config.log' for more details
```

从 "config.log" 中找到错误日志如下:

```sh
configure:2913: checking whether the C compiler works
configure:2935: /usr/bin/gcc -Os -w -pipe -march=core2 -msse4 -isystem/home/admin/.linuxbrew/include -L/home/admin/.linuxbrew/lib -Wl,-headerpad_max_install_names conftest.c  >&5
cc1: error: unrecognized command line option "-msse4"
configure:2939: $? = 1
configure:2977: result: no
```

错误原因是不支持 "-msse4" 选项, 应该是目标机器 gcc 版本太低, 
这个选项是 brew 脚本设置环境变量引入的.

```sh
[admin@v125205215 tmp]$ /usr/bin/gcc -Os -w -pipe -march=core2 -msse4 -isystem/home/admin/.linuxbrew/include -L/home/admin/.linuxbrew/lib -Wl,-headerpad_max_install_names a.c
cc1: 错误：无法识别的命令行选项“-msse4”
[admin@v125205215 tmp]$ env | grep msse
CXXFLAGS=-Os -w -pipe -march=core2 -msse4
CFLAGS=-Os -w -pipe -march=core2 -msse4
OBJCFLAGS=-Os -w -pipe -march=core2 -msse4
OBJCXXFLAGS=-Os -w -pipe -march=core2 -msse4
[admin@v125205215 tmp]$ gcc --version
gcc (GCC) 4.1.2 20080704 (Red Hat 4.1.2-51)
Copyright (C) 2006 Free Software Foundation, Inc.
```

安装其他软件包也会报这个错, 这个选项应该是 linuxbrew 基础环境引入的.
搜索 linuxbrew 代码, 找到 "Library/Homebrew/extend/ENV/std.rb" 文件.

```sh
[admin@v125205215 .linuxbrew]$ find Library/ -type f | xargs grep --color msse4
Library/Formula/justniffer.rb:  # 'CXXFLAGS=-O3 -w -pipe -march=core2 -msse4' 'CC=/usr/bin/llvm-gcc'
Library/Formula/justniffer.rb:  # 'CFLAGS=-O3 -w -pipe -march=core2 -msse4' --cache-file=/dev/null--srcdir=.
Library/Formula/python.rb:    # "-msse4" is present.)
Library/Formula/python3.rb:    # "-msse4" is present.)
Library/Homebrew/extend/ENV/std.rb:  DEFAULT_FLAGS = '-march=core2 -msse4'
Library/Homebrew/extend/ENV/std.rb:    remove flags, %r{-msse4(\.\d)?}
Library/Homebrew/os/mac/hardware.rb:    :penryn => '-march=core2 -msse4.1',
```

修改 "std.rb" 文件,

```ruby
  DEFAULT_FLAGS = '-march=core2 -msse4'
```

这行修改为

```ruby
  DEFAULT_FLAGS = '-march=core2'
```

由于 brew 是基于 git 的, 
在 "$HOME/.linuxbrew" 下运行 `git status` 就可以看到我们对相关脚本的修改点.
对 "icu4c.rb" 的修改可以去掉, 再重新安装 icu4c, 终于编译安装成功.

```sh
[admin@v125205215 .linuxbrew]$ git status
# On branch linuxbrew
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#	modified:   Library/Formula/icu4c.rb
#	modified:   Library/Homebrew/extend/ENV/std.rb
#
no changes added to commit (use "git add" and/or "git commit -a")
[admin@v125205215 .linuxbrew]$ git checkout Library/Formula/icu4c.rb
[admin@v125205215 ~]$ brew install icu4c
==> Downloading http://download.icu-project.org/files/icu4c/52.1/icu4c-52_1-src.
Already downloaded: /home/admin/.cache/Homebrew/icu4c-52.1.tgz
==> ./configure --prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1 --disable-samp
==> make VERBOSE=1
==> make VERBOSE=1 install
... ...
```

brew 还能安装 python, ruby 自身, 甚至 gcc 等基础软件,
感觉是个不错的跨平台软件包管理器, 可惜用了讨厌的 ruby.

brew 将每个软件包版本安装到独立文件夹,
使用软链接管理默认使用的软件包, 类似 linux 的 `update-alternatives`.
icu4c 可能跟其他软件包有冲突, 默认没有建立连接.
建立, 取消连接可使用:

```sh
brew link icu4c
brew unlink icu4c
```

