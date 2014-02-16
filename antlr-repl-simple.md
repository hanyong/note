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

查看产生的解析器 `PlusParser` 源码, 
每条语法规则对应一个同名的解析对应语法的函数.
编程方式使用解析器代码示例 "Plus.java" 如下:

```java
package plus;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;

import plus.g4.PlusLexer;
import plus.g4.PlusParser;

public class Plus {

	public static void main(String[] args) throws Exception {
		PlusLexer lexer = new PlusLexer(new ANTLRInputStream(System.in));
		PlusParser parser = new PlusParser(new CommonTokenStream(lexer));
		parser.expr();
	}

}
```

运行程序, 将在标准输入接受输入, 如果有语法错误将会提示,
否则跟之前的情形一样, 什么也不做...

## 将语句映射到行为

antlr 只能帮你到这里了.
antlr 已经帮你解析出语法, 得到一条条语句, 
但是每条语句是什么意思, 要执行什么动作, 就要由我们来定义了.
antlr 提供了两种方式实现将语句映射到行为上, 
一种是 Actions, 类似解析 XML 时的 SAX, 
一种抽象语法树 ast, 类似解析 XML 时的 DOM.
对解释器而言, 我们当然希望边输入边执行, 当然第一种方式更适合.

antlr 对 actions 的支持简单而直接, 
直接在语法定义文件中插入 java 代码.
在定义语句的地方用 java 写出该语句要执行什么操作, 即定义语义.
文档参考: https://theantlrguy.atlassian.net/wiki/display/ANTLR4/Actions+and+Attributes

如 list 语法定义:

```antlr
list: '(' '+' expr expr ')'
	;
```

可以直接在 list 语句下定义该语句要执行的操作:

```antlr
list: '(' '+' expr expr ')'
	{
		System.out.println("find list");
	}
	;
```

expr 是 INT 语句或 list 语句:

```antlr
expr: INT
	| list
	;
```

可以在每条语句下写出该语句要执行的操作:

```antlr
expr: INT
	{
		System.out.println("find expr int");
	}
	| list
	{
		System.out.println("find expr list");
	}
	;
```

编写 Actions 时, 还可以直接根据 token 名字访问 token 对象.
语句不能直接通过名字访问, 必须定义别名.
并且只能访问语句的属性, 不能访问语句对象本身.
token 也可以定义别名访问, 
这样同一语句中重复出现的 token 可以通过不同的别名区分.
"Plus.g4" 添加简单行为定义后完整代码如下:

```antlr
grammar Plus;

expr: INT
	{
		System.out.println("found expr int: " + $INT.text);
	}
	| x = list
	{
		System.out.println("found expr list: " + $x.text);
	}
	;

list: '(' '+' a = expr b = expr ')'
	{
		System.out.printf("found list: %s + %s\n", $a.text, $b.text);
	}
	;

INT: [0-9]
	;

WS: [ \t\r\n]+ -> skip
	;
```

重新生成解析器后再运行 Plus 解释器, 输入 `(+ 1 2)`, 可看到如下输出:

```sh
(+ 1 2)
found expr int: 1
found expr int: 2
found list: 1 + 2
found expr list: (+12)
```

## 解释器

就像直接在 JSP 页面中写 java 代码一样, 
直接在语法文件中写 java 代码看起来不是一个好办法.
模仿 MVC 的思路, 
应该考虑在独立的 java 代码中完成解释器的主要工作.
如上定义的加法器, 可以通过一个简单的堆栈机 "PlusVm" 实现,
提供 `read`, `plus` 两条指令在语法文件中调用即可.

```java
package plus;

import java.util.ArrayDeque;

public class PlusVm {

	private ArrayDeque<Integer> stack = new ArrayDeque<>();

	public void read(String s) {
		int n = Integer.parseInt(s);
		stack.addLast(n);
		System.out.println("read int: " + n);
	}

	public void plus() {
		int b = stack.removeLast();
		int a = stack.removeLast();
		int c = a + b;
		stack.addLast(c);
		System.out.printf("plus: %d + %d = %d\n", a, b, c);
	}

}
```

语法文件可以通过 `@header` action 添加 import 语句,
通过 `@members` action 为 parser 添加 vm 成员,
然后在语句 action 中添加对 vm 的简单调用即可.

```antlr
grammar Plus;

@parser::header {
	import plus.PlusVm;
}

@parser::members {
	PlusVm vm = new PlusVm();
}

expr: INT
	{
		vm.read($INT.text);
	}
	| x = list
	;

list: '(' '+' expr expr ')'
	{
		vm.plus();
	}
	;

INT: [0-9]
	;

WS: [ \t\r\n]+ -> skip
	;
```

重新编译运行, 执行结果如下:

```sh
(+ 1 2)
read int: 1
read int: 2
plus: 1 + 2 = 3
```

之前定义的语法测试输入执行结果:

```sh
(+
	(+ 1 1)
	(+ 5 5)
	)
read int: 1
read int: 1
plus: 1 + 1 = 2
read int: 5
read int: 5
plus: 5 + 5 = 10
plus: 2 + 10 = 12
```

测试结果正确, 至此, 我们实现了 plus 解释器的功能.

[grammars-v4]: https://github.com/antlr/grammars-v4

