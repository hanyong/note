ubuntu 12.04
===

## 全局

```sh
# aptitude 基本工具
sudo apt-get update
sudo apt-get install -y aptitude
sudo aptitude install -y dconf-tools
sudo aptitude install -y gconf-editor

# git
sudo add-apt-repository -y ppa:git-core/ppa
sudo aptitude install -y git gitk git-cola

# gnome classic
sudo aptitude remove -y indicator-appmenu
sudo aptitude remove -y overlay-scrollbar liboverlay-scrollbar3-0.2-0 liboverlay-scrollbar-0.2-0
sudo aptitude install -y gnome-panel
sudo aptitude install -y indicator-applet indicator-applet-session
#注销, 登陆界面选择 "GNOME Classic (No effects)" 进入系统.

# awn dock.
sudo aptitude install -R -y avant-window-navigator awn-settings libdesktop-agnostic-cfg-gconf
#`-R` 避免安装一堆用不着的 awn 推荐依赖. 
#`libdesktop-agnostic-cfg-gconf` 避免显示绿加号的 bug.

# vim
sudo aptitude install -y vim vim-gnome
sudo tee /etc/vim/vimrc.local <<EOF
set ts=4 sw=4 nu
set nobackup
set backupdir=~/tmp,/tmp,.
EOF
#>
```

## 个人

## gedit

"编辑" -> "首选项".
* "查看" tab, 勾选 "显示行号", 取消 "启用自动换行".
* "编辑器" tab, "制表符宽度" 修改为 "4", 取消 "在保存前创建备份文件".

## gnome-terminal

"编辑" -> "配置文件首选项".

* "颜色" tab, 取消 "使用系统主题中的颜色", "内置方案" 选择 "白底黑字".

## sunpinyin

运行 `/usr/lib/ibus-sunpinyin/ibus-setup-sunpinyin`.
* "Keyboard" tab, "Page Flip" 选中 "- / =", "[ / ]".
* "General" tab, "Character Set" 选择 "GB18030" (或保持默认 "GBK").

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
```

## gnome classic

* move min/max/close buttons

```sh
gconftool-2 --set "/apps/metacity/general/button_layout" --type string ":minimize,maximize,close"
```

* Run dialog

```sh
gconftool-2 --set "/apps/metacity/global_keybindings/panel_run_dialog" --type string "<Alt>F2"
```

* update-notifier

```sh
gsettings set com.ubuntu.update-notifier auto-launch false
```

* datetime

```
gsettings set com.canonical.indicator.datetime show-calendar false
gsettings set com.canonical.indicator.datetime show-clock false
gsettings set com.canonical.indicator.datetime show-events false
```

## firefox

运行 `firefox -P`, "Create Profile...", name "default", 
"Choose Folder...", "~/var/firefox/default", "Finish".
"Start Firefox".

"编辑" -> "首选项".

* 常规 tab, "启动 Firefox 时" 选择 "显示上次打开的窗口和标签页".
"下载" 选择 "总是询问保存文件的位置".
* 高级 tab, "证书", 设置 "自动选择一个", "查看证书" -> "您的证书" -> "导入...", 选择个人 p12 证书文件.
弹出 "修改主密码", 保留为空, 直接点 "确定", 弹出警告, 再确定.
弹出密码输入对话框, 输入证书密码, 点 "确定".

## 任务栏

### 桌面切换
* 右键, "首选项", "工作区的数量" 修改为 "1".
* "Alt" + 右键, "从面板上删除".

### 完整指示器

* "Alt" + 右键, "Move", 拖到右下角面板上.

运行 `dconf-editor`, 展开 `com.canonical.indicator.datetime`, 
取消所有显示, 即取消 "show-calendar", "show-clock" 和 "show-events".
或者用 gsettings, 见 "gnome classic" -> "datetime" 命令.

**TODO**: 取消会话管理的用户名显示. 用户完整名字设置为空可避免显示用户名.

添加 "时钟" 到面板.

OR:

* 删除 "完整指示器", 依次添加 "指示器小程序", "时钟" 和 "指示器小程序会话" 到右下角.

### 显示桌面

* "Alt" + 右键, "移动", 拖到最右下.

### 顶面板

* "Alt" + 右键, "删除该面板", 弹出确认对话框, 点 "删除".

### awn dock

底面板取消扩展, 拖到右下角.

运行 `avant-window-navigator`.

* "首选项", "Size of icons" 设置为 "40" pixels.
"Position on the screen" 设置为 "左边".
勾选 "Start Awn automatically".
* "Task Manager", 取消 "Group common windows".
* "Applets" 设置仅需要保留 "Cairo Main Menu", "分隔符", "任务管理器" 3 项.
"Cairo Main Menu" 旁边带的 "Places" 上右键选择 "Remove Icon" 去掉这个图标.
* "Advanced", "Offset" 设置为 "7".

awn 设置好后删除底面板上的 "task list".

## vim

```sh
sed -re '/^\s*set\s+backup/ s#^#"#' /usr/share/vim/vim73/vimrc_example.vim > ~/.vimrc
```

