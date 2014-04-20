使用 byobu 配置简单优化 screen 和 tmux
===

byobu 为 screen 和 tmux 提供了美化定制的配置文件.
但是:

0. 公司机器上不能安装 byobu.
0. 只想要其中几个核心配置效果.
0. 不想为了使用几个配置而安装一个软件包.

研究下 byobu 的定制配置 (ubuntu 12.04.4, byobu 5.17), 
把我们想要的核心配置提取出来, 
就可以在各种环境简单使用这些配置美化 screen 或 tmux.

## screen 配置

byobu 的 screen 主要配置文件是 `usr/share/byobu/profiles/common`,
screen 用户默认配置文件是 `~/.screenrc`.

提取如下几条配置就可以简单优化 screen.

0. 不要显示启动消息
0. 关掉闪屏
0. 默认支持 Unicode UTF-8
0. 添加显示任务栏

```sh
# Now, let's override with our customizations
startup_message off
vbell off
defutf8 on

# Window tabs, second to last line
caption always "%1001`%?%-Lw%50L>%?%{=r}%n*%f %t%?(%u)%?%{-}%12`%?%+Lw%?%11` %=%12`%1002`%10`%<"
```

## tmux 配置

byobu 的 tmux 主要配置文件是 `usr/share/byobu/profiles/tmux`.
看 `man tmux`, tmux 配置可用 `-f` 参数指定,
默认是 `/etc/tmux.conf` 和 `~/.tmux.conf`.

tmux 默认已经带状态栏, 可以使用如下配置简单优化 tmux.

0. 兼容 screen 快捷键
0. 日期时间格式优化
0. 运行 tmux 时保留 gnome-terminal 的滚动条

```sh
set -s escape-time 0

# Set the prefix to ^A.
unbind C-b
set -g prefix ^A
bind a send-prefix

# keys
set -g mode-keys vi
set -g status-keys vi

# date time
set -g status-interval 1
set -g status-right "%F %H:%M"
set -g clock-mode-style 24

# term
set -g terminal-overrides "xterm*:smcup@:rmcup@"
```

## tmux 配置比较

可以按下列操作将 tmux 的 `options` 保存到文件, 比较 byobu 配置和默认配置的差异.

* 执行 `show -g` 命令显示所有选项
* 选中复制所有选项
* 执行 `saveb tmux.conf` 将选项保存到文件

忽略颜色设置等差异, 我们可能关心的差异有如下几点.
注释掉的设置表示 `tmux` 默认.

```
# 设置 gnome-terminal 窗口标题栏
#set -g set-titles off
#set -g set-titles-string "#S:#I:#W - "#T""
set -g set-titles on
set -g set-titles-string "#(whoami)@#H - byobu (#S)"

# 修改键绑定为 vi
#set -g status-keys emacs
set -g status-keys vi

# 修改状态栏
#set -g status-left "[#S]"
#set -g status-left-length 10
#set -g status-right ""#22T" %H:%M %d-%b-%y"
#set -g status-right-length 40
set -g status-left "#(byobu-status tmux_left)"
set -g status-left-length 256
set -g status-right "#(byobu-status tmux_right)"
set -g status-right-length 256

# 设置这个会保留 gnome-terminal 的滚动条
#set -g terminal-overrides "*88col*:colors=88,*256col*:colors=256,xterm*:XT:Ms=\E]52;%p1
set -g terminal-overrides "xterm*:smcup@:rmcup@"
```

再看 `show -s` 有如下差异:

```sh
#escape-time 500
escape-time 0
```

## tmux 笔记

首先找一台机器安装运行 byobu, 执行 `pstree -psa $$` 查看当前启动 byobu 的命令行.

```sh
hanyong@hk:~/.byobu$ pstree -psa $$
init,1
  └─tmux,10206 -2 -f /usr/share/byobu/profiles/tmuxrc new-session ...
      └─sh,10208 -c /usr/bin/byobu-shell
          └─bash,10212
              └─pstree,30207 -psa 10212
```

可看到 byobu 默认使用的 backend 是 tmux, 
看了下 `/etc/byobu/backend` 配置:

```sh
# BYOBU_BACKEND can currently be "screen" or "tmux"
# Override this on a per-user basis by editing "$BYOBU_CONFIG_DIR/backend"
# or by launching either "byobu-screen" or "byobu-tmux" instead of "byobu".
#BYOBU_BACKEND="tmux"
```

