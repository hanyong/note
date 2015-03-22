ubuntu 使用 FreeNx 访问远程桌面
===

有时会把公司笔记本电脑带回家用, 没有外接鼠标键盘显示器使用很不方便.
家里用的是台式机电脑，每次拆换键盘显示器也很麻烦.
所以最好就是将笔记本连上家里的局域网后, 在家里的台式机上远程访问笔记本电脑.
使用 ssh 当然没问题, 然而要做很多事情的话没有图像界面是远远不够的, 
比如打开 eclipse 写点代码, excel 编辑个文件.

之前尝试过 x11vnc 等 vnc 远程登陆, 图像效果差, 操作不流畅, 很多按键操作不灵, 各种问题.

比较靠谱的还是 `ssh -X` X 转发, 不过这样一次只能拉起一个 GUI 程序,
我通常是先起一个 gnome-terminal, 然后在这个 gnome-terminal 中启动其他 GUI 程序.
由于使用命令行启动 GUI 程序, 每个 GUI 程序会 block 住一个终端, 即一个 gnome-terminal 标签.
另外还有一些其他问题, 经常面临在两台机器的进程间切换, 
gedit, firefox 等最好只在远程机器上启动, 否则其进程间通信会有点问题.
连接 vpn 等操作习惯在桌面系统托盘上搞.
简单来说, 这种方式只是拉起一个进程, 而不是一个完整的桌面, 这种方式可以工作, 但用户体验不够好.
更极端一点, 这种方式得家里电脑也用 ubuntu, windows 下 x-server 也是体验不够好的.
但在家里经常喜欢用 windows 听听歌, 玩玩游戏.

今天看到有个软件叫 FreeNx, 开始打算尝试下, 要用 nomachine 的客户端,
下载 nomachine 4 的客户端搞了下没搞定， 直接卸载用 nomachine 4 免费版了, 感觉功能也挺好.

以下是折腾 freenx 的过程.

