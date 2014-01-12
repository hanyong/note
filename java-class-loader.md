java 类加载器
===

java 应用程序的入口是一个类的静态 main 方法.
启动一个 java 程序的命令如下所示:

```sh
java -classpath a.jar:b.jar com.example.App
```

jvm 启动时, 自动用 classpath 上的所有路径列表, 创建一个类加载器, 叫做系统类加载器.
然后用系统类加载器加载入口类, 并执行入口类的 main 方法.
classpath 由 `CLASSPATH` 环境变量 和 `-classpath` 命令行参数合并产生.
运行时可以用 ```ClassLoader.getSystemClassLoader()``` 取到系统类加载器的实例.

jvm 默认存在 3 个类加载器, 父委托关系如下:

```sh
"system class loader" -> "ext class loader" -> "bootstrap class loader"
```

java 应用程序无法取到启动类加载器 (bootstrap) 的引用,
```ClassLoader.getSystemClassLoader().getParent().getParent() == null```.
运行程序:

```java
package target;

public class Test {

	public static void main(String[] args) throws Exception {
		ClassLoader sys = ClassLoader.getSystemClassLoader();
		ClassLoader ext = sys.getParent();
		ClassLoader boot = ext.getParent();
		System.out.printf("sys: %s\next: %s\nboot: %s\n", sys, ext, boot);
	}

}
```

可看到输出如下:

```sh
sys: sun.misc.Launcher$AppClassLoader@13e8d89
ext: sun.misc.Launcher$ExtClassLoader@1be2d65
boot: null
```

