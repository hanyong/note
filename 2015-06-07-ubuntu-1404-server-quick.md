ubuntu 1404 server quick
===

官方文档参考: https://help.ubuntu.com/lts/installation-guide/amd64/index.html

从安装镜像解压出 `install/initrd.gz`, `install/vmlinuz` 两个文件.
linux 下可使用如下命令完成:

```sh
sudo mount ubuntu-14.04.2-server-amd64.iso cdrom/
sudo rsync -avR cdrom/./install/{vmlinuz*,initrd*} ubuntu-14.04.2-server-amd64/
sudo umount cdrom/
```

grub 添加硬盘安装启动配置. 

grub4dos menu.lst 可添加如下配置:

```sh
title ubuntu-14.04.2-server-amd64 install
find --set-root /ubuntu-14.04.2-server-amd64/install/vmlinuz
kernel /ubuntu-14.04.2-server-amd64/install/vmlinuz
initrd /ubuntu-14.04.2-server-amd64/install/initrd.gz
```

ubuntu 下 grub2 可在 `/etc/grub.d/41_custom` 末尾添加如下配置:

```
for iso in /ubuntu-*-server-*.iso ; do
        local dir="${iso%.iso}"
        local name="$(basename $dir)"
        local vm=$(ls "$dir/casper/vmlinuz"*)
        local init=$(ls "$dir/casper/initrd"*)
        cat <<EOF
menuentry '$name install' {
        insmod gzio
        insmod part_msdos
        insmod ext2
        #insmod lvm
        set root='hd0,msdos1'
        search --no-floppy --file --set=root $vm
        linux $vm
        initrd $init
}
EOF
```
