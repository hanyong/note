gollum 安装笔记
===

gollum 是个很棒的 wiki (文档服务器), 支持 github markdown.
可惜用了 ruby 语言, 一直很讨厌 ruby,
不过 gitlab 的 wiki 实在太烂, 还是决定自己搭一下 gollum.

**快速安装** 可参考如下命令 (需要 sudo 权限, 安装到系统目录):

```sh
sudo yum install -b current ruby
sudo gem sources --remove https://rubygems.org/
sudo gem sources -a http://ruby.taobao.org/

wget http://download.icu-project.org/files/icu4c/52.1/icu4c-52_1-RHEL6-x64.tgz
tar xf icu4c-52_1-RHEL6-x64.tgz
sudo rsync -av --itemize-changes usr/local/ /usr/

sudo gem install gollum
```

个人目录 "绿色" 安装笔记如下.

首先打开 github gollum 主页 (https://github.com/gollum/gollum),
了解安装方法.
看了一下最新版 tag 是 "v2.5.2", 
拉取最新 tag 到 master 的提交记录到本地,
简单看了下只增加了几次提交, 改动不大.

查看系统要求如下:

>## SYSTEM REQUIREMENTS

>- Python 2.5+ (2.7.3 recommended)
- Ruby 1.8.7+ (1.9.3 recommended)
- Unix like operating system (OS X, Ubuntu, Debian, and more)
- Will not work on Windows (because of [grit](https://github.com/github/grit))

目标机器是版本较旧的 redhat, 
yum 仓库上没有高版本的 python.
python 是可以 "绿色安装" 的, ruby 应该也可以,
创建 `~/local` 文件夹, 打算将所需软件都安装到这下面, 不影响原有系统.
将 `~/local/bin` 添加到 PATH 前面, 以使用新安装的软件.
python 很容易从源码安装, ruby 也看看是否可以简单的从源码安装.
创建 `~/build` 文件夹, 下载编译相关源码.

从源码安装 python:

```sh
wget http://www.pythttp://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgzhon.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar xf Python-2.7.6.tgz
cd Python-2.7.6
./configure --prefix ~/local/
make
make install
```

部分模块未编译成功, 暂时忽略.

```sh
INFO: Can't locate Tcl/Tk libs and/or headers

Python build finished, but the necessary bits to build these modules were not found:
_tkinter           bsddb185           dl              
imageop            sunaudiodev                        
To find the necessary bits, look in setup.py in detect_modules() for the module's name.
```

看一下安装了哪些文件. 

```sh
[admin@v125205215 ruby-2.0.0-p353]$ ls ~/local/bin
2to3  pydoc   python2    python2.7-config  python-config
idle  python  python2.7  python2-config    smtpd.py
```

安装完成后 python 就可以启动了.

```sh
[admin@v125205215 ruby-2.0.0-p353]$ which python
~/local/bin/python
[admin@v125205215 ruby-2.0.0-p353]$ python
Python 2.7.6 (default, Dec 21 2013, 12:44:04) 
[GCC 4.1.2 20080704 (Red Hat 4.1.2-51)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

从源码安装 ruby (ruby 源码可以从[淘宝镜像](http://ruby.taobao.org/)下载):

```sh
wget http://ruby.taobao.org/mirrors/ruby/ruby-2.0.0-p353.tar.gz
cd ruby-2.0.0-p353
./configure --prefix ~/local/
make
make install
```

ruby 编译安装很慢, 安装完成后可以看一下新增的安装文件,
`ruby`, `irb`, `gem`, `rake`, `rdoc` 这些命令都有了.

```sh
[admin@v125205215 ruby-2.0.0-p353]$ ls ~/local/bin/
2to3  idle   python     python2.7-config  rake  ruby
erb   irb    python2    python2-config    rdoc  smtpd.py
gem   pydoc  python2.7  python-config     ri    testrb
[admin@v125205215 ruby-2.0.0-p353]$ which -a ruby
~/local/bin/ruby
/usr/bin/ruby
[admin@v125205215 ruby-2.0.0-p353]$ which -a irb
~/local/bin/irb
[admin@v125205215 ruby-2.0.0-p353]$ irb
irb(main):001:0> 
```

按淘宝镜像提示更新 gem 源.

```sh
[admin@v125205215 ruby-2.0.0-p353]$ gem sources -l
*** CURRENT SOURCES ***

https://rubygems.org/
[admin@v125205215 ruby-2.0.0-p353]$ gem sources --remove https://rubygems.org/
https://rubygems.org/ removed from sources
[admin@v125205215 ruby-2.0.0-p353]$ gem sources -a http://ruby.taobao.org/
http://ruby.taobao.org/ added to sources
[admin@v125205215 ruby-2.0.0-p353]$ gem sources -l
*** CURRENT SOURCES ***

http://ruby.taobao.org/
```

gollum 安装说明如下:

>## INSTALLATION

>The best way to install Gollum is with RubyGems:

>```bash
$ [sudo] gem install gollum
>```

按文档安装 gollum 出现如下错误:

```sh
[admin@v125205215 ruby-2.0.0-p353]$ gem install gollum
Fetching: charlock_holmes-0.6.9.4.gem (100%)
Building native extensions.  This could take a while...
ERROR:  Error installing gollum:
	ERROR: Failed to build gem native extension.

    /home/admin/local/bin/ruby extconf.rb
checking for main() in -licui18n... no
... ...

***************************************************************************************
*********** icu required (brew install icu4c or apt-get install libicu-dev) ***********
***************************************************************************************
```

原因是缺少 `icu4c` 库.

目标机器不是 ubuntu 系统, yum 上没有 icu4c, 
从 [icu 官网](http://site.icu-project.org/) 下载 RHEL6 二进制包, 
经测试可以使用.
拷贝 icu4c 二进制文件到 `~/local/`, 设置 `LD_LIBRARY_PATH` 环境变量.

```sh
wget http://download.icu-project.org/files/icu4c/52.1/icu4c-52_1-RHEL6-x64.tgz
tar xf icu4c-52_1-RHEL6-x64.tgz
rsync -av --itemize-changes usr/local/ ~/local/
export LD_LIBRARY_PATH=$HOME/local/lib:$LD_LIBRARY_PATH
```

icu4c 二进制文件可以使用, 但是获取编译参数要添加 `--detect-prefix` 才行.

```sh
[admin@v125205215 build]$ uconv --version
uconv v2.1  ICU 52.1
[admin@v125205215 build]$ icu-config --cflags
### icu-config: Can't find /usr/local/lib/libicuuc.so - ICU prefix is wrong.
###      Try the --prefix= option 
###      or --detect-prefix
###      (If you want to disable this check, use  the --noverify option)
### icu-config: Exitting.
[admin@v125205215 build]$ icu-config --detect-prefix --cflags
## Using --prefix=/home/admin/local/bin//..
-O3 -std=c99 -Wall -pedantic -Wshadow -Wpointer-arith -Wmissing-prototypes -Wwrite-strings    
[admin@v125205215 build]$ icu-config --detect-prefix --cppflags
## Using --prefix=/home/admin/local/bin//..
-D_REENTRANT  -DU_HAVE_ELF_H=1 -DU_HAVE_ATOMIC=0   -I/home/admin/local/bin//../include 
```

注意这里的 `--cppflags` 是指预处理器, 不是指 "C++", "C++" 是 "--cxxflags".

再次安装 gollum 还是报错.

```sh
[admin@v125205215 build]$ gem install gollum
Building native extensions.  This could take a while...
ERROR:  Error installing gollum:
	ERROR: Failed to build gem native extension.

    /home/admin/local/bin/ruby extconf.rb
checking for main() in -licui18n... yes
checking for main() in -licui18n... yes
checking for unicode/ucnv.h... no


***************************************************************************************
*********** icu required (brew install icu4c or apt-get install libicu-dev) ***********
***************************************************************************************
*** extconf.rb failed ***
```

找一下 extconf.rb 文件在哪里?

```sh
[admin@v125205215 build]$ find ~/local/ -name extconf.rb
/home/admin/local/lib/ruby/gems/2.0.0/gems/charlock_holmes-0.6.9.4/ext/charlock_holmes/extconf.rb
```

打开文件, 搜一下 "icu", 找到如下代码:

```ruby
##
# ICU dependency
#

dir_config 'icu'

# detect homebrew installs
if !have_library 'icui18n'
  base = if !`which brew`.empty?
    `brew --prefix`.strip
  elsif File.exists?("/usr/local/Cellar/icu4c")
    '/usr/local/Cellar'
  end

  if base and icu4c = Dir[File.join(base, 'Cellar/icu4c/*')].sort.last
    $INCFLAGS << " -I#{icu4c}/include "
    $LDFLAGS  << " -L#{icu4c}/lib "
  end
end

unless have_library 'icui18n' and have_header 'unicode/ucnv.h'
  STDERR.puts "\n\n"
  STDERR.puts "***************************************************************************************"
  STDERR.puts "*********** icu required (brew install icu4c or apt-get install libicu-dev) ***********"
  STDERR.puts "***************************************************************************************"
  exit(1)
end
```

只支持 "icu4c" 安装到系统路径或 "/usr/local/Cellar/icu4c", what's a fuck.

找找 "homebrew" 有没有 linux 版本.
上 [homebrew 官网](http://brew.sh/) 看了下，
还是挺酷的一个软件, 基于 git 和 ruby, 主要为 Apple (OS X) 设计.
github 上有一个 [linuxbrew](https://github.com/Homebrew/linuxbrew) 分支.

按提示安装 linuxbrew.

```sh
git clone https://github.com/Homebrew/linuxbrew.git ~/.linuxbrew
export PATH="$HOME/.linuxbrew/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.linuxbrew/lib:$LD_LIBRARY_PATH"
```

安装 icu4c 报错:

```sh
[admin@v125205215 ~]$ brew install icu4c
==> Downloading http://download.icu-project.org/files/icu4c/52.1/icu4c-52_1-src.
######################################################################## 100.0%
==> ./configure --prefix=/home/admin/.linuxbrew/Cellar/icu4c/52.1 --disable-samp
checking whether to build release libraries... yes
checking whether the C compiler works... no
configure: error: in `/tmp/icu4c-8643/icu/source':
configure: error: C compiler cannot create executables
See `config.log' for more details

READ THIS: https://github.com/mxcl/homebrew/wiki/troubleshooting

/home/admin/local/lib/ruby/2.0.0/open-uri.rb:353:in `open_http': 404 Not Found (OpenURI::HTTPError)
	from /home/admin/local/lib/ruby/2.0.0/open-uri.rb:708:in `buffer_open'
... ...
```

本身对 linuxbrew 不了解, 又是试验版本, 感觉存在大把问题, 
费了半天劲没能解决问题, 放弃 linuxbrew. 

直接将解压的二进制文件安装到 "/usr/local/Cellar/icu4c".
因为 ruby 脚本在系统路径找不到 icu4c 库才会找 homebrew 路径,
同时把 `~/local/` 下的 icu4c 相关文件删掉.

```sh
sudo mkdir -p /usr/local/Cellar/icu4c
cd ~/build
sudo rsync -av usr/local/ /usr/local/Cellar/icu4c/52.1/
cd ~/build/usr
find -type f | (cd; xargs rm)
```

再次安装还是失败, 忽略一个问题, 
linuxbrew 的 `brew --prefix` 是 "/home/admin/.linuxbrew", 
不是 "/usr/local/Cellar".
linuxbrew 相关设置 (PATH, LD_LIBRARY_PATH) 也清掉.

放大招直接将 icu4c 二进制文件安装到系统路径 "/usr/local" 下,
再次运行 `gem install gollum` 安装,
经过较长时间的等待后安装成功,
"gollum" 启动脚本安装到 "~/local/bin/gollum".
设置 "`LD_LIBRARY_PATH=/usr/local/lib`" 后运行 `gollum` 成功,
不设置会加载不到 icu4c 动态库.
貌似也不用额外安装文档格式模块, markdown 等很多格式都默认支持了.

使用 linuxbrew 可按如下步骤安装.

```sh
sudo yum install -b current ruby

## fix git ssl error
git config --global http.sslVerify false
#git clone https://github.com/Homebrew/linuxbrew.git ~/.linuxbrew
git clone --depth 1 https://github.com/Homebrew/linuxbrew.git ~/.linuxbrew
## add these to ~/.bash_profile
cat >> ~/.bash_profile <<'EOF'
export PATH="$HOME/.linuxbrew/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.linuxbrew/lib:$LD_LIBRARY_PATH"
EOF
export PATH="$HOME/.linuxbrew/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.linuxbrew/lib:$LD_LIBRARY_PATH"
## fix old gcc not support "-msse4", see [[2013-12-21-linuxbrew-gcc-error]]
sed -r -i 's#^(\s*DEFAULT_FLAGS\b.*?)-msse4(.*)$#\1\2#' ~/.linuxbrew/Library/Homebrew/extend/ENV/std.rb
## use taobao ruby mirror
sed -i "s#url '"'http://cache.ruby-lang.org/pub/ruby/.*.tar.bz2'\''#url '\''http://ruby.taobao.org/mirrors/ruby/ruby-2.0.0-p353.tar.bz2'\''#' ~/.linuxbrew/Library/Formula/ruby.rb

brew install ruby
gem sources --remove https://rubygems.org/
gem sources -a http://ruby.taobao.org/

## install python failed, can skip?
#brew install python

brew install icu4c
brew link --force icu4c

gem install gollum
```

