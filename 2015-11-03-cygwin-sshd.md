cygwin 下安装 sshd
===

由于习惯了 linux 命令行，我在 windows 下一般会安装一下 cygwin 环境，为了能够 ssh 登陆，同时还会安装上 sshd 服务。
cygwin 经过这么多年的发展，已经日趋成熟，安装配置也相对简单。
下载运行[安装程序](https://cygwin.com/setup-x86.exe)，默认安装路径 "C:\cygwin"，我一般会改成 "D:\cygwin"，
通常我会把 cygwin 安装程序本身也丢到这个目录下，软件包下载目录也设成这个目录。
安装镜像选择一个国内速度较快的源，我一般会选 ustc http://mirrors.ustc.edu.cn/。
软件包选择目录搜索一下 ssh，选上 openssh 服务器和客户端。
其他软件包按需选择，vim, wget, curl, tar, find 等等这些常用的都可以选上，然后一路 next 即可完成安装。

安装完成后其他客户端工具都可以使用了，如果要使用 sshd 服务还要再额外配置一下，
配置过程也相对简单，cygwin 提供了一个配置脚本 ssh-host-config，需要注意的是需要以超级管理员 (Administrator) 权限运行这个脚本，
以超级管理员权限打开一个 cygwin 终端，运行 ssh-host-config，会问几个问题，基本上一路 yes 就可以了，
除了 CYGWIN 环境变量留空，cyg_server 用户是否改名选 no，设置一个密码，我一般随意设置一个简单的 "abc123"。
这个密码会在随后的脚本输出中明文打出，有点坑爹，所以不要输入敏感密码。
配置脚本会在系统中创建一个 sshd 用户和一个 cyg_server 用户，安装一个名为 sshd 的服务。
这个服务会在下次启动电脑时自动启动，或者使用 "net start sshd" 或 "cygrunsrv --start sshd" 手动启动。
之后就可以通过 ssh 使用本机用户名密码远程登陆机器了。