参考 [ubuntu 文档](https://help.ubuntu.com/community/FreeNX) 操作.
我使用的是 ubuntu 12.04.

这个软件包不再官方仓库中, 
先添加 [ppa 仓库](https://launchpad.net/~freenx-team/+archive/ubuntu/ppa),
再安装 `freenx-server`.

```sh
sudo apt-add-repository ppa:freenx-team/ppa
sudo aptitude update
sudo aptitude install freenx-server
```

安装完成时, 看到一条警告和一个 nxserver 启动失败的错误:

```sh
adduser：警告：主目录 /var/lib/nxserver/home/ 不属于您当前创建的用户。
正在设置 freenx-server (0.7.3.zgit.120322.977c28d-0~ppa11) ...
update-alternatives: 使用 /usr/lib/nx/nxserver 来提供 /usr/bin/nxserver (nxserver)，于 自动模式 中。
NX> 100 NXSERVER - Version 3.2.0-74-SVN OS (GPL, using backend: 3.5.0)
NX> 500 Error: No running sessions found.
NX> 999 Bye
NX> 100 NXSERVER - Version 3.2.0-74-SVN OS (GPL, using backend: 3.5.0)
mv: 无法获取"/var/lib/nxserver/home/.ssh/authorized_keys2.disabled" 的文件状态(stat): 没有那个文件或目录
NX> 122 Service started
NX> 999 Bye
正在处理用于 libc-bin 的触发器...
ldconfig deferred processing now taking place
```

安装完成后启动脚本在 `/etc/init.d/freenx-server`,
可通过 `sudo service freenx-server` 控制服务启动、停止.
手动执行 `sudo service freenx-server start` 重复出现前面的启动错误.
按文档描述应该是缺少 nxsetup, 参考文档下载运行 nxsetup.

```
wget https://bugs.launchpad.net/freenx-server/+bug/576359/+attachment/1378450/+files/nxsetup.tar.gz
tar -xvf nxsetup.tar.gz
sudo cp nxsetup /usr/lib/nx/
sudo /usr/lib/nx/nxsetup --install
```

询问是否使用自定义 key, 为简单起见, 先保持默认的 'N', 输出结果如下:

```
$ sudo /usr/lib/nx/nxsetup --install
------> It is recommended that you use the NoMachine key for
        easier setup. If you answer "y", FreeNX creates a custom
        KeyPair and expects you to setup your clients manually. 
        "N" is default and uses the NoMachine key for installation.

 Do you want to use your own custom KeyPair? [y/N] 
Setting up /etc/nxserver ...done
Generating public/private dsa key pair.
Your identification has been saved in /etc/nxserver/users.id_dsa.
Your public key has been saved in /etc/nxserver/users.id_dsa.pub.
The key fingerprint is:
9d:98:64:df:43:7b:db:75:49:dc:2f:2e:66:e6:7b:63 root@ali-59375n
The key's randomart image is:
+--[ DSA 1024]----+
|                 |
|              . .|
|        o   .  o.|
|       o = + .. o|
|        S + + o.+|
|             + +o|
|            = o .|
|           = .E  |
|            o+ . |
+-----------------+
Setting up /var/lib/nxserver/db ...done
Setting up /var/log/nxserver.log ...done
Adding user "nx" to group "utmp" ...done
Setting up known_hosts and authorized_keys2 ...done
Setting up permissions ...done
Setting up cups nxipp backend ...cp: "/usr/lib/cups/backend/ipp" 与"/usr/lib/cups/backend/ipp" 为同一文件
```

再次测试 `sudo service freenx-server start` 提示已经启动, 测试 stop, start 成功.

```sh
$ sudo service freenx-server status
$ sudo service freenx-server start
Not starting freenx-server, it's already started.
observer.hany@ali-59375n:~/tmp$ sudo service freenx-server stop
NX> 100 NXSERVER - Version 3.2.0-74-SVN OS (GPL, using backend: 3.5.0)
NX> 123 Service stopped
NX> 999 Bye
NX> 100 NXSERVER - Version 3.2.0-74-SVN OS (GPL, using backend: 3.5.0)
NX> 500 Error: No running sessions found.
NX> 999 Bye
$ sudo service freenx-server start
NX> 100 NXSERVER - Version 3.2.0-74-SVN OS (GPL, using backend: 3.5.0)
NX> 500 Error: No running sessions found.
NX> 999 Bye
NX> 100 NXSERVER - Version 3.2.0-74-SVN OS (GPL, using backend: 3.5.0)
NX> 122 Service started
NX> 999 Bye
```

安装完成后, 需要到 [nomachine](https://www.nomachine.com/) 网站下载客户端.
nomachine 免费版同时包含服务器和客户端, 企业版有一个免费客户端可供下载.
看介绍 nomachine 4 免费版可以访问远程机器的物理桌面,
企业版增加了创建虚拟桌面等功能, 看样子免费版的功能已经足够满足需求了, 挺不错的样子.
下载一个免费版本机安装试试.
从官网上找到下载页面链接, 下载后使用 `dpkg -i` 安装.

```sh
wget http://download.nomachine.com/download/4.4/Linux/nomachine_4.4.12_11_amd64.deb
sudo dpkg -i nomachine_4.4.12_11_amd64.deb
```

安装完成后可用 `sudo service nxserver` 管理服务, 可看到服务已经自动启动:

```sh
$ sudo service nxserver status
NX> 161 Enabled service: nxserver.
NX> 161 Enabled service: nxnode.
NX> 161 Enabled service: nxd.
```

注意: freenx 默认安装在 `/lib/lib/nx/` 下, 配置文件等按 linux 文件目录结构放, 如 `/etc/nxserver/`.
而 nomachine 默认安装在 `/usr/NX/` 下, 所有相关文件都在该目录的子目录下, 绿色软件的样子.
两者的安装目录和服务名均不冲突.

研究了下 nomachine 客户端怎么用, 
尝试使用 "System login" 登录, 提示服务没有运行, 研究半天没搞定, 不搞了, 
直接删了 freenx, 在远程机器上也给安装个 nomachine 免费版.

```sh
sudo add-apt-repository --remove ppa:freenx-team/ppa
sudo aptitude update
```
