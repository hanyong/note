ubuntu 搭建 OpenVPN 服务器
===

## 服务器设置

首先按照 [OpenVPN 指南][] 进行设置.

执行 `sudo service openvpn start` 启动服务时出现如下错误:

```sh
: ERROR while getting interface flags: No such device
SIOCSIFDSTADDR: No such device
: ERROR while getting interface flags: No such device
SIOCSIFMTU: No such device
```

网上搜索了一下, 大概是 vps 服务器要开启 "tun". 
登录 VPS 管理控制台, 正好看到有 "TUN/TAP" 选项, 默认为 "OFF".
设置为 "ON" 后 vps 重启, 重新登录上去, 启动 openvpn 服务成功.

## 客户端设置

客户端安装 `sudo aptitude install network-manager-openvpn-gnome`, 
拷贝上一步生成的 client 证书等文件到本地, 设置 openvpn 客户端后连接成功.

连接 openvpn 后所有网站都打不开了, 看了下路由表, 似乎所有路由都走了 vpn 网络:

```sh
hanyong@han:~$ netstat -rn
内核 IP 路由表
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         10.8.0.5        0.0.0.0         UG        0 0          0 tun0
10.8.0.1        10.8.0.5        255.255.255.255 UGH       0 0          0 tun0
10.8.0.5        0.0.0.0         255.255.255.255 UH        0 0          0 tun0
123.103.241.126 192.168.100.1   255.255.255.255 UGH       0 0          0 eth0
169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth0
192.168.100.0   0.0.0.0         255.255.255.0   U         0 0          0 eth0
```

找到 vpn 设置的 "路由..." 设置, 勾选上 "仅将此连接用于相对应的网络上的资源", 
重新连接 vpn, 其他网站可以正常访问了, 这时查看路由表如下:

```sh
hanyong@han:~$ netstat -rn
内核 IP 路由表
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         192.168.100.1   0.0.0.0         UG        0 0          0 eth0
10.8.0.1        10.8.0.5        255.255.255.255 UGH       0 0          0 tun0
10.8.0.5        0.0.0.0         255.255.255.255 UH        0 0          0 tun0
123.103.241.126 192.168.100.1   255.255.255.255 UGH       0 0          0 eth0
169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth0
192.168.100.0   0.0.0.0         255.255.255.0   U         0 0          0 eth0
```

`ping 10.8.0.1` 还是不通.
服务器端 `/var/log/syslog` 看到如下两条警告日志:

```sh
Apr  7 12:49:00 hk ovpn-server[816]: 115.193.183.247:48175 WARNING: 'link-mtu' is used inconsistently, local='link-mtu 1542', remote='link-mtu 1541'
Apr  7 12:49:00 hk ovpn-server[816]: 115.193.183.247:48175 WARNING: 'comp-lzo' is present in local config but missing in remote config, local='comp-lzo'
```

查看客户端 vpn 设置, 勾选上 "使用 LZO 压缩".
再次连接后这两个警告日志没有了, 同时再试 `ping 10.8.0.1` 可以 ping 通了.

## 命令行登录

拷贝客户端证书到 `~/etc/openvpn/` 目录.
将 `client.conf` 也拷贝到此目录.

```sh
cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ./
```

注释掉 `remote` 设置, 可运行时从命令行指定, 方便切换 vpn 服务器. 
修改客户端证书设置为正确的证书文件名.

```sh
;remote my-server-1 1194
;remote my-server-2 1194

ca ca.crt
cert client1.crt
key client1.key
```

openvpn 既是服务器也是客户端, 使用客户端配置即可启动客户端连接服务器.

```sh
sudo openvpn --config ./client.conf --remote us.oolap.com
```

使用命令行登录时, 默认只有 `10.8.0.0/8` 子网走 vpn 连接, 查看路由表与上述类似.

