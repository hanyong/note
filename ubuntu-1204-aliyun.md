阿里云 ubuntu 12.04 配置指南
===

## 全局设置

```sh
# 基本工具
sudo apt-get update
sudo apt-get install -y aptitude
sudo aptitude install -y python-software-properties
sudo aptitude install -y tmux
sudo aptitude install -y gcc g++ autoconf automake cmake
# 中文支持
sudo locale-gen zh_CN.UTF-8 zh_CN.GB18030 zh_CN.GBK

# vim
# 需要安装 `vim-gnome` 后才能简单在 vim 中复制内容到 gnome 剪贴板.
sudo aptitude install -y vim vim-gnome
sudo tee /etc/vim/vimrc.local <<EOF
set ts=4 sw=4 nu
set nobackup
set backupdir=~/tmp,/tmp,.
EOF
#>
# tmux
sudo aptitude install -y tmux
#>

# 修改 hostname
# FIXME: 经测试不能改 hostname, 重启后 hostname 恢复为原设置.
(
OLD_NAME=$HOSTNAME
NEW_NAME=han-srv
# append new name to "127.0.1.1"
# @see https://help.ubuntu.com/community/NetworkConfigurationCommandLine/Automatic#Setting.2BAC8-changing_the_hostname
sudo sed -i -re '/^127\.0\.1\.1\s+/ s#$# '"${NEW_NAME}"'#' /etc/hosts
# set new name
sudo hostname "${NEW_NAME}"
# replace OLD_NAME
sudo sed -i -re 's#\b'"${OLD_NAME}"'\b#'"${NEW_NAME}"'#' /etc/hosts
# update "127.0.1.1"
sudo sed -i -re '/^127\.0\.1\.1\s+/ c \'$'\n'"127.0.1.1 ${NEW_NAME}" /etc/hosts
)

# 数据盘分区 `/opt`, `/home`
# `sudo fdisk -l` 查看确定数据盘, `sudo fdisk "${DATA_DEV}"` 进行分区.
(
DATA_DEV=/dev/xvdb
#sudo fdisk "${DATA_DEV}"
#   o   create a new empty DOS partition table
#   n   add a new partition
: '
Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-31457279, default 2048): 
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-31457279, default 31457279): +5G

Command (m for help): n
Partition type:
   p   primary (1 primary, 0 extended, 3 free)
   e   extended
Select (default p): p
Partition number (1-4, default 2): 
Using default value 2
First sector (10487808-31457279, default 10487808): 
Using default value 10487808
Last sector, +sectors or +size{K,M,G} (10487808-31457279, default 31457279): 
Using default value 31457279
'
#   w   write table to disk and exit

DEV_OPT="${DATA_DEV}1"
DEV_HOME="${DATA_DEV}2"
# format
sudo mkfs.ext4 "${DEV_OPT}"
sudo mkfs.ext4 "${DEV_HOME}"
# find dev uuid by blkid, update `/etc/fstab`
eval "$(blkid -o export "${DEV_OPT}")"
echo "UUID=$UUID /opt $TYPE defaults 0 0" | sudo tee -a /etc/fstab
eval "$(blkid -o export "${DEV_HOME}")"
echo "UUID=$UUID /home $TYPE defaults 0 0" | sudo tee -a /etc/fstab
# mount
sudo mount /opt
sudo mount /home
)

# 创建普通用户
#sudo adduser hanyong
sudo adduser hanyong sudo
# 完成后退出, 重新使用普通用户登录.
```

```sh
# 打通普通用户 ssh 通道
ssh-copy-id -i ~/.ssh/id_rsa.pub oolap.com
```

```sh
# gollum
sudo aptitude install ruby1.9.1 ruby1.9.1-dev
# 按淘宝镜像提示更新 gem 源.
sudo gem sources -l | grep -P '^http.*\brubygems\.org\b' | xargs --no-run-if-empty sudo gem sources --remove
sudo gem sources -a http://ruby.taobao.org/
sudo aptitude install -y libicu-dev
sudo gem install --no-rdoc --no-ri gollum
```

## 个人设置

```sh
cat <<EOF > ~/.pam_environment
LANGUAGE=zh_CN:en_US:en
LANG=zh_CN.UTF-8
EOF
```

