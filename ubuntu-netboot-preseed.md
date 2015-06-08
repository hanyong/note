```
mkdir netboot
cd netboot
wget http://mirrors.ustc.edu.cn/ubuntu/dists/trusty-updates/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/linux
wget http://mirrors.ustc.edu.cn/ubuntu/dists/trusty-updates/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/initrd.gz
```

```
menuentry 'ubuntu netboot' {
    search --file --set=root /netboot/linux
    linux /netboot/linux auto=true locale=en_US.UTF-8 \
        console-setup/ask_detect=false keyboard-configuration/layoutcode=us \
        netcfg/disable_autoconfig=true \
        netcfg/get_nameservers string 8.8.8.8 \
        netcfg/get_ipaddress string 118.193.215.39 \
        netcfg/get_netmask string 255.255.255.128 \
        netcfg/get_gateway string 118.193.215.1 \
        netcfg/confirm_static boolean true \
        netcfg/get_hostname=han-ubu netcfg/get_domain=oolap.com \
        url= \
        anna/choose_modules=network-console \
        network-console/password=r00tme network-console/password-again=r00tme \
        mirror/protocol=http mirror/country=manual \
        mirror/http/hostname=mirrors.ustc.edu.cn \
        mirror/http/directory=/ubuntu \
        mirror/http/proxy=
    initrd /netboot/initrd.gz
}
```

```
# Ignore questions with a priority less than:
# Choices: critical, high, medium, low
debconf debconf/priority        select  high

# System locale:
# Choices: en_US.UTF-8, en_US.UTF-8
d-i     debian-installer/locale select  en_US.UTF-8
# Optionally specify additional locales to be generated.
#d-i localechooser/supported-locales zh_CN.UTF-8

# Keyboard selection.
# Disable automatic (interactive) keymap detection.
d-i console-setup/ask_detect boolean false
#d-i keyboard-configuration/modelcode string pc105
d-i keyboard-configuration/layoutcode string us

# Disable network configuration entirely. This is useful for cdrom
# installations on non-networked devices where the network questions,
# warning and long timeouts are a nuisance.
#d-i netcfg/enable boolean false

# netcfg will choose an interface that has link if possible. This makes it
# skip displaying a list if there is more than one interface.
d-i netcfg/choose_interface select auto

# To pick a particular interface instead:
#d-i netcfg/choose_interface select eth1

# If you prefer to configure the network manually, uncomment this line and
# the static network configuration below.
d-i netcfg/disable_autoconfig boolean true

# If you want the preconfiguration file to work on systems both with and
# without a dhcp server, uncomment these lines and the static network
# configuration below.
#d-i netcfg/dhcp_failed note
#d-i netcfg/dhcp_options select Configure network manually

# Static network configuration.
d-i netcfg/get_nameservers string 8.8.8.8
d-i netcfg/get_ipaddress string 118.193.215.39
d-i netcfg/get_netmask string 255.255.255.128
d-i netcfg/get_gateway string 118.193.215.1
d-i netcfg/confirm_static boolean true

# Any hostname and domain names assigned from dhcp take precedence over
# values set here. However, setting the values still prevents the questions
# from being shown, even if values come from dhcp.
d-i netcfg/get_hostname string hk
d-i netcfg/get_domain string oolap.com

# Disable that annoying WEP key dialog.
d-i netcfg/wireless_wep string
# The wacky dhcp hostname that some ISPs use as a password of sorts.
#d-i netcfg/dhcp_hostname string radish

# If non-free firmware is needed for the network or other hardware, you can
# configure the installer to always try to load it, without prompting. Or
# change to false to disable asking.
d-i hw-detect/load_firmware boolean false

# Use the following settings if you wish to make use of the network-console
# component for remote installation over SSH. This only makes sense if you
# intend to perform the remainder of the installation manually.
d-i anna/choose_modules string network-console
#d-i network-console/password password r00tme
#d-i network-console/password-again password r00tme
# Use this instead if you prefer to use key-based authentication
d-i network-console/authorized_keys_url /authorized_keys

# If you select ftp, the mirror/country string does not need to be set.
#d-i mirror/protocol string ftp
d-i mirror/country string manual
d-i mirror/http/hostname string archive.ubuntu.com
d-i mirror/http/directory string /ubuntu
d-i mirror/http/proxy string
```
