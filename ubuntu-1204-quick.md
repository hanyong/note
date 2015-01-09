ubuntu 12.04
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

重启进入 LiveCD 桌面后执行下列命令卸载镜像挂载分区:

```sh
sudo umount -l /isodevice/
```

### 设置 lvm 分区

安装系统前可以参考 [UbuntuDesktopLVM][] 设置 lvm 逻辑卷.

```sh
# 准备一个启动分区和一个物理卷分区.
# 在我的机器上分别是主分区 `/dev/sda3` 和逻辑分区 `/dev/sda5`.
BOOT_DEV="/dev/sda3"
PV_DEV="/dev/sda5"

# LiveCD 安装 lvm2.
# 安装完有一个内核镜像 (LiveCD 只读镜像) 不能修改的错误, 请忽略.
sudo aptitude install -y lvm2

# 创建物理卷
sudo pvcreate "${PV_DEV}"

# 创建 lvm 卷组
sudo vgcreate vg "${PV_DEV}"
#             ^     ^
#            name   PV

# 创建逻辑卷
sudo lvcreate -L 20G -n lvroot vg
#                 ^       ^    ^
#                size    name  VG
sudo lvcreate -L 50G -n lvhome vg
sudo lvcreate -L 10G -n lvopt vg
sudo lvcreate -L 5G -n lvswap vg
# 查看逻辑卷
sudo lvdisplay

# 在逻辑卷上创建文件系统
sudo mkfs.ext4 /dev/mapper/vg-lvroot
sudo mkfs.ext4 /dev/mapper/vg-lvhome
sudo mkfs.ext4 /dev/mapper/vg-lvopt
sudo mkswap -f /dev/mapper/vg-lvswap
```

>LiveCD 默认不支持 lvm, 重启到 LiveCD 安装 lvm2 后不能自动识别出已创建的 lvm 卷设备.
测试发现: 执行一次 `vgexport` 后再执行一次 `vgimport`, 就会识别到已有的 lvm 卷了.

>```sh
# 重启到 LiveCD
sudo apt-get install -y lvm2
sudo vgexport -a
sudo vgimport -a
>```

运行安装程序, 语言选择中文, 
手动设置分区, 设置创建好的逻辑卷作为安装分区.
**注意**: 启动程序 (如 grub) 可能不能识别逻辑卷, `/boot` 最好挂载在非逻辑卷 `${BOOT_DEV}` 上.

Desktop 内核默认没有安装逻辑卷功能, 安装完系统后不能立即重启, 
按下列操作为安装后的系统安装 lvm2.

```sh
# 挂载安装后的系统
sudo mount /dev/mapper/vg-lvroot /mnt
sudo mount /dev/mapper/vg-lvhome /mnt/home
sudo mount /dev/mapper/vg-lvopt /mnt/opt
sudo mount "${BOOT_DEV}" /mnt/boot
# chroot 过去
sudo chroot /mnt
```

**注意**: 
* 下列操作在 chroot 之后的终端环境下执行, **跟上述操作不能在一个脚本里执行**.
* chroot 后当前用户是 root.

```sh
# OPTIONAL: Load LVM modules on startup 
cat <<EOF | tee -a /etc/modules >> /etc/initramfs-tools/modules
dm-mod
dm-snapshot
dm-mirror
EOF

# 安装 lvm2
apt-get install -y lvm2
```

>如果没有安装 lvm2 系统将无法启动. 
LiveCD 默认也不支持 lvm, 重启到 LiveCD 安装 lvm2 后也不能自动识别出已创建的 lvm 卷.
测试发现: 执行一次 `vgexport` 后再执行一次 `vgimport`, 就会识别到已有的 lvm 卷了.

## 全局

