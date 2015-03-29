#!/usr/bin/python2
# -*- encoding: utf-8 -*-

import sys, os, subprocess
import urlparse

DEFAULT_MIRROR = \
r"http://mirrors.ustc.edu.cn/ubuntu/"
#r"http://mirrors.aliyun.com/ubuntu/"
#r"http://mirrors.163.com/ubuntu/"

noMirrorList = [
	"archive.canonical.com",
	"extras.ubuntu.com",
	]

def main(mirror):
	codename = subprocess.check_output(["lsb_release", "-sc",]).strip()
	catalogList = [ codename + e for e in [ 
		"", 
		"-security", # 重要安全更新
		"-updates", # 推荐更新
		"-proposed", # 提前释放出的更新
		"-backports", # 不支持的更新
		]]
	print >>sys.stderr, mirror + "\n" + repr(catalogList)
	out = open("/etc/apt/sources.list.new", "wb")
	f = open("/etc/apt/sources.list", "rb")
	for line in f:
		comment = 0
		for c in line:
			if c in "# \t":
				comment += 1
			else:
				break
		comment = line[:comment]
		tokenList = line[len(comment):].split(" ", 3)
		if not tokenList[0] in [ "deb", "deb-src", ]:
			print >>out, line,
		elif tokenList[1].startswith("cdrom:"):
			print >>out, line,
		else:
			(deb, url, catalog, stream) = tokenList
			if urlparse.urlsplit(url).hostname not in noMirrorList:
				if catalog in catalogList:
					url = mirror
			if url != mirror:
				if not comment.startswith("#"):
					comment = "#" + comment
			print >>out, comment + deb, url, catalog, stream,
	f.close()
	out.close()
	subprocess.check_call(["mv", "-Tb", "sources.list.new", "sources.list"], cwd="/etc/apt/")

if __name__ == '__main__':
	if len(sys.argv) > 1:
		mirror = sys.argv[1]
	else:
		mirror = DEFAULT_MIRROR
	main(mirror)

