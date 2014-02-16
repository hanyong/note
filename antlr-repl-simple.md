使用 antlr 轻松实现解释器
===

antlr 资源参考:
* antlr 官方主页: http://www.antlr.org/
* eclipse 插件: https://github.com/jknack/antlr4ide
* maven 依赖:

```xml
		<dependency>
			<groupId>org.antlr</groupId>
			<artifactId>antlr4</artifactId>
			<version>4.2</version>
		</dependency>
```

* 源码仓库: https://github.com/antlr/antlr4
* 语法文件收集仓库: https://github.com/antlr/grammars-v4
* 语法文件生成解析器工具类: `org.antlr.v4.Tool`
* 运行解析器测试类: `org.antlr.v4.runtime.misc.TestRig`
* 本教程源码: https://github.com/hanyong/lisping/tree/master/antlr-repl-simple

我现在使用的是最新 4.2 版本,
http://search.maven.org/ 上发现还有个对应的 maven 插件 "antlr4-maven-plugin".
奇怪的是 antlr4 maven 插件官方和 google 都没找到相关文档 
(只好拉源码自己 mvn site 生成文档?),
官方主推的 ANTLRWorks 好像是个 netbeans 插件, 汗...
对我来说使用 eclipse 插件就足够, 暂时不管别的.

antlr 的使用方式很简单, 写一个语法定义文件 "Somelang.g4",
然后调用 `org.antlr.v4.Tool`
就可根据语法定义文件生成一个词法分析器和一个语法解析器.
或者直接调用 eclipse 插件.
选中语法定义文件, 直接点运行按钮即可生成分析器.
默认每次修改保存文件时都会自动重新生存,
默认生成目录为 "./target/generated-sources/antlr4".
我根据习惯修改了下插件配置, 禁用自动生成,
生成目录修改为 "src/main/java",
取消勾选 "Mark generated files as derived" 选项.

## 词法分析与语法解析

编译原理上有两个概念, "词法分析" 和 "语法解析", 
词法分析检查单词拼写, 产生一个个单词, 即 token.
语法解析则检查单词和标点符号 (也是 token) 组成句子的语法是否正确,
句子的含义是什么.
如果语法正确, antlr 还可以自动生成语法树.

antlr 同时支持词法分析和语法解析.
显然, 词法分析的输出作为语法解析的输入,
你也可以让 antlr 只做其中一样, 自己实现另外一样.
当然最好两件事都让 antlr 来做, 
因为 antlr 两件事都做的很棒!

## 前缀加法器

我们定义一个前缀表达式加法语言,
相当于一个精简版的 clojure 表达式.
合法语法示例 "test.clj" 如下:

```clj
(+
	(+ 1 1)
	(+ 5 5)
	)
```

姑且把它叫做 plus 语言, 然后为它实现一个解释器.
上述表达式应该得到计算结果 `(1 + 1) + (5 + 5) = 12`.

## 语法定义

antlr 的使用方式很简单, 首先写一个语法定义文件 "Plus.g4".
然后调用 `org.antlr.v4.Tool`, 或 eclipse 插件,
根据语法定义文件生成一个词法分析器和一个语法解析器.

plus 简单语法定义如下:

```antlr
grammar Plus;

expr: INT
	| list
	;

list: '(' '+' expr expr ')'
	;

INT: [0-9]
	;
```

第一行 `grammar Plus;` 说明语法名称, 
与 java 类似, 语法名必须与文件名同名.
这个名字将作为自动生成的 java 类名的前缀, 所以使用大写字母开头.

antlr 约定词法规则名字以大写字母开头, 如 `INT`,
语法规则名字以小写字母开头, 如 `expr`, `list`.
两者定义都以分号 ";" 结束.
antlr 说它的语法是基于 C 的, 易于学习,
感觉也有很多像正则表达式的地方.
两者的书写语法稍有不同.
词法规则貌似简单的字符串匹配.
语法规则中字面量放在单引号内,
可以直接通过名字引用其他词法和语法规则.

`list` 语句由 5 个 token 组成,
每个字面量 (标点符号) 也是一个 token,
词法分析器包含了 4 种 token.
所以在 antlr 中实际上是词法和语法混在一起,
更加方便描述和使用.

不知道语法文件怎么写?
[grammars-v4][] 收集了许多流行语言的语法写法示例, 
你可以直接参考或者照抄.

## 运行解析器

使用 `org.antlr.v4.runtime.misc.TestRig` 可以直接运行生成的分析器.
antlr eclipse 插件没有直接支持这个, 
不过使用 "Java Application" 运行配置也可以很方便的运行类.
新建运行配置 "grun-plus", 设置参数为 "plus.g4.Plus expr",
第一个参数是语法名，即分析器类名前缀, 所以加了 `plus.g4.` 包名,
第二个参数是要解析的语法规则名.
从使用帮助上看到, 如果是纯词法规则, 第二个参数可以用 "tokens".
还可以跟一个文件名参数, 表示从文件读入输入, 否则从标准输入读入.

运行 "grun-plus", 输入 `(+ 1 2)`, 可看到如下输出报错:

```sh
(+ 1 2)
line 1:2 token recognition error at: ' '
line 1:4 token recognition error at: ' '
line 1:7 token recognition error at: '\n'
```

词法分析器尝试将所有输入都解析为 token,
所有输入字符都要有合法的词法分析规则.
可以照抄一段示例语法 `WS: [ \t\r\n]+ -> skip ;` 忽略空白字符.

修正后的语法定义如下:

```antlr
grammar Plus;

expr: INT
	| list
	;

list: '(' '+' expr expr ')'
	;

INT: [0-9]
	;

WS: [ \t\r\n]+ -> skip
	;
```

再次运行 "grun-plus", 输入 `(+ 1 2)`, 没有任何输出,
说明输入是合法的, antlr 已经识别出输入语法, 然后什么也没做...

修改 "grun-plus" 参数为 "plus.g4.Plus expr -tree src/test.clj",
即增加 "-tree src/test.clj" 参数,
让解析器以 test.clj 作为输入, 并打印出解析后的语法树.
输出结果为:

```clj
(expr (list ( + (expr (list ( + (expr 1) (expr 1) ))) (expr (list ( + (expr 5) (expr 5) ))) )))
```

因为 clojure 语法输入本来就是语法树, 这没什么稀奇的, 
对其他语言可是大功一件.
还可以使用 "-gui" 参数以图形化方式展示解析后的语法树.
修改 "grun-plus" 参数为 "plus.g4.Plus expr -gui src/test.clj",
再次运行, 可看到如下结果, 这下觉得牛逼了吧.

[[antlr-repl-simple/antlr-plus-gui.png]]

## 编程方式使用解析器



[grammars-v4]: https://github.com/antlr/grammars-v4

