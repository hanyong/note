使用 maven enforcer 插件检查依赖冲突
===

我们在项目开发时常常会遇到依赖冲突，
在开发时就解决掉依赖冲突，
能有效避免运行时再暴露问题带来的损失和高昂排查成本。
maven enforcer 插件并不能解决依赖冲突，但可以检查依赖冲突，而检查是解决的第一步。

对项目开发者而言，对可能冲突的依赖，我们必须清楚项目最终将包含、不包含哪些依赖，甚至确定依赖什么版本，即对最终依赖的期望。
我们将这种期望告诉 enforcer，enforcer 帮我们检查项目最终依赖是否满足期望。

实际上 maven enforcer 插件包含许多规则, 检查最终依赖的规则叫做 "bannedDependencies" 。
比如我们项目使用 slf4j 打印日志，项目依赖的一些库依赖了 log4j, 一些库依赖了 logback, 
我们最终想要使用 log4j, 需要在所有依赖中排除 logback, 可书写如下规则:

```xml
<bannedDependencies>
	<excludes>
		<exclude>org.slf4j:*</exclude>
		<exclude>ch.qos.logback:*</exclude>
	</excludes>
	<includes>
		<include>org.slf4j:slf4j-api</include>
		<include>org.slf4j:slf4j-log4j12</include>
	</includes>
</bannedDependencies>
```

slf4j 有许多种实现绑定，这些绑定是互相冲突的，除了 log4j 实现绑定 (即 `slf4j-log4j12`) 外其他实现我们希望通通排除。
挨个列举所有 slf4j 实现绑定很麻烦，可能还会有错漏，所以我们干脆直接排除了 "org.slf4j" 整个组，
再通过 includes 配置添加上我们需要依赖的 `slf4j-api` 接口和 `slf4j-log4j12` 实现。
logback 也是 slf4j 的一个实现，我们通过 logback 的 groupId "ch.qos.logback" 排除了其所有依赖，不需要包含其任何依赖。

从以上配置示例可知，bannedDependencies 规则是先应用 excludes 规则得到一个大的结果，再应用 includes 规则对结果进行微调。
groupId, artifactId, version 之间用冒号 ":" 分割，version 可以省略，artifactId 可以使用星号 "*" 表示所有，即不限定。

再举个例子，我们希望限定项目最终使用的 spring 框架必须为某个版本，可以使用如下规则:

```xml
<bannedDependencies>
	<excludes>
		<exclude>org.springframework:*</exclude>
	</excludes>
	<includes>
		<include>org.springframework:*:${spring-version}</include>
	</includes>
</bannedDependencies>
```

首先我们通过 spring 框架的 groupId 排除了所有 spring 依赖, 然后我们再通过 includes 指定某个版本的 spring 允许被包含。
其中 `${spring-version}` 是我们在 pom 中配置的一个属性。

针对如上两条规则，可得到完整插件配置如下:

```xml
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-enforcer-plugin</artifactId>
	<version>1.3.1</version>
	<executions>
		<execution>
			<id>default-enforce</id>
			<goals>
				<goal>enforce</goal>
			</goals>
			<configuration>
				<rules>
					<bannedDependencies>
						<excludes>
							<exclude>org.slf4j:*</exclude>
							<exclude>ch.qos.logback:*</exclude>
							<exclude>org.springframework:*</exclude>
						</excludes>
						<includes>
							<include>org.slf4j:slf4j-api</include>
							<include>org.slf4j:slf4j-log4j12</include>
							<include>org.springframework:*:${spring-version}</include>
						</includes>
					</bannedDependencies>
				</rules>					
			</configuration>
		</execution>
	</executions>
</plugin>
```

如果依赖规则不满足，我们执行 `mvn package` (准确的说是 `mvn validate`) 时就会报错。

如果有报错，我们需要手动解决依赖冲突，具体情况需要具体分析。简单来说有两种情况。

1. 缺少依赖。只需要在 pom 文件中增加依赖配置即可。

2. 包含了不应该包含的依赖。根据报错结果，通过 eclipse m2e 插件的 maven 依赖视图可以轻易找到是哪一条依赖路径引入依赖，
在该依赖配置下添加 exclude 配置排除不期望的依赖。如果一个依赖被很多库都依赖了，需要逐个添加配置排除，
这可能会很繁琐，勤快点，不要怕麻烦，一个一个来。

如我们依赖了 diamond，但要排除 logback，依赖配置如下：

```xml
<dependency>
	<groupId>com.taobao.diamond</groupId>
	<artifactId>diamond-client</artifactId>
	<exclusions>
		<exclusion>
			<groupId>ch.qos.logback</groupId>
			<artifactId>*</artifactId>
		</exclusion>
	</exclusions>
	<version>3.6.9.2</version>
</dependency>
```

顺带提一下: 为了排除某个依赖，还有个办法是引入一个版本号为 `99.0-does-not-exist` 的空 jar 包。
这是某网友在 07 年想出来的一个土办法，具体可参考: [version-99-does-not-exist](http://day-to-day-stuff.blogspot.com/2007/10/announcement-version-99-does-not-exist.html).
这个办法有两个问题，
(1) 是每个你想排除的依赖，你得给它虚构一个 "99.0-does-not-exist" 版本的 jar 包，
(2) 是 maven 中央仓库不会帮你维护这个虚构版本的 jar 包([look](http://search.maven.org/#search|ga|1|v%3A%2299.0-does-not-exist%22))，
你得想办法把它配置在一个私服上，然后你的 maven 环境得依赖这个私服。
总之来说就是 **非标准化**，事隔多年之后，原作者也发贴 **建议使用** 稍微麻烦许多的 **enforcer 检查替代 99.0-does-not-exist** (人间正道是沧桑)。
具体可参考 [stackoverflow 讨论](http://stackoverflow.com/questions/547805/exclude-all-transitive-dependencies-of-a-single-dependency/10391251#10391251)。

更多信息可参考最新官方文档: [maven-enforcer-plugin](http://maven.apache.org/enforcer/maven-enforcer-plugin/).
