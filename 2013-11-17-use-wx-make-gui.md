使用 wxWidgets 开发 GUI 应用程序
===

wxWidgets (http://wxwidgets.org/) 是一个 C++ 图形界面 (GUI) 程序库。
它是一个开源跨平台库, 并且有 Python (wxPython, http://wxpython.org/) 等其他语言移植版本。

wxPython 是比较流行和成熟的一个移植版本, 
可惜截至目前 (2013-11-17) 还不支持 python3, 只有 python2 版本。
Python 版基本与 C++ 版相同, 但针对 python 语言的特点, 
有一些用法和细节上稍微有所区别或改进。
C++ 文档相对比较完善, python 版本没有, 其实也没必要, 维护单独的文档。
结合 C++ 文档和 wxPython API 代码的文档注视, 可以探索 wxPython 的用法。

Ubuntu 12.04 下可使用如下命令安装 wxPython:

```bash
sudo aptitude install python-wxgtk2.8
```

Windows 下可以从官网下载二进制安装包。

### GUI 应用程序基本框架

一个 wxPython GUI 应用程序的基本框架通常如下:

0. 继承 wx.App 类, 实现 OnInit() 方法, 实现应用程序初始化。
窗口控件的创建和组装, 其他系统和服务初始化, 设置事件监听, 显示主窗口。
0. 创建自定义 App 类的 app 对象。OnInit() 方法在应用程序初始化时被调用。
0. 调用 app 的 MainLoop() 方法进入主消息循环。
主循环监听和响应事件, 直到最后一个顶层窗口 (Top Window) 被关闭后退出主循环, 结束程序。

TODO: C++ 不应该在构造函数调用虚函数, C++ 中 OnInit() 被调用的时机? wxPython 和 wxWidgets 的区别?

一个简单 GUI 程序代码示例 (simple.py):

```python
#!/usr/bin/env python

import wx

class App(wx.App):
	def OnInit(self):
		self.frame = wx.Frame(None)
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

def main():
	app = App(False)
	app.MainLoop()

if __name__ == '__main__':
	main()
```


### MVC 分离

虽然可以用手写代码控制窗口控件创建和组装,
使用图形化工具设计界面通常更直观更简单。
可以使用的有商业软件 [DialogBlocks](http://www.anthemion.co.uk/dialogblocks)
和开源软件 [wxFormBuilder](http://wxformbuilder.org/), 
[wxGlade](http://wxglade.sourceforge.net/),
[XRCed](http://xrced.sf.net/) 等。

我试用过 wxFormBuilder 和 wxGlade, XRCed。
wxFormBuilder 整体感觉更简单易用。

Ubuntu 12.04 下可以使用如下命令安装 wxFormBuilder:

```bash
sudo aptitude install wxformbuilder
```

Windows 下可以从官网下载二进制安装包。

wxFormBuilder 可以产生创建图形界面的程序源码或者 XRC 资源文件。
但设计结果使用自定义的私有 XML 格式 ".fbp" 文件保存。
这是一个两阶段的过程, ".fbp" 文件是一个中间文件, 一个 ".fbp" 文件对应产生一组源码。
一个 ".fbp" 文件叫做一个 "Project", 这个名字稍微有点误导，
一个 "Project" 就是一个单纯的 ".fbp" 文件, 没有特定的文件夹结构或多个文件。
产生文件的相对路径, 文件名和格式可以在 "Project" 中设置。
wxFormBuilder 可以仅以命令行方式启动将一个 ".fbp" 文件转换为源码, 而不启动图形界面编辑器,
这时可以通过命令行参数指定要生成的源码类型。
老版本只支持生成 C++ 和 XRC,
新版本还增加支持了 Python, Lua 等其他语言。
但很多设置都是针对 C++ 的, 对 C++ 提供了比较完整的支持。

XRC (http://docs.wxwidgets.org/2.8.12/wx_xrcoverview.html) 
是 wxWidgets 官方标准的 XML 格式图形界面资源文件,
可以直接加载 XRC 资源文件创建图形界面。
wxFormBuilder 使用 XRC 相对 C++ 会损失一些特性,
但是这种方式完全做到图形界面设计与代码分离, 
相对比较灵活, 并且是一种跨语言的方案。

一个 GUI 程序可以分为图形界面设计(View),
图形界面的事件响应和控制逻辑(Controller)
和后台业务逻辑 3 部分, 
即 MVC 模型。

其中 V 和 C 有一定程度的耦合,
但我们希望 V 完全由图形化设计工具自动生成,
而 C 的控制逻辑手写编码维护,
所以我们希望这两部分代码可以完全分离。
其中事件映射也是比较机械和繁琐的事, 
最好这一部分也由设计工具维护,
预留一些钩子或函数让 C 去实现。

使用 XRC 资源的简单 GUI 程序代码 "simple_xrc.py" 示例:

```python
#!/usr/bin/env python

import wx, wx.xrc

class App(wx.App):
	def OnInit(self):
		wx.xrc.XmlResource.Get().Load("git_save.xrc")
		self.frame = wx.xrc.XmlResource.Get().LoadFrame(None, "MainWindowUi")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

def main():
	app = App(False)
	app.MainLoop()

if __name__ == '__main__':
	main()
```

与 "simple.py" 示例相比,
仅仅是

```python
		self.frame = wx.Frame(None)
```

这一行变成了

```python
		wx.xrc.XmlResource.Get().Load("git_save.xrc")
		self.frame = wx.xrc.XmlResource.Get().LoadFrame(None, "MainWindowUi")
```

这样的两行。
但前者只能创建一个简单的空白窗口,
而后者的 XRC 文件由图形化设计工具产生,
可以设计出任意复杂的图形界面,
代码还是一样的, 不需要任何改动。

注意与 C++ 的区别:

0. "xrc" 相关的类被放在 "wx.xrc" 这个单独的包里, 并且需要单独导入。
0. C++ 版 LoadFrame() 方法需要一个预创建的 wxFrame 对象作为第一个参数,
Python 版直接由 xrc 创建返回一个 wxFrame 对象, 代码更简洁一些。


### 两阶段创建

有时候我们希望从 XRC 创建一个自定义的 wxFrame 子类对象, 而不是标准的 wxFrame 对象,
因为 python 不支持函数重载, 
所以 wxPython 增加了一个 LoadOnFrame() 方法实现类似的功能,
同时预创建的对象要用 wx.PreFrame 表示, 
具体细节请参考 "两阶段创建" 的说明(http://wiki.wxpython.org/TwoStageCreation)。

文中提到还可以使用 "subclass" 来实现类似功能。
试了一下 python 中查找 subclass 的规则还需要琢磨下,
不清楚这个东西在 C++ 中是否支持及如何支持,
属性设置是否可以通用。
这个不清楚的东西最好还是不要使用。

wxFormBuilder 生成源码时,
一个 Form 对应一个类, Form 名字作为类名,
而子窗口控件都是类的字段, 控件名字作为字段名。
因此我们设计界面时, 也应该按 Form 用类名, 控件用字段名的风格来设计。
subclass 作为基类名, C++ 代码可以设置 header 指定 subclass 的来源,
Python 代码就不知道 subclass 从何而来, 
再次说明 subclass 这个东西没有标准化, 不要使用。

生成 C++/Python 代码时虽然设置了事件映射的函数,
要分离自动生成的代码和试图控制逻辑代码,
我们还是应该在单独的文件中实现事件处理函数,
通用的方式就是继承自动生成的类,
重写事件处理函数。
自动生成的类是更纯粹的试图展现,
所以我们给自动生成的类添加 "Ui" 后缀, 
即设计 Form 名字时带 "Ui" 后缀。

生成 XRC 文件时不支持设置事件映射, 也没有自动生成的类。
视图控制类可以借助两阶段创建初始化, 或者直接将创建后的视图对象传递给视图控制对象。

```
```

C++ 不能传递对象, 可以使用两阶段创建。

生成源码时, 默认每个控件都成为 Form 对象的一个字段,
而加载 XRC 资源时, 不会自动将控件作为 Form 的字段, 只能根据需要设置字段。
C++ 不能动态扩展字段, 创建字段的过程更加机械和繁琐, 也许使用源码还更简单。

