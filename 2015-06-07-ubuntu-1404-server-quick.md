ubuntu 1404 server quick
===

官方文档参考: https://help.ubuntu.com/lts/installation-guide/amd64/index.html

从 `ubuntu-releases` 和 `ubuntu` 镜像网站下载安装 CD 和硬盘安装文件.
安装 CD 必须放在分区根目录,
要求安装程序可识别分区文件系统, `fat32`, `ntfs`, `ext3`, `ext4` 应该都可以, lvm 未测试.
硬盘安装文件任意目录均可.
硬盘安装文件会尝试在所有分区根目录查找光盘镜像.

```sh
cd /
#wget --continue 'http://ftp.cuhk.edu.hk/pub/Linux/ubuntu-releases/trusty/ubuntu-14.04.2-server-amd64.iso'
wget --continue 'http://mirrors.ustc.edu.cn/ubuntu-releases/trusty/ubuntu-14.04.2-server-amd64.iso'
mkdir -p /install
cd /install
#wget --continue 'http://ftp.cuhk.edu.hk/pub/Linux/ubuntu/dists/trusty/main/installer-amd64/current/images/hd-media/vmlinuz'
#wget --continue 'http://ftp.cuhk.edu.hk/pub/Linux/ubuntu/dists/trusty/main/installer-amd64/current/images/hd-media/initrd.gz'
wget --continue 'http://mirrors.ustc.edu.cn/ubuntu/dists/trusty/main/installer-amd64/current/images/hd-media/vmlinuz'
wget --continue 'http://mirrors.ustc.edu.cn/ubuntu/dists/trusty/main/installer-amd64/current/images/hd-media/initrd.gz'
```

grub 添加硬盘安装启动配置. 

grub4dos menu.lst 可添加如下配置:

```sh
title ubuntu-14.04.2-server-amd64 install
find --set-root /install/vmlinuz
kernel /install/vmlinuz
initrd /install/initrd.gz
```

ubuntu 下 grub2 可在 `/etc/grub.d/41_custom` 末尾添加如下配置:

```
for iso in /ubuntu-*-server-*.iso ; do
        dir="${iso%.iso}"
        name="$(basename $dir)"
        vm=$(ls "/install/vmlinuz"*)
        init=$(ls "/install/initrd"*)
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
done
```