```sh
# vim 基本配置
sudo tee /etc/vim/vimrc.local <<EOF
set ts=4 sw=4 nu
"set et
set nobackup
set backupdir=~/tmp,/tmp,.
EOF
#>

# adduser 用户名允许使用 "."
sudo sed -i '/^NAME_REGEX=/ d; /^#NAME_REGEX=/ a \''
NAME_REGEX="^[a-z][-a-z0-9_.]*$"
' /etc/adduser.conf

# 基本工具
sudo apt-get update
sudo apt-get install -y aptitude dconf-tools gconf-editor realpath
# 其他工具
#sudo aptitude install -y gnome-color-chooser
sudo aptitude install -y tree unrar

# fix "小提示" 前景色, 背景色
sudo sed -i -r -e 's/tooltip_bg_color\:\#\w+/tooltip_bg_color:#FFFFAF/' -e 's/tooltip_fg_color\:\#\w+/tooltip_fg_color:#000000/' /usr/share/themes/Ambiance/{gtk-2.0/gtkrc,gtk-3.0/settings.ini}

# 系统设置
sudo locale-gen zh_CN.GBK zh_CN.GB18030

# git
#sudo add-apt-repository -y ppa:git-core/ppa
#sudo apt-get update
sudo aptitude install -y git gitk git-cola
sudo chmod +x /usr/share/doc/git/contrib/workdir/git-new-workdir
#ln -sf /usr/share/doc/git/contrib/workdir/git-new-workdir ~/usr/local/bin/

# gnome classic
# https://help.ubuntu.com/community/PreciseGnomeClassicTweaks
# 这篇文章介绍安装 `gnome-panel` 比 `gnome-session-fallback` 好.
# 其他设置说明推荐参考这篇文章.
sudo aptitude remove -y indicator-appmenu
sudo aptitude remove -y overlay-scrollbar liboverlay-scrollbar3-0.2-0 liboverlay-scrollbar-0.2-0
sudo aptitude install -y gnome-panel
# "GNOME Classic (No effects)" 默认使用 metacity, "GNOME Classic" 默认使用 compiz.
# 如果要使用 compiz, 可安装相应配置管理和插件
sudo aptitude install -y compiz compizconfig-settings-manager compiz-plugins-extra compiz-plugins-main compiz-plugins
#注销, 登陆界面选择 "GNOME Classic (No effects)" 进入系统.

# awn dock.
#`-R` 避免安装一堆用不着的 awn 推荐依赖. 
# 安装 `libdesktop-agnostic-cfg-gconf` 避免 dock 启动时出现一个讨厌的绿色 "+" 号,
# 参考: https://bugs.launchpad.net/awn/+bug/990774.
sudo aptitude install -R -y avant-window-navigator awn-settings awn-applet-cairo-main-menu libdesktop-agnostic-cfg-gconf

# vim
# 需要安装 `vim-gnome` 后才能简单在 vim 中复制内容到 gnome 剪贴板.
sudo aptitude install -y vim vim-gnome

# vpn
# 连接公司 VPN 需要安装 openconnect.
sudo aptitude install -y network-manager-openconnect-gnome
# 配置 VPN, 只需要在 "网关" 输入公司 VPN 地址, 不需要 "https://" 前缀.
# 点连接, 输入用户名, 密码即可登陆成功.
# GUI 登录老是出现 "VPN secret 非法" 的错误. 命令行登录可以成功.
# 安装 `vpnc` 得到得到脚本 `/etc/vpnc/vpnc-script`, 
# 然后使用 `sudo openconnect --script /etc/vpnc/vpnc-script <server>` 即可登录成功.
sudo aptitude install -y vpnc
```

### gollum

```sh
# c, c++ 基本开发工具
sudo aptitude install -y gcc g++ autoconf automake cmake
# ruby
sudo aptitude install -y ruby1.9.1 ruby1.9.1-dev
# 按淘宝镜像提示更新 gem 源.
# 额, 国外 vps 应该跳过这一步 ?
sudo gem sources -l | grep -P '^http.*\brubygems\.org\b' | xargs --no-run-if-empty sudo gem sources --remove
sudo gem sources -a http://ruby.taobao.org/
sudo gem sources -l
# icu4c zlib1g-dev
sudo aptitude install -y libicu-dev zlib1g-dev
# gollum
sudo gem install --no-rdoc --no-ri gollum
```

## 个人

ubuntu 下系统和应用程序有两种方式保存配置.

|     | GUI 编辑器 | 命令行操作
| --- | --- | --- | ---
| 旧方式 | gconf-editor gconf-editor | gconf2 gconftool-2
| 新方式 | dconf-tools dconf-editor | libglib2.0-bin gsettings