```sh
hanyong@han:~$ netstat -rn
内核 IP 路由表
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         192.168.100.1   0.0.0.0         UG        0 0          0 eth0
10.8.0.0        10.8.0.5        255.255.255.0   UG        0 0          0 tun0
10.8.0.5        0.0.0.0         255.255.255.255 UH        0 0          0 tun0
169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth0
192.168.100.0   0.0.0.0         255.255.255.0   U         0 0          0 eth0
```

>注意有一点区别, 路由表少了一项:
```sh
123.103.241.126 192.168.100.1   255.255.255.255 UGH       0 0          0 eth0
```

openvpn 服务器端打开如下设置, 
命令行客户端就会优先 vpn 路由, 类似 "network-manager" 默认设置.
经测试这段设置只对命令行客户端有效, "network-manager" 只由客户端设置决定.

```sh
push "redirect-gateway def1 bypass-dhcp"
```

路由表如下:

```sh
hanyong@han:~$ netstat -rn
内核 IP 路由表
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         10.8.0.5        128.0.0.0       UG        0 0          0 tun0
0.0.0.0         192.168.100.1   0.0.0.0         UG        0 0          0 eth0
10.8.0.0        10.8.0.5        255.255.255.0   UG        0 0          0 tun0
10.8.0.5        0.0.0.0         255.255.255.255 UH        0 0          0 tun0
123.103.241.126 192.168.100.1   255.255.255.255 UGH       0 0          0 eth0
128.0.0.0       10.8.0.5        128.0.0.0       UG        0 0          0 tun0
169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth0
192.168.100.0   0.0.0.0         255.255.255.0   U         0 0          0 eth0
```

这个路由表与 GUI 设置只走 vpn 时有一些差异.
另外 GUI 只走 vpn 时 dns 也无法解析, 命令行时可以解析 dns 的.

## 使用 vpn 翻墙

默认情况下 vpn 只是用来访问私有子网.
要使用 vpn 翻墙, 参考 [how-to-set-up-openvpn-in-a-vps][].
使用 pptpd 参考 [how-to-set-up-a-vpn-in-a-vps][].

0. 首先设置客户端所有网络走 vpn. 
这时会所有网络都连不通, 即前面所说的情况.

0. 设置 vpn 服务器推送 DNS 服务器设置到客户端.

	可使用 google 公共 dns 服务器:

	```sh
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
	```
	
	或 opendns 服务器:

	```sh
push "dhcp-option DNS 208.67.222.222"
push "dhcp-option DNS 208.67.220.220"
	```
	
	这时客户端可以解析 DNS 了, 不过网络还是连不通.

0. vpn 服务器设置 NAT 转发.

	确认服务器支持 IP 转发.

	```sh
hanyong@hk:~$ cat /proc/sys/net/ipv4/ip_forward 
1
	```

	如果不支持, 可编辑 `/etc/sysctl.conf`, 
设置 `net.ipv4.ip_forward=1`, 
执行 `sysctl -p` 使设置生效.

	使用 iptables 设置 NAT 转发 vpn 私有子网请求到 vpn 服务器外网.

	```sh
iptables -t nat -A POSTROUTING -s 10.8.0.0/8 -o venet0 -j SNAT --to 199.195.250.158
	```

	这时, 客户端就可以通过 vpn 访问外网, 实现翻墙了, 即 vpn + nat.

	碰到某 vps 不支持 iptable_nat, 似乎要找 vps 供应商才能解决.
其他信息参考: [VPN via the TUN/TAP device][].

[OpenVPN 指南]: https://help.ubuntu.com/12.04/serverguide/openvpn.html
[VPN via the TUN/TAP device]: http://wiki.openvz.org/VPN_via_the_TUN/TAP_device
[how-to-set-up-a-vpn-in-a-vps]: http://freenuts.com/how-to-set-up-a-vpn-in-a-vps/
[how-to-set-up-openvpn-in-a-vps]: http://freenuts.com/how-to-set-up-openvpn-in-a-vps/

