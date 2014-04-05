几款 vps 测评
===

因为 [github][] 被封了, 又刚好看到 [阿里云][] 的广告, 就打算买个 vps 玩玩, 
有机会自己搭个 git 服务器, git wiki 也挺好.
买完之外又觉得不能翻墙的 vps 不是好 vps, 
又尝试了下 [photonvps][], [傲游主机][], [buyvm.net][] 几款 vps.
使用测评比较如下.

<table>

<tr>
<th>vps</th> <th>配置性价比</th> <th>网速</th> <th>是否支持 ubuntu 12.04 64bit</th> <th>用户体验</th> <th>综合评价</th>
</tr>

<tr>
<th>阿里云</th> <td>一般, 配置灵活</td> <td>快, 不能翻墙</td> <td>是</td> <td>差</td> <td>一般, 国内推荐</td>
</tr>

<tr>
<th>photonvps</th> <td>一般</td> <td>慢, 可翻墙</td> <td>是</td> <td>一般</td> <td>一般</td>
</tr>

<tr>
<th>傲游主机</th> <td>一般</td> <td>香港 vps 较快, 可翻墙</td> <td>否</td> <td>较好</td> <td>一般</td>
</tr>

<tr>
<th>buyvm.net</th> <td>超值</td> <td>慢, 可翻墙</td> <td>是, 迷你定制版, 自建仓库镜像</td> <td>较好</td> <td>推荐</td>
</tr>

</table>

写这篇文章主要是为了大赞一下 [buyvm.net][].
唯一缺点就是网络较慢, 但似乎是我大天朝的问题, 这也是推荐 [阿里云][] 的原因.
其他两个已申请退款, 要想兼顾速度与翻墙, 也许香港 vps 才是出路.
傲游主机不支持 ubuntu 12.04 64bit 是硬伤.

## 硬件配置

除了 [buyvm.net][] 配置超值, 其他几家都差不多, [阿里云][] 似乎略贵, 但配置调整灵活.

附加服务方面:
* [阿里云][] 送备份和快照等服务.
* [buyvm.net][] 送最近 7 天每天自动备份一次, 不送快照.
* [傲游主机][] 好像备份和快照都要额外收费.
* [photonvps][] 没注意, 忘了.

另外, [阿里云][] 和 [buyvm.net][] 都显示有内部 IP 和外部 IP, 其他两个好像只有外部 IP ?

## 是否支持 ubuntu 12.04 64bit

* [傲游主机][] 支持的系统较少, ubuntu 只有 10.10 32bit, 客服说可以退款.
* [buyvm.net][] 支持的系统超多, ubuntu 全系列当然不在话下, 
尝试了 ubuntu 12.04 minimal 定制版, 感觉超赞, 绝对是服务器首选, 
并且自建了 ubuntu 仓库镜像, 软件下载安装那叫一个飞快, **严重加分**.
* [阿里云][] 支持的系统很少, 恰好包含 ubuntu 12.04.
* [photonvps][] 主流 linux 系统版本基本包含.

## 用户体验

* 为什么给 [阿里云][] 打差:
	* 界面有点找不着北.
	* 提单选来选去麻烦, 
	* 找不到查看工单的入口
	* 回答太官腔生硬, 最后一个回答是 "root 权限都给你了, 自己 google 解决", 好吧, 几十块钱的产品我也不能要求什么.
* [buyvm.net][] vps 查看管理方便, 工单提交与查看方便, 响应较快, 正面回答解决问题.
* [傲游主机][] 也还好, 退款爽快.
* [photonvps][] 也还好, 就是退款磨磨蹭蹭.

[github]: https://github.com/
[阿里云]: http://www.aliyun.com/product/ecs/
[photonvps]: http://www.photonvps.com/linux.html
[傲游主机]: http://www.aoyouhost.com/
[buyvm.net]: http://buyvm.net/