```sh
# 查看所有配置
gconftool-2 -R
gsettings list-recursively
# 设置值
gconftool-2 --type int|bool|float|string|list|pair /path/to/key value
gsettings set path.to key value
```

```sh
# 设置 "HOME" 目录下的文件夹为英文名
LANGUAGE=en_US:en LANG=en_US.UTF-8 /usr/bin/xdg-user-dirs-update --force
#重新登陆后系统自动运行 `/usr/bin/xdg-user-dirs-gtk-update` 
#提示修改文件名时选择 "否", 并勾选 "不要再提示".

# 删除 `.pam_environment` 文件中 "^LC_" 相关设置.
sed -i '/^LC_/ d' .pam_environment

# inputrc
cat <<'EOF' > ~/.inputrc
$include /etc/inputrc

# mappings for Ctrl-up-arrow and Ctrl-down-arrow for history search
"\e[1;5A": history-search-backward
"\e[1;5B": history-search-forward
EOF

## gnome classic
# move min/max/close buttons
gconftool-2 --set "/apps/metacity/general/button_layout" --type string ":minimize,maximize,close"
# Run dialog
#gconftool-2 --set "/apps/metacity/global_keybindings/panel_run_dialog" --type string "<Alt>F2"

# update-notifier
gsettings set com.ubuntu.update-notifier auto-launch false

# "显示桌面", "Alt" + 右键, "移动", 拖到最右下.
# 完整指示器, "Alt" + 右键, "Move", 拖到右下角面板上.
# 用户完整名字设置为空可避免显示用户名.
# 运行 `dconf-editor`, 展开 `com.canonical.indicator.datetime`, 
# 取消 "show-events".
gsettings set com.canonical.indicator.datetime show-events false
gsettings set com.canonical.indicator.datetime time-format custom
gsettings set com.canonical.indicator.datetime custom-time-format '%F %A %H:%M'
# 或者删除 "完整指示器", 依次添加 "指示器小程序", "时钟" 和 "指示器小程序会话" 到右下角.
#sudo aptitude install -y indicator-applet indicator-applet-session

# 桌面切换, 右键, "首选项", "工作区的数量" 修改为 "1".
# compiz
gconftool-2 --type int --set /apps/compiz-1/general/screen0/options/hsize 1
gconftool-2 --type int --set /apps/compiz-1/general/screen0/options/vsize 1
# "Alt" + 右键, "从面板上删除".

# ccsm
# 禁用插件 "Desktop Wall" (wall), "Grid" (grid), "Snapping Windows" (snap),
# 启用插件 "Static Application Switcher" (staticswitcher)
( x="$(python2 -c '
toDel = [ "wall", "grid", "snap", ]
toAdd = [ "staticswitcher", ]
s0 = r"""'"$(gconftool-2 --get /apps/compiz-1/general/screen0/options/active_plugins)"'"""
L = s0[1:-1].split(",")
L = [ e for e in L if not e in toDel]
L += [e for e in toAdd if not e in L]
print ",".join(L)
')" && gconftool-2 --type list --list-type string --set /apps/compiz-1/general/screen0/options/active_plugins "[$x]"
)
# 窗口管理 "缩放" 插件禁用 '<Shift><Alt>Up' 快捷键, 避免跟 eclipse 快捷键冲突
gconftool-2 --type string --set /apps/compiz-1/plugins/scale/screen0/options/initiate_key Disabled

## gedit
# "编辑" -> "首选项".
# "查看" tab, 勾选 "显示行号", 取消 "启用自动换行".
gsettings set org.gnome.gedit.preferences.editor display-line-numbers true
gsettings set org.gnome.gedit.preferences.editor wrap-mode none
# "编辑器" tab, "制表符宽度" 修改为 "4", 取消 "在保存前创建备份文件".
gsettings set org.gnome.gedit.preferences.editor tabs-size 4
gsettings set org.gnome.gedit.preferences.editor auto-indent true
gsettings set org.gnome.gedit.preferences.editor create-backup-copy false
# "使用空格代替制表符插入"
#gsettings set org.gnome.gedit.preferences.editor insert-spaces true

# 显示文件末尾换行符
# @see https://bugs.launchpad.net/ubuntu/+source/gedit/+bug/379367
gsettings set org.gnome.gedit.preferences.editor ensure-trailing-newline false

## gnome-terminal
# "编辑" -> "配置文件首选项".
# "颜色" tab, 取消 "使用系统主题中的颜色",
gconftool-2 --type bool --set /apps/gnome-terminal/profiles/Default/use_theme_colors false
# "内置方案" 选择 "白底黑字"
gconftool-2 --type string --set /apps/gnome-terminal/profiles/Default/background_color '#FFFFFFFFFFFF'
gconftool-2 --type string --set /apps/gnome-terminal/profiles/Default/foreground_color '#000000000000'
# "黑底灰字"
#gconftool-2 --type string --set /apps/gnome-terminal/profiles/Default/background_color '#000000000000'
#gconftool-2 --type string --set /apps/gnome-terminal/profiles/Default/foreground_color '#AAAAAAAAAAAA'

## sunpinyin
# 运行 `/usr/lib/ibus-sunpinyin/ibus-setup-sunpinyin`.
# "Keyboard" tab, "Page Flip" 选中 "- / =", "[ / ]".
gconftool-2 --type bool --set /desktop/ibus/engine/SunPinyin/Keyboard/Page/Brackets true
gconftool-2 --type bool --set /desktop/ibus/engine/SunPinyin/Keyboard/Page/MinusEquals true
# "General" tab, "Character Set" 选择 "GB18030" (或保持默认 "GBK").
#gconftool-2 --type string --set /desktop/ibus/engine/SunPinyin/General/Charset GB18030
```

