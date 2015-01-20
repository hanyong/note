通过远程 ssh 安装 ubuntu
===

**未测试成功**:

0. CentOS 6.4 下 chroot 到 debootstrap 安装的系统后, 安装 openssh-server 失败.
0. 重启进入 debootstrap 安装的系统后网络设置不正确, 机器 ping 不同, 更无法 ssh 登陆.

假如你有一台机器, 只能通过 ssh 登陆上去, 如何在这台机器上重装 ubuntu 系统?
通过 ssh 安装 ubuntu, 核心是使用 debootstrap 安装系统, 官方有 3 篇文档可以参考,
不过有些文档较旧, 里面描述的有些内容已经过时没有更新.
这 3 篇文档按从新到旧的次序依次是:

0. [Installation/OverSSH-Light](https://help.ubuntu.com/community/Installation/OverSSH-Light)
0. [Installation/FromLinux#Without_CD](https://help.ubuntu.com/community/Installation/FromLinux#Without_CD)
0. [Installation/OverSSH](https://help.ubuntu.com/community/Installation/OverSSH)

## 准备安装新系统的分区

准备安装新系统的分区, 这里就不详述了, 使用 `parted` 或 `fdisk` 均可, `parted` 更新更强大.

```sh
mkfs.ext4 /dev/sdb1
mkswap /dev/sdb2
```

需要注意的是:

0. 安装系统的 `/boot` 所在分区要设置成可启动的
0. 安装完系统后别忘了安装 `linux-generic`, `grub-pc-bin` 和 `openssh-server`, 以能够启动并登陆系统.

## 安装 debootstrap

首先是要找到并安装希望安装的 ubuntu 对应版本 (或更新版本) 的 debootstrap.

先到 `http://packages.ubuntu.com/` 按包名搜索 `debootstrap`, 目标系统选择期望安装的 ubuntu 版本即可.
如果当前 linux 版本较旧, 安装新版本 debootstrap 可能还有很多困难, 
因此建议选择一个期望安装安装 ubuntu 版本对应的 debootstrap 版本即可.
如果这个版本都安装不上, 只能先安装一个较低版本的 ubuntu 再慢慢升级上来.

如我想安装 ubuntu 14.04 (trusty), 对应 debootstrap 版本的搜索结果链接为
http://packages.ubuntu.com/search?keywords=debootstrap&searchon=names&suite=trusty&section=all .
从搜索结果可看到对应 debootstrap 版本为 `1.0.59:all`.

找到 debootstrap 版本之后, 到任意 ubuntu 镜像的 `pool/main/d/debootstrap/` 目录下
即可找到并下载对应版本的 debootstrap.
可在 http://mirrors.ubuntu.com/ 找到 ubuntu 在各个地方的镜像.
如国内较快的镜像 http://mirrors.ustc.edu.cn/ubuntu/pool/main/d/debootstrap/ .
ubuntu 系统或支持 `dpkg` 的系统可以下载 `.deb` 包并使用 `dpkg -i` 命令安装.
其他系统可以用 `ar` 命令解开 `.deb` 包, 再用 `tar` 命令解开内部 `data.tar.gz` 文件到系统根目录 `/` 即可.
还可以下载 `udeb` 版本微 deb 包, 或者下载 `.tar.gz` 源码包版本, 参照 `README` 文档安装使用.

```sh
mkdir work
cd work
wget 'http://ubuntu.01link.hk/pool/main/d/debootstrap/debootstrap_1.0.59_all.deb'
ar xf debootstrap_1.0.59_all.deb
cd /
tar xf ~/work/data.tar.xz
```

## 使用 debootstrap 安装系统

首先挂载目标分区, 然后执行 debootstrap 安装系统到目标分区.
可使用 `--arch=` 参数指定系统架构, 可指定一个镜像 URL, 让下载安装速度快一些.

```sh
mkdir /mnt/ubuntu
mount /dev/sdb1 /mnt/ubuntu/
debootstrap --arch=amd64 --include=openssh-server,cgroup-lite trusty /mnt/ubuntu/ http://ubuntu.01link.hk/
#debootstrap --arch=amd64 --include=aptitude,linux-generic,grub-pc,vim trusty /mnt/ubuntu/ http://mirrors.aliyun.com/ubuntu/
```

## 基本系统设置

对安装完的基本系统进行设置,
可把当前系统的一些设置直接拷贝过去再进行修改.

```
echo $HOSTNAME > /mnt/ubuntu/etc/hostname
#rsync -av /etc/hostname /mnt/ubuntu/etc/
#rsync -av /etc/fstab /mnt/ubuntu/etc/
# fstab 参考配置
cat <<'EOF' > /mnt/ubuntu/etc/fstab
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
proc            /proc             proc    defaults        0 0
/dev/sdb1       /                 ext4    defaults,errors=remount-ro        0 1
/dev/sdb2       none              swap    sw              0 0
#tmpfs           /dev/shm          tmpfs   defaults        0 0
#devpts          /dev/pts          devpts  gid=5,mode=620  0 0
#sysfs           /sys              sysfs   defaults        0 0
EOF
#vim /mnt/ubuntu/etc/fstab
```

```sh
#rsync -av /etc/networks /mnt/ubuntu/etc/
#rsync -av /etc/network/interfaces /mnt/ubuntu/etc/network/
#vim /mnt/ubuntu/etc/network/interfaces
# interfaces 参考配置, ifconfig 查看当前配置相关信息
cat <<EOF >> /etc/network/interfaces
auto lo
iface lo inet loopback

# seth0
auto seth0
iface seth0 inet static
    hwaddress 00:15:5d:d7:02:25
	address 118.193.215.39
	netmask 255.255.255.128
	gateway 118.193.215.1
EOF
```

vps CentOS 网卡配置

```sh
[root@cloud ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0 
DEVICE=seth0
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
DEFROUTE=yes
IPV6INIT=no
IPV4_FAILURE_FATAL=yes
PEERDNS=yes
NAME=VPSNetCard
HWADDR=00:15:5d:d7:02:25
IPADDR=118.193.215.39
NETMASK=255.255.255.128
GATEWAY=118.193.215.1
DNS1=8.8.8.8
DNS2=8.8.4.4
```

## 进入新安装系统环境

# vps 系统重新初始化后设置
```sh
yum remove xorg-x11-server-Xorg hal cups postfix
mkdir /mnt/ubuntu
echo 'UUID=4ed1920a-e87b-4b91-b4da-e1e4d5401578 /mnt/ubuntu ext4 defaults 1 1' >> /etc/fstab
mount /mnt/ubuntu
mount -o bind /dev /mnt/ubuntu/dev
chroot /mnt/ubuntu

# 为 chroot 后的系统挂载重要系统目录:
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devpts none /dev/pts
grub-install /dev/sda
grub-set-default CentOS
```

进入新安装系统环境前, 需要先为新系统挂载 `/dev`.

```sh
mount -o bind /dev /mnt/ubuntu/dev
chroot /mnt/ubuntu

# 为 chroot 后的系统挂载重要系统目录:
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devpts none /dev/pts
mount /hd-inst
#export HOME=/root
#export LC_ALL=C
```

退出时记得 umount 对应的文件系统, 参考重启说明.

## 设置时区和语言

```sh
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
echo 'Asia/Shanghai' > /etc/timezone
cat <<EOF > /etc/default/locale
LANG="en_US.UTF-8"
LANGUAGE=
EOF
locale-gen en_US.UTF-8 zh_CN.UTF-8
#dpkg-reconfigure -f noninteractive tzdata
#dpkg-reconfigure locales
```

## 安装其他软件包, 安装 OpenSSH 服务器和 grub

```sh
sudo apt-get update
sudo apt-get install aptitude
sudo aptitude install linux-generic
#sudo aptitude install openssh-server
sudo grub-install /dev/sda
sudo update-grub
```

# 重启

```sh
umount /dev/pts
umount /sys
umount /proc
exit

# 回到 chroot 前的系统只执行
umount /mnt/ubuntu/dev/
reboot
```
