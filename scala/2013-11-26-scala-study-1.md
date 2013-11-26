scala学习笔记-1
===

浏览了一些 scala 学习资料,
决定先看创始人亲自写的《Programming in Scala》.

java 的一个缺点被认为是不够简洁.
很多新语言都支持列表, 字典等常用数据结构的字面值表示, 
如 python.

```python
L = [ 1, 3, "abc", ]
d = { "x": 5, "y": 3, 99: "good", }
```

java 中构造一个字典则要麻烦得多.

```java
HashMap<String, Integer> map = new HashMap<String, Integer>();
map.put("x", 3);
map.put("y", 5);
map.put("z", 12);
```

大量的重复拼写容易产生疲劳和错误,
而且数据被大量语法字符包围,
不方便单独抽取和维护数据.

另一方面, java 中的数据结构是执行指令逐步建立起来的,
而 python 中的数据结构就像是 (编译时) 预先创建好的,
似乎还有性能和使用简洁 (不需要考虑何时初始化) 的优势.

另一种方案是数据采用独有的资源和格式来维护,
但对太少量嵌入式数据未免过于复杂.
数据和代码使用同一套语法格式来维护将会简单一致很多,
这正是 clojure 等 LISP 语言的一大优势.

简单来说, **java 缺少良好的表示数据的方式** ,
而需要表示数据的需求并不罕见.

我曾设想 java 可以把 python 表示数据的语法引进来.
python 的字典只有一个类型, 
Java 的 Map 却有许多类型, 
Java 可以给字面量增加一个表示类型的前缀.

```java
map = HashMap<String, Integer> {
	"x": 3,
	"y": 5,
	"z": 12,
};
```

然而 python 的 dict 类型是语言定义的一部分,
是解释器可以感知并特殊对待的,
而 java 的 Map 是语言定义之外的库,
编译器没有感知.
java 是否可能引入这种定义和感知?
Exception 虽然也是通过库定义,
编译器却能感知和检查,
一开始对这个特性也很感到惊异和奇特.

java 中唯一支持的较复杂数据结构字面量就是数组.
模拟 clojure 的语法,
倒是可以通过数组构造 map.

```java
Object[] a = { 
	"x", 3, 
	"y", 5, 
	"z", 12, 
};
HashMap<String, Integer> map = new HashMap<String, Integer>();
for (int i = 0; i < a.length; i += 2) {
	String k = (String) a[i];
	Integer v = (Integer) a[i + 1];
	map.put(k, v);
}
```

但这种方式缺少编译时数组长度 (必须为偶数) 和类型安全检查,
远没有语言原生支持数据类型字面量方便和安全可靠.

书一开始 "1.1" 提到 scala 可以使用很简洁的语法表示数据, 
突然想起上面的话题.

```scala
var capital = Map("US" -> "Washington", "France" -> "Paris")
capital += ("Japan" -> "Tokyo")
println(capital("France"))
```

