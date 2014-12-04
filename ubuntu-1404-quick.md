ubuntu 14.04 安装配置快速指导
===

## 安装

### 硬盘启动 LiveCD

下载光盘镜像, 将光盘镜像下 `/casper/{vmlinuz,initrd}*` 两个文件解压出来.

解压后目录结构如下:

```sh
ubuntu-14.04.1-desktop-amd64.iso
ubuntu-14.04.1-desktop-amd64
`-- casper/
    |-- initrd.lz
    `-- vmlinuz.efi
```

使用 "Grub 4 DOS" (或 EasyBCD) 启动光盘镜像.

我的机器上光盘镜像保存在 D 盘 `/home/software/linux/ubuntu-14.04.1-desktop-amd64.iso`,
添加 "Grub 4 DOS" 启动配置如下:

```sh
title Ubuntu 14.04.1 LiveCD
find --set-root /home/software/linux/ubuntu-14.04.1-desktop-amd64.iso
kernel /home/software/linux/ubuntu-14.04.1-desktop-amd64/casper/vmlinuz.efi boot=casper iso-scan/filename=/home/software/linux/ubuntu-14.04.1-desktop-amd64.iso
initrd /home/software/linux/ubuntu-14.04.1-desktop-amd64/casper/initrd.lz
```

重启进入 LiveCD 桌面后执行下列命令卸载镜像挂载分区:

```sh
sudo umount -l /isodevice/
```

### 设置 lvm 分区

14.04 桌面版已经默认支持 lvm 逻辑卷管理,
可使用 lvm 分区.

```sh
# 准备一个启动分区和一个物理卷分区.
# 在我的机器上分别是主分区 `/dev/sda3` 和逻辑分区 `/dev/sda5`.
BOOT_DEV="/dev/sda3"
PV_DEV="/dev/sda5"

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

运行安装程序, 语言选择中文, 手动设置分区, 完成安装.

## 全局设置

### 脚本自动操作

```sh
# 添加额外的源, 如 git, ubuntu kylin
sudo add-apt-repository ppa:git-core/ppa
#sudo add-apt-repository ppa:ubuntukylin-members/ubuntukylin
sudo apt-get update
# 安装一些基本工具
sudo apt-get install -y aptitude
sudo aptitude install -y gconf-editor dconf-editor
sudo aptitude install -y realpath tree
sudo aptitude install -y unrar p7zip-full p7zip-rar

# 系统设置
# inputrc
sudo tee -a /etc/inputrc <<EOF

# mappings for Ctrl-up-arrow and Ctrl-down-arrow for history search
"\e[1;5A": history-search-backward
"\e[1;5B": history-search-forward
EOF
: '>'
# adduser 用户名允许使用 "."
sudo sed -i '/^NAME_REGEX=/ d; /^#NAME_REGEX=/ a \''
NAME_REGEX="^[a-z][-a-z0-9_.]*$"
' /etc/adduser.conf
# 更新系统默认 locale 设置.
# 系统默认 locale 设置保存在 `/etc/default/locale`,
# 为简化修改进程 locale, 只保留 `LANG`, `LANGUAGE` 设置.
grep '^LANG' /etc/default/locale | xargs sudo localectl set-locale
# grub
sudo sed -i -r -e 's/^(GRUB_DEFAULT=).*/\1saved/' /etc/default/grub
sudo update-grub

# gnome-session-flashback
sudo aptitude install -y gnome-session-flashback
sudo aptitude install compiz-plugins compizconfig-settings-manager
#从登陆界面选择 "GNOME Flashback (Compiz)" 进入系统.
sudo aptitude install -y cairo-dock

# vim
# 需要安装 `vim-gnome` 后才能简单在 vim 中复制内容到 gnome 剪贴板.
sudo aptitude install -y vim vim-gnome
sudo tee /etc/vim/vimrc.local <<EOF
set ts=4 sw=4 nu
set et
set nobackup
set backupdir=~/tmp,/tmp,.
EOF
#>

# git
sudo aptitude install -y git gitk git-cola

# wireshark
sudo aptitude install -y wireshark
# 设置非 root 用户可以使用 wireshark, 执行如下命令, 选择 "是".
sudo dpkg-reconfigure wireshark-common

