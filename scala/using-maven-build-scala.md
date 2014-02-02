使用 maven 编译 scala 程序
===

初学一门语言, 多做练习很重要,
所以初学 scala 时, 了解如何开发, 运行 scala 程序也很重要.
之前尝试过学习 sbt, 晦涩难懂又非常难用, 果断抛弃.
试用了一下 scala ide, 使用 maven 开发, 感觉靠谱很多.
可参考 [官方教程](http://scala-ide.org/docs/tutorials/m2eclipse/index.html#create-a-new-scala-maven-project).

首先下载 scala ide 完整版, 解压, 根据需要修改 `eclipse.ini` 文件和其他配置.
我使用的是 3.0.2 版本.

```sh
tar xf scala-SDK-3.0.2-vfinal-2.10-linux.gtk.x86.tar.gz
mv eclipse eclipse-scala
```

打开 scala ide, 根据教程新建一个 maven 工程.
eclipse 默认没有 scala-archetype-simple, 
但在 http://search.maven.org 上可以找到这个 archetype,
可以直接添加到 eclipse, 相关信息如下:

```xml
<dependency>
    <groupId>net.alchim31.maven</groupId>
    <artifactId>scala-archetype-simple</artifactId>
    <version>1.5</version>
</dependency>
```

生成 scala maven 项目中的关键信息如下.

项目属性添加:

```xml
	<properties>
		<scala.tools.version>2.10</scala.tools.version>
		<scala.version>2.10.0</scala.version>
	</properties>
```

项目依赖添加:

```xml
		<dependency>
			<groupId>org.scala-lang</groupId>
			<artifactId>scala-library</artifactId>
			<version>${scala.version}</version>
		</dependency>

		<!-- Test -->
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.11</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.specs2</groupId>
			<artifactId>specs2_${scala.tools.version}</artifactId>
			<version>1.13</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.scalatest</groupId>
			<artifactId>scalatest_${scala.tools.version}</artifactId>
			<version>2.0.M6-SNAP8</version>
			<scope>test</scope>
		</dependency>
```

项目 build 添加:

```xml
		<sourceDirectory>src/main/scala</sourceDirectory>
		<testSourceDirectory>src/test/scala</testSourceDirectory>
```

build 插件添加:

```xml
			<plugin>
				<!-- see http://davidb.github.com/scala-maven-plugin -->
				<groupId>net.alchim31.maven</groupId>
				<artifactId>scala-maven-plugin</artifactId>
				<version>3.1.3</version>
				<executions>
					<execution>
						<goals>
							<goal>compile</goal>
							<goal>testCompile</goal>
						</goals>
						<configuration>
							<args>
								<arg>-make:transitive</arg>
								<arg>-dependencyfile</arg>
								<arg>${project.build.directory}/.scala_dependencies</arg>
							</args>
						</configuration>
					</execution>
				</executions>
			</plugin>
```

因为 scala 不同版本可能不兼容, 
项目 scala-library 依赖和 scala 编译插件应该保证使用相同版本的 scala.

scala ide 会自动完成 scala 代码编译, 并支持直接运行.

maven 下也可以直接编译, 编译之后的类可直接使用 scala 解释器运行.

```sh
mvn clean
mvn compile
scala -cp target/classes test.App
```

为了保证编译时的 scala 版本和运行时的 scala 版本一致,
最好使用项目依赖的 scala-library 运行程序.

scala 编译后的 class 文件就是普通的 java class 文件,
可直接通过 jvm 运行,
只要找到对应的 scala 依赖即可.
可以用 maven dependency 插件找到项目所有依赖, 
最简单的情况下， 只需要 scala-library 即可.

```sh
mvn dependency:build-classpath
java -cp /home/observer.hany/.m2/repository/org/scala-lang/scala-library/2.10.0/scala-library-2.10.0.jar:target/classes/ test.App
```

