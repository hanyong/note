ubuntu服务器安装桌面环境
===

想在 ubuntu 服务器上安装桌面环境, 但是不想用 ubuntu 默认的 unity 桌面.

首先安装 `gnome`, 其包含了 gnome 桌面环境的许多组件, 其中包含 gnome3 桌面 `gnome-session`.
由于 X-Windows 是客户端, 服务器结构, 安装 gnome 时只是安装客户端包, 不会安装 xserver.

有了 session 后, 还需要一个欢迎界面.
想想登陆 ubuntu 桌面时, 先要有个欢迎界面, 选择要登陆的 session 类型, 输入用户名和密码.
这可以选择安装 `lightdm-gtk-greeter` 或 ubuntu 默认的 `unity-greeter`.
安装了 greeter 后, 还是可以没有安装 xserver.

接下来需要一个显示管理器, 这里可以安装 `lightdm`.
注意, 安装 `lightdm` 时会推荐安装 `xserver-xorg`, 即 xserver.
这里依然可以给 aptitude 添加 `-R` 参数不安装 xserver.
不过不安装 xserver lightdm 将无法启动, 所以还是安装.

之后再启动电脑, 就会启动 xserver, 到达 greeter 的欢迎屏幕了.

要卸载桌面环境, 首先停止 lightdm 服务, `sudo service lightdm stop`,
这时可看到图形界面消失. 
然后卸载 lightdm 和 xserver, 就卸载掉图形桌面了.
但是客户端还保留.
通过 `ssh -X` 或者 nomachine, 还是可以启动图形软件和桌面.
但是无法启动到欢迎屏幕了. 
nomachine 默认启动的虚拟桌面总是 gnome3 桌面.