## ssh

```sh
mkdir -p ~/.ssh
cp /d/home/hanyong/.ssh/id_rsa* ~/.ssh/
chmod 400 ~/.ssh/id_rsa
```

## git

```sh
git config --global user.name hanyong
git config --global user.email observer.hany@alibaba-inc.com
git config --global diff.tool bc3
git config --global merge.tool bc3
#git config --global push.default simple
git config --global push.default current
```

## firefox

运行 `firefox -P`, "Create Profile...", name "default", 
"Choose Folder...", "~/var/firefox/default", "Finish".
"Start Firefox".

>如果没有已有配置，可进行如下基本设置.

>"编辑" -> "首选项".

>* 常规 tab, "启动 Firefox 时" 选择 "显示上次打开的窗口和标签页".
"下载" 选择 "总是询问保存文件的位置".
>* 高级 tab, "证书", 设置 "自动选择一个", "查看证书" -> "您的证书" -> "导入...", 选择个人 p12 证书文件.
弹出 "修改主密码", 保留为空, 直接点 "确定", 弹出警告, 再确定.
弹出密码输入对话框, 输入证书密码, 点 "确定".

## 任务栏

### 顶面板

* "Alt" + 右键, "删除该面板", 弹出确认对话框, 点 "删除".

### awn dock

底面板取消扩展, 拖到右下角.

运行 `avant-window-navigator`.

* "首选项", -"Size of icons" 设置为 "40" pixels-.
"Position on the screen" 设置为 "左边".
勾选 "Start Awn automatically".
* "Task Manager", 取消 "Group common windows".
* "Applets" 设置仅需要保留 "Cairo Main Menu", "分隔符", "任务管理器" 3 项.
"Cairo Main Menu" 旁边带的 "Places" 上右键选择 "Remove Icon" 去掉这个图标.
* "Advanced", "Offset" 设置为 "7".

awn 设置好后删除底面板上的 "task list".

>使用 "GNOME Classic (No effects)" (metacity) 时默认 "awn" 启动很慢, 登陆后过一会才出现. 
电源 (会话) 按钮点 "启动应用程序...", 找到 "awn".
点 "编辑", "命令" 栏删除默认的 ` --startup` 参数, 似乎可以解决问题.

## vim

```sh
sed -re '/^\s*set\s+backup/ s#^#"#' /usr/share/vim/vim73/vimrc_example.vim > ~/.vimrc
```

## bcompare

官网 http://www.scootersoftware.com/download.php 下载 Debian 包, 双击安装.
(注: 使用默认推荐的 32 位包, 旧 64 位包会导致安装一堆 32 位兼容软件包).

官网上下载附加格式支持包, "Tools" -> "Import Settings...", 选择需要导入支持的格式.

[UbuntuDesktopLVM]: https://help.ubuntu.com/community/UbuntuDesktopLVM
