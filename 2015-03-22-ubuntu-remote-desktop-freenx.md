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

综合尝试过 nomachine 4, freenx, nomachine 3, x2go 后, 
整体感觉是 nomachine 4 > x2go > nxclient + freenx > nomachine 3.
而且其他几个软件好像都只有 linux (和mac) 的服务端, nomachine 4 是唯一跨平台最好的.
还有 nomachine 4 是唯一共享物理屏幕的 (因为其他几个都是 nomachine 3 系), 
体验会更一致和流畅一些, 缺憾是屏幕分辨率不能超过远程机器物理屏幕分辨率.

今天看到有个软件叫 FreeNx, 打算尝试下.
参考 [ubuntu 文档](https://help.ubuntu.com/community/FreeNX) 操作.
我使用的是 ubuntu 12.04.

这个软件包不在官方仓库中, 
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

安装完成后, 需要从 nomachine 网站下载客户端.
freenx 对应的 nomachine 版本是 [nomachine 3](https://www.nomachine.com/version-3).
nomachine 3 核心代码是开源的, 
freenx, x2go 等开源软件都是基于 nomachine 3 的开源代码进行开发.
但 nomachine 4 开始决定闭源.
现在官网主推 nomachine 4, 并且也不再提供 nomachine 3 的免费下载.

nomachine 4 也提供免费版, 免费版同时包含服务器和客户端, 企业版有一个免费客户端可供下载.
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
而 nomachine 4 默认安装在 `/usr/NX/` 下, 所有相关文件都在该目录的子目录下, 绿色软件的样子.
两者的安装目录和服务名均不冲突.

试用了下 nomachine 4 免费版, 两台机器都安装上 nomachine 4 就可以互通访问了, 感觉挺不错的.
免费版不支持 ssh "System login", 要使用 NX 协议支持公钥登录, 需要添加公钥到 nomachine 的公钥配置,
参考[这里](https://www.nomachine.com/AR02L00785).
但折腾半天不知道怎么跟 freenx 配合使用, 也不知道能不能配合 freenx 使用.

nomachine 官方不再提供 nomachine 3 的下载,
网上搜了下在其他地方找到了 [nomachine 3 的下载链接](https://code.google.com/p/vpsvoo/downloads/list),
[这里找到 windows nxclient](http://uni-smr.ac.ru/archive/linux/distr/special/servers-and-clusters/NX/),
windows nxserver 没找到, 不知道有没有.
看样子 nomachine 3 拆分了 3 个包 nxserver, nxnode, nxclient.
nomachine 4 免费版则只有一个包, 但启动时也可看到分成了 nxserver, nxnode 这样的服务.
nomachine 3 与 nomachine 4 冲突, 需要先卸载 nomachine 4 才能安装 nomachine 3.
安装时可看到, nxserver 依赖 nxnode 和 nxclient, nxnode 依赖 nxclient.

可以先安装 nxclient.

```sh
sudo dpkg -i nxclient_3.5.0-7_amd64.deb
```

也可以 3 个包一起安装:

```sh
sudo dpkg -i nxclient_3.5.0-7_amd64.deb nxnode_3.5.0-9_amd64.deb nxserver_3.5.0-11_amd64.deb
```

一起安装后可看到多了两个服务 nxserver 和 nxsensor.
nxsensor 不知道是什么, 并且好像默认是禁用状态.

```sh
$ sudo service nxse
nxsensor  nxserver  
$ sudo service nxserver restart
Trying to restart NX server:
NX> 611 No subscription information found. Please visit the
NX> 611 NoMachine web site at http://www.nomachine.com/
NX> 611 to acquire a valid subscription.
NX> 611 The NX server can't perform the requested operation.
NX> 999 Bye.
Trying to restart NX statistics:
NX> 611 No subscription information found. Please visit the
NX> 611 NoMachine web site at http://www.nomachine.com/
NX> 611 to acquire a valid subscription.
NX> 611 The NX server can't perform the requested operation.
NX> 999 Bye.
$ sudo service nxsensor restart
nxsensor is disabled in '/usr/NX/etc/node.cfg'
```

客户端机器从程序菜单选择 "NX Connection Wizard" 建立一个到远程机器的会话信息, 
收入用户密码即可连接到安装了 freenx 的远程机器桌面, 使用体验跟 windows 远程桌面很像.

测试一下 nomachine 自带的 nxserver, 直接连接提示 "No subscription information found",
跟上述执行 `sudo service nxserver start` 的提示类似.
根据上面安装 freenx 的经验, 是不是也要做一些设置?
看了下目录 `/usr/NX/bin/` 没有 nxsetup 命令.
执行 `/usr/NX/bin/nxserver --help` 看到有个  `--install` 参数, 执行一下, 没什么用.
网上搜了下, 这个错误应该是没有证书, [链接](https://www.nomachine.com/AR07D00404).
看了下证书文件 `server.lic` 和 `node.lic` 是有的, 
估计是 nomachine 4 残留的文件, 与 3 不匹配.
卸载 nxserver 和 nxnode, 删除证书文件, 重新安装, 问题解决.

```sh
sudo aptitude purge nxnode nxserver
sudo rm /usr/NX/etc/*.lic
sudo dpkg -i nxnode_3.5.0-9_amd64.deb nxserver_3.5.0-11_amd64.deb
```

再次用 nxclient 连接, 认证不通过.
根据网上看的一些文章, nxserver 可能不是直接用系统用户登陆认证,
尝试执行如下命令添加用户.

```sh
sudo /usr/NX/bin/nxserver --useradd $USER
```

输入密码后出现如下错误:

```
Info: received data in err channel from NX Node: 'Bad owner or permissions on /home/hanyong/.ssh/config
' (NXNodeExec)
```

再 google 了下, 是用 [sudo 执行 nxserver 的一个坑](https://www.nomachine.com/AR02E00446).
想到之前执行 `nxserver --install` 也出现这个错.
直接切换到 root 用户, 再执行 `nxserver --install`, 
执行成功, 这个好像是安装和更新 nxserver 本身的.

```
sudo su -l
/usr/NX/bin/nxserver --install
```

再次用客户端连接, 连接成功.

在已安装过 freenx 的机器上安装 nomachine 3 的 nxserver, 
因为都用了 nx 这个用户, 创建用户失败, 安装失败.
卸载 freenx 再重装.
直接连接新安装 nomachine 3 的机器成功.
看来应该不需要做额外设置,
之前连接不成功是因为安装问题.

另外试了下 x2go, x2go 支持传输声音, 整体感觉比 freenx 好.
安装 x2go 服务端需要添加 ppa 仓库, 当官方仓库自带了 x2go 客户端.

```sh
sudo aptitude install x2goclient
```

```sh
sudo add-apt-repository ppa:x2go/stable
sudo aptitude update
sudo aptitude install x2goserver x2goserver-xsession
```
