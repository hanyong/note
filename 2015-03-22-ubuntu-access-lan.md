ubuntu 访问局域网机器
===

本文基于 ubuntu 12.04 .

同一个局域网中的两台机器, 可通过 `${HOSTNAME}.local` 相互访问.
如:

```sh
ssh ali-59375n.local
```

参考: https://help.ubuntu.com/community/HowToZeroconf , http://www.zeroconf.org/ .

局域网中的机器通常使用 DHCP 动态获取 IP 地址,
为了避免 ssh 经常提示主机 IP 变化的警告,
可在 `~/.ssh/config` 文件添加如下配置:

```
Host *.local
	CheckHostIp no
```
