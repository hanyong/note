ipv6 导致 "ssh -X" 失败
===

使用 `ssh -X` 登录服务器出现如下错误:

```sh
X11 forwarding request failed on channel 0
```

查看 `/etc/ssh/sshd_config`, 允许 X11 转发已经是打开的.

```sh
X11Forwarding yes
```

网上查到该问题, `/var/log/auth.log` 下有如下错误:

```sh
Apr  4 21:20:46 AY140330144942734002Z sshd[24663]: error: Failed to allocate internet-domain X11 display socket.
```

原因是 `sshd` 尝试绑定到 ipv6 时失败, 解决办法是 `sshd_config` 添加如下配置:

```sh
AddressFamily inet
```

然后重启 `sshd` 服务:

或者正确设置系统 ipv6 ?

相关链接:
* http://ibohm.blogspot.com/2011/12/failed-to-allocate-internet-domain-x11.html
* https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=422327

