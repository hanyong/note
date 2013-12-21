git 高级技巧
===

## 从指定版本开始 clone 代码

以 [gollum](https://github.com/gollum/gollum) 为例,
目前最新版 tag 是 "v2.5.2", 使用浅 clone 的拉取一份快照到本地.

```sh
observer.hany@ali-59375nm:~/workspace/third$ git init gollum
Initialized empty Git repository in /home/observer.hany/workspace/third/gollum/.git/
observer.hany@ali-59375nm:~/workspace/third$ cd gollum/
observer.hany@ali-59375nm:~/workspace/third/gollum$ git remote add origin git@github.com:gollum/gollum.git
observer.hany@ali-59375nm:~/workspace/third/gollum$ git ls-remote --tags origin
... ...
31dfcbaa9ee8d543115fd72f330b1f5ad8ef2b3d	refs/tags/v2.4.9
9c714e768748db4560bc017cacef4afa0c751a63	refs/tags/v2.5.0
5a9af4005887b7c92fe5414847beb7373232eae8	refs/tags/v2.5.1
714985e37750e640b64467f1a58be029c1e28882	refs/tags/v2.5.2
observer.hany@ali-59375nm:~/workspace/third/gollum$ git fetch --depth 1 origin refs/tags/v2.5.2:refs/tags/v2.5.2
remote: Counting objects: 821, done.
remote: Compressing objects: 100% (556/556), done.
remote: Total 821 (delta 228), reused 592 (delta 192)
Receiving objects: 100% (821/821), 1.12 MiB | 420 KiB/s, done.
Resolving deltas: 100% (228/228), done.
From github.com:gollum/gollum
 * [new tag]         v2.5.2     -> v2.5.2
observer.hany@ali-59375nm:~/workspace/third/gollum$ git reset --hard v2.5.2
HEAD is now at 714985e Release 2.5.2
observer.hany@ali-59375nm:~/workspace/third/gollum$ ls
bin        Gemfile         Home.md  licenses  README.md
config.rb  gollum.gemspec  lib      openrc    templates
docs       HISTORY.md      LICENSE  Rakefile  test
```

tag 应该是在 master 分支上的, 尝试从 tag 开始拉取 master 最新修改.

```sh
observer.hany@ali-59375nm:~/workspace/third/gollum$ git update-ref refs/remotes/origin/master v2.5.2
observer.hany@ali-59375nm:~/workspace/third/gollum$ git branch --set-upstream master origin/master 
Branch master set up to track remote branch master from origin.
observer.hany@ali-59375nm:~/workspace/third/gollum$ git pull --ff-only
Updating 714985e..cb4471b
Fast-forward
 bin/gollum                                         |    5 +++++
 lib/gollum/app.rb                                  |    9 ++++-----
 .../public/gollum/javascript/gollum.dialog.js      |    1 +
 test/test_app.rb                                   |    3 ++-
 4 files changed, 12 insertions(+), 6 deletions(-)
```