建议通过 `$BYOBU_CONFIG_DIR/backend` 修改用户 backend, 
或者运行 `byobu-screen`, `byobu-tmux` 指定 backend.
分别试了下, `tmux` 会保留滚动条, 状态栏也更简洁, 感觉 `tmux` 要好些.

看一下命令行指定的 tmux 配置 `/usr/share/byobu/profiles/tmuxrc` 文件:

```sh
source-file $HOME/.byobu/color.tmux
source-file $BYOBU_CONFIG_DIR/profile.tmux
source-file $BYOBU_CONFIG_DIR/keybindings.tmux
source-file $HOME/.byoburc.tmux
```

只是简单导入几个其他配置.
这里猜到 `$BYOBU_CONFIG_DIR` 应该就是 `$HOME/.byobu`,

看一下 `keybindings.tmux` 只有以下简单几行:

```sh
unbind-key -n C-a
set -g prefix ^A
set -g prefix2 ^A
bind a send-prefix
```

这个文件在 `profile.tmux` 之后加载, 只是用来覆盖 `profile.tmux` 的 `C-a` 键绑定.

再看一下 `profile.tmux`, 又直接引用了 `$BYOBU_PREFIX/share/byobu/profiles/tmux`,
即 `/usr/share/byobu/profiles/tmux`, 这个才是 tmux 真正的主要配置文件.

看一下这个文件, 开头是这几行:

```sh
# Initialize environment, clean up
set-environment -g BYOBU_BACKEND tmux
new-window -d byobu-janitor
set -s escape-time 0
```

然后看到这几行:

```sh
# Change to Screen's ctrl-a escape sequence
source /usr/share/doc/tmux/examples/screen-keys.conf
# On Archlinux, this file is not under the same directory
source /usr/share/tmux/screen-keys.conf

# Add F12 to the prefix list
set -g prefix ^A,F12
```

`tmux` 默认快捷键是 `Ctrl + B`, byobu 改成了兼容 screen 的 `Ctrl + A`.
这里是直接引用了 `tmux` 自己的兼容 `screen` 快捷键配置.

再从 `screen-keys.conf` 看到如下内容.
screen 我主要是 `Ctrl + A` 用的比较熟, 下面还有很多内容我就不关心了.

```sh
# Set the prefix to ^A.
unbind C-b
set -g prefix ^A
bind a send-prefix
```

继续看 `/usr/share/byobu/profiles/tmux`, 可能会关注的有这些:

```sh
set-option -g set-titles on
set-option -g set-titles-string '#(whoami)@#H - byobu (#S)'
set-option -g history-limit 10000
set-option -g display-panes-time 150
set-option -g clock-mode-style 24
set-option -g mode-keys vi

set -g status-interval 1
set -g status-left-length 256
set -g status-right-length 256
set -g status-left '#(byobu-status tmux_left)'
set -g status-right '#(byobu-status tmux_right)'
```

看了下 `byobu-status` 也是个脚本:

```sh
hanyong@hk:~/.byobu$ which byobu-status
/usr/bin/byobu-status
hanyong@hk:~/.byobu$ file /usr/bin/byobu-status
/usr/bin/byobu-status: POSIX shell script, ASCII text executable
```

这个脚本导入了 `status`, `statusrc` 等文件, 后面的逻辑较复杂, 暂略过.
`status` 文件定义了如下内容:

```sh
# Tmux has one status line, with 2 halves for status
tmux_left="logo #distro release #arch"
# You can have as many tmux right lines below here, and cycle through them using Shift-F5
tmux_right="#network #disk_io #custom #entropy raid reboot_required updates_available #apport #services #mail #users uptime #ec2_cost #rcs_cost #fan_speed #cpu_temp #battery #wifi_quality #processes load_average cpu_count cpu_freq memory #swap #disk #whoami #hostname #ip_address #time_utc date time"
```

好像 "#" 开头的是命令或函数调用, 非 "#" 开头的是内置命令 ?
看了下 tmux 的文档, "status-left" (及 "status-right") 只支持命令替换和几个简单参数.
status 文件解析应该是 byobu 特有的行为.
将 byobu deb 包解开后 grep, 找到 memory 等相关脚本在 `usr/lib/byobu/` 目录下.

