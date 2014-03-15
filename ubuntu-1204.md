ubuntu 12.04 安装使用记录
===

## 安装

下载光盘镜像, 将光盘镜像下 `/casper/{vmlinuz,initrd}*` 两个文件解压出来.

```sh
├── ubuntu-12.04.4-desktop-amd64.iso
└── ubuntu-12.04.4-desktop-amd64/
    └── casper/
        ├── initrd.lz
        └── vmlinuz.efi
```

使用 "Grub 4 DOS" (或 EasyBCD) 启动安装镜像.
启动配置如下:

```sh
title Ubuntu 12.04.4 LiveCD
find --set-root /home/software/linux/ubuntu-12.04.4-desktop-amd64.iso
kernel /home/software/linux/ubuntu-12.04.4-desktop-amd64/casper/vmlinuz.efi boot=casper iso-scan/filename=/home/software/linux/ubuntu-12.04.4-desktop-amd64.iso
initrd /home/software/linux/ubuntu-12.04.4-desktop-amd64/casper/initrd.lz
```

命令行执行下列命令卸载镜像挂载点:

```sh
sudo umount -l /isodevice/
```

运行安装程序, 手动设置分区, 语言选择中文.

## 基本设置

安装 `aptitude`, 完成后重启终端使 `aptitude` 自动提示生效.

```sh
sudo apt-get update
sudo apt-get install aptitude
```

"系统设置" -> "键盘" -> "快捷键" -> "系统",
设置 "显示运行命令提示符" 快捷键为 "Alt + F2".

运行 `/usr/lib/ibus-sunpinyin/ibus-setup-sunpinyin`,
设置 sunpinyin 翻页快捷键和字符集.

### 取消全局菜单

删除带 "appmenu" 的软件包.

```sh
sudo aptitude remove indicator-appmenu
```

### 恢复正常滚动条

删除带 "scrollbar" 的软件包.

```sh
sudo aptitude remove overlay-scrollbar liboverlay-scrollbar3-0.2-0 liboverlay-scrollbar-0.2-0
```

### 设置 "HOME" 目录下的文件夹为英文名

"用户账户" 修改用户语言为 "英语(美国)",
重新登陆后系统自动运行 `/usr/bin/xdg-user-dirs-gtk-update` 
提示修改文件名, 选择 "Yes".
再次修改用户语言恢复为 "汉语", 
重启登陆后提示修改文件名时选择 "否", 并勾选 "不要再提示".

### 安装 gnome2 桌面

安装 `gnome-session-fallback`.

```sh
sudo aptitude install gnome-session-fallback
```

注销或重启, 登陆界面选择 "Gnome classic" 进入系统.

### 关闭按钮调到菜单栏右边

安装 `gconf-editor`.

```sh
sudo aptitude install gconf-editor
```

打开 "gconf-editor", 
设置 "/apps/metacity/general/button_layout"
值为 ":minimize,maximize,close".

### 设置任务栏

"Alt + 右键" 点击底部任务栏, 打开 "属性" 设置.
取消 "扩展", 左键点击托动面板到屏幕中间, 稍后安装 "dock" 软件包后可以删除.
同样设置顶部面板, 取消 "扩展", 设置方向为 "底部", 拖到屏幕右下角.
原上部面板变成下部面板, 添加 "显示桌面" 和 "时钟", 设置所在地区.

* 删除原面板中的时间显示

安装 `dconf-tools`.

```sh
sudo aptitude install dconf-tools
```

运行 "dconf-editor", 
找到 "com.canonical.indicator.datetime",
取消所有显示选项.

* 安装 dock

```sh
sudo aptitude install avant-window-navigator
sudo aptitude install libdesktop-agnostic-cfg-gconf
```

安装 `libdesktop-agnostic-cfg-gconf` 避免 dock 启动时出现一个讨厌的绿色 "+" 号,
参考: https://bugs.launchpad.net/awn/+bug/990774.

运行 "avant-window-navigator".
首选项取消 "扩展面板", 位置设置为左边, 勾选 "Start Awn automatically".
"Task Manager" 取消勾选 "Group common windows".
"Applets" 设置仅需要保留 "Cairo Main Menu", "分隔符", "任务管理器" 3 项.
"Cairo Main Menu" 旁边带的 "Places" 上右键选择 "Remove Icon" 去掉这个图标.
"Advanced" 设置 "Offset" 为 "8".

>"Cairo Main Menu" 菜单有些功能失效了, 没有 "注销" 和 "关机",
可以尝试装 `awn-applet-yama`, yama 有时会崩溃.
yama 默认的图标颜色太浅, 
可修改文件 `/usr/share/avant-window-navigator/applets/yama/yama.py` 
修改 `applet_logo` 更换图标, 如改为 `/usr/share/icons/gnome/scalable/places/ubuntu-logo.svg`.

### gedit

"编辑" -> "首选项", "查看", 勾选 "显示行号", 取消 "启用自动换行".
"编辑器" "字表符宽度" 设置为 "4", 取消 "在保存前创建备份文件".

### 安装 vim

```sh
sudo aptitude install vim vim-gnome
```

>需要安装 `vim-gnome` 后才能简单在 vim 中复制内容到 gnome 剪贴板.

打开 `$VIM/vim73` 目录下的 `vimrc_example.vim`, 确认关闭 `backup`.
编辑文件注释掉 `nobackup`, 保存到 `~/.vimrc`.

```sh
:e /usr/share/vim/vim73/vimrc_example.vim
:set backup!
:w ~/.vimrc
```

可以将需要修改的通用设置保存到 `/etc/vim/vim.local` 全局修改.
`nobackup` 必须改 `~/.vimrc` 文件, 否则全局修改会被 `~/.vimrc` 覆盖.

```vim
set ts=4 sw=4 nu
set nobackup
set bdir=~/tmp,/tmp,.
```

### 连接公司 VPN

安装 openconnect.

```sh
sudo aptitude install network-manager-openconnect-gnome
```

配置 VPN, 只需要在 "网关" 输入公司 VPN 地址, 不需要 "https://" 前缀.
点连接, 输入用户名, 密码即可登陆成功.