# 搜狗输入法
#sudo aptitude install -y sogoupinyin
# 从搜狗官方网站下载 ".deb" 安装包
sudo aptitude install -y gdebi
gdebi-gtk sogou_pinyin_linux_1.1.0.0037_amd64.deb
#安装完成后从 "系统设置" 打开 "语言支持", 
#将 "键盘输入方式系统" 修改为 "fcitx".
```

### 手动操作

软件中心去掉 "软件商店" 中的收费项目.
参考 [这里](http://askubuntu.com/questions/47997/how-to-remove-the-for-purchase-section-from-the-software-center/404153#404153).

修改文件:

```sh
sudo vim /usr/share/software-center/softwarecenter/db/update.py
```

`def make_doc` 函数开头添加 3 行修改如下:

```py
    def make_doc(self, cache):
        """Build a Xapian document from the desktop info."""
        if self.has_option_desktop("X-AppInstall-Price"):
            if self.get_desktop("X-AppInstall-Price") > 0:
                return
```

## 个人设置

### 手动操作

笔记本设置: "系统设置" -> "电源", 合上盖子时选择 "不处理".

从 "系统设置" 打开 "语言支持", 
将 "键盘输入方式系统" 修改为 "fcitx".

打开搜狗输入法设置, 设置 "隐藏状态栏" (因为测试了下状态栏显示有问题, 不如不要), 
修改使用方括号键翻页.

运行 "ccsm", "特效" 取消 "Animations" 和 "渐隐窗口", 仅保留一个 "窗口装饰" 即可.
"窗口管理" 勾选上 "Static Application Switcher", 支持 "Alt + Tab" 切换窗口.

底下面板删除, 顶上面板取消 "扩展", 拖到又下角, 添加 "显示桌面", 删除 "自定义菜单".

启动 cairo-dock, 使用 OpenGL 选中 "不再提示", 选择 "是".

cairo-dock 配置:

* 基于默认主题 "Default-Single".
	* "Configuration", "行为", "主 Dock 面板的可见性" 设置为 "为 dock 保留的空间",
"鼠标悬停时" 动画选择为空, "在点击时" 动画选择 "脉动"; 
"外观", "主停靠栏外观" 选择 "面板".
	* "附加组件", 除 "应用程序菜单" 外其他全部取消.
	* "Current items", 删除所有不要的启动器和分割符.
"应用程序菜单", "配置", "Display a notification to quickly launch new applications" 取消勾选,
"Show Logout and/or Shutdown" 选择 "Both".

* 切换到 "高级模式".
	* "位置" 调到 "左边" "0.000".
	* "任务条" 取消 "Automatically add a separator", 取消 "组合相同程序的所有窗口".
"最小化窗口的透明度" 设置为 "不透明" "0.000".
"当窗口获得焦点时, 其对应的图标将播放一小段动画" 选择为空.
"中键点击相关应用的动作" 设置为 "无".
"让应用程序图标弹出气泡来提醒您" 取消勾选.
"应用程序将以动画形式引起你的关注" 选择 "繁忙".
	* "系统设置", "面板", "Ratio to apply on icons' size" 设置为 "normal icons" "1.000".
	* "背景", "图片透明度" 设置为 "0.750".
	* "图标", "图标大小" 设置为 "48x48". "图标放大最大大小" 设置为 "1.000".
	* "Illusion", "Global", "Animation on disappearance" 和 "Animation on appearance" 均设置为 "Fade out";
"Fade out", "Duration of the animation" 设置为最小值 "100".
	* "动态图标", "Global", "Repeat these effects until the corresponding application opens" 取消勾选;
"繁忙", "Image size" 设置为 "0.720".

设置完毕后, "Cairo-Dock" 菜单选择 "开机启动 Cairo-Dock".

### 脚本自动操作

```sh
# 为简化修改进程 locale, 删除 `LC_` 相关环境变量设置.
sed -i -e '/^LC_/ d' ~/.pam_environment

# 设置正常滚动条.
gsettings set com.canonical.desktop.interface scrollbar-mode normal
# 标题栏关闭按钮靠右.
gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close'

# 搜索内容时禁止从网上搜索
gsettings set com.canonical.Unity.Lenses remote-content-search none

# vim
sed -re '/^\s*set\s+backup/ s#^#"#' /usr/share/vim/vim74/vimrc_example.vim > ~/.vimrc

# gedit
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

# .profile 添加设置 "export LIBOVERLAY_SCROLLBAR=0", 否则 wireshark 会崩溃.
# 参考: http://www.bictor.com/2014/06/05/wireshark-crashes-in-ubuntu-14-04/
cat <<EOF >> ~/.profile

# fix wireshark crash
export LIBOVERLAY_SCROLLBAR=0
EOF
sudo adduser $USER wireshark
# 添加用户到组后要注销重新登录才能生效.
```

其他相关设置可参考 [12.04 设置](ubuntu-1204-quick).
