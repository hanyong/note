ubuntu 12.04 buyvm 主机配置
===

在 buyvm.net 买了一个最低配 vps, 只有 128M 内存. 
安装了 ubuntu 12.04 minimal, 正担心能不能起来, 
结果起来了一看, 只用了 10 多 MB 内存, 还有大把空闲.
使用 `top` 或 `ps -ef` 命令看一下启动的进程数也是屈指可数, 很干净很爽.
下面记下我的安装设置过程.

管理控制台在 manage.buyvm.net, 登陆后可以改主机名, root 密码等设置.

## 系统安装与设置

```sh
# 首次登录以 root 登录, 登录后立即修改 root 密码.
passwd

# 创建普通用户
adduser hanyong

# 添加到 sudo 组
adduser hanyong sudo

# 断开连接
```

```sh
# 打通 ssh, 因为我本机与远程普通用户同名, 可以省略用户名
ssh-copy-id -i ~/.ssh/id_rsa.pub us.oolap.com
# 为了方便在 vps 上访问 github, 将我的 ssh key 也同步过去
rsync -av --itemize-changes ~/.ssh/id_rsa* us.oolap.com:~/.ssh/
# 登录 vps 继续设置, ssh 已经打通, 可以免密码登录
ssh us.oolap.com
```

```sh
# 第一步, 先更新源. buyvm.net 设置了自己的 ubuntu 镜像, 速度飞快.
sudo apt-get update
# 第二步, 安装用的更顺手的 aptitude
sudo apt-get install -y aptitude
# 默认最小化 ubuntu 命令行自动提示都没有, 有点不爽.

# 设置中文 locale
sudo locale-gen zh_CN.UTF-8
# 看了下默认的 locale 已经是 zh_CN.UTF-8 了, 奇怪.
# 原来登录后的 locale 默认与本地的 locale 相同, 厉害!

# vim
sudo aptitude install -y vim
# tmux
sudo aptitude install -y tmux
# 启动 tmux, 再 top 看下, 内存就基本占满了, 进程数还是很少, 没关系.

# nginx
sudo aptitude install -y nginx
sudo service nginx start
# squid
sudo aptitude install -y squid

# git 用 ubuntu 自带的好了
sudo aptitude install -y git
```

## 用户设置

```sh
# .vimrc
sed -re '/^\s*set\s+backup/ s#^#"#' /usr/share/vim/vim73/vimrc_example.vim > ~/.vimrc

# git config
git config --global user.name hanyong
git config --global user.email observer.hany@alibaba-inc.com
```

