eclipse 插件源码学习
===

## 运行配置类型

jdt 提供了一个运行 java 应用程序的基类抽象类
`org.eclipse.jdt.launching.AbstractJavaLaunchConfigurationDelegate`,
需要提供运行 java 程序功能的插件都可以从这个类继承.
这个类和运行 "Java Application" 的扩展 `JavaLaunchDelegate` 在包
"org.eclipse.jdt.launching_3.7.0.v20130515-1451.jar".
扩展配置如下:

```xml
   <extension
         point="org.eclipse.debug.core.launchConfigurationTypes">
      <launchConfigurationType
            delegate="org.eclipse.jdt.launching.JavaLaunchDelegate"
            delegateDescription="%localJavaApplicationDelegate.description"
            delegateName="%eclipseJDTLauncher.name"
            id="org.eclipse.jdt.launching.localJavaApplication"
            migrationDelegate="org.eclipse.jdt.internal.launching.JavaMigrationDelegate"
            modes="run, debug"
            name="%localJavaApplication"
            sourceLocatorId="org.eclipse.jdt.launching.sourceLocator.JavaSourceLookupDirector"
            sourcePathComputerId="org.eclipse.jdt.launching.sourceLookup.javaSourcePathComputer">
      </launchConfigurationType>
      ...
   </extension>
```

而提供配置界面的扩展 `LocalJavaApplicationTabGroup` 在另一个包
"org.eclipse.jdt.debug.ui_3.6.200.v20130514-0841.jar".
扩展配置如下:

```xml
   <extension
         point="org.eclipse.debug.ui.launchConfigurationTabGroups">
      <launchConfigurationTabGroup
            type="org.eclipse.jdt.launching.localJavaApplication"
            helpContextId="org.eclipse.jdt.debug.ui.local_java_application_type_context"
            class="org.eclipse.jdt.internal.debug.ui.launcher.LocalJavaApplicationTabGroup"
            id="org.eclipse.jdt.debug.ui.launchConfigurationTabGroup.localJavaApplication">
            <launchMode 
                  mode="debug"
                  perspective="org.eclipse.debug.ui.DebugPerspective"
                  description="%localJavaApplicationTabGroupDescription.debug">
            </launchMode>
            <launchMode
                  mode="run"
                  description="%localJavaApplicationTabGroupDescription.run">
            </launchMode>
      </launchConfigurationTabGroup>
```

可以通过 "launchConfigurationTabGroup" 下的 "launchMode" 
配置运行时需要选择的视图.
没有配置 "launchMode" 子节点时, 这个配置界面可以用于所有支持的 "modes",
而如果配置了 "launchMode" 子节点, 则只有子节点指定的 "mode" 才可以用,
所以不需要其他配置的 "mode" 也要加一个空 "launchMode" 子节点.

## 运行前自动编译代码

jdt 运行 java 程序前会先自动编译代码, 是如何实现的呢?
运行程序时跟踪到包
"org.eclipse.debug.ui_3.9.0.v20130516-1713.jar" 
下的类
`org.eclipse.debug.internal.ui.DebugUIPlugin`,
方法片段:

```java
	public static ILaunch buildAndLaunch(ILaunchConfiguration configuration, String mode, IProgressMonitor monitor) throws CoreException {
		boolean buildBeforeLaunch = getDefault().getPreferenceStore().getBoolean(IDebugUIConstants.PREF_BUILD_BEFORE_LAUNCH);
		
		monitor.beginTask(IInternalDebugCoreConstants.EMPTY_STRING, 1);
		try
		{
			return configuration.launch(
					mode,
					new SubProgressMonitor(monitor, 1),
					buildBeforeLaunch);
		}
		finally
		{
			monitor.done();
		}
	}
```

"buildBeforeLaunch" 取自选项
`IDebugUIConstants.PREF_BUILD_BEFORE_LAUNCH` 
("org.eclipse.debug.ui.build_before_launch").
取选项的代码在包
"org.eclipse.ui.workbench_3.105.1.v20130821-1411.jar"
类
`org.eclipse.ui.preferences.ScopedPreferenceStore`.
这个选项可以通过运行配置设置.

一次运行操作将请求调用到包
"org.eclipse.debug.core_3.8.0.v20130514-0954.jar", 
下的类
`org.eclipse.debug.internal.core.LaunchConfiguration`.

```java
    public ILaunch launch(String mode, IProgressMonitor monitor, boolean build, boolean register) throws CoreException {
    	if (monitor == null) {
			monitor = new NullProgressMonitor();
    	}
    	/* Setup progress monitor
    	 * - Prepare delegate (0)
    	 * - Pre-launch check (1)
    	 * - [Build before launch (7)]					if build
    	 * - [Incremental build before launch (3)]		if build
    	 * - Final launch validation (1)
    	 * - Initialize source locator (1)
    	 * - Launch delegate (10) */
```

然后调用到包
"org.eclipse.debug.core_3.8.0.v20130514-0954.jar"
的接口
`org.eclipse.debug.core.model.ILaunchConfigurationDelegate2`
的方法
`public boolean buildForLaunch(ILaunchConfiguration configuration, String mode, IProgressMonitor monitor) throws CoreException;`.

`org.eclipse.debug.core.model.LaunchConfigurationDelegate`
实现了 "buildForLaunch()" 方法,
调用了方法
`protected void buildProjects(final IProject[] projects, IProgressMonitor monitor) throws CoreException`,
最终调用到包
"org.eclipse.core.resources_3.8.101.v20130717-0806.jar"
接口
"org.eclipse.core.resources.IProject"
的方法
`public void build(int kind, IProgressMonitor monitor) throws CoreException`.
类
`org.eclipse.core.internal.resources.Project`
实现了这个方法.

## "Run As" 上下文菜单

在 jetty 插件被 "Run As" 菜单触发的扩展
"org.eclipse.core.expressions.propertyTesters" 
上打断点, 跟踪到如下堆栈片段:

```sh
	at org.eclipse.core.internal.expressions.EnablementExpression.evaluate(EnablementExpression.java:53)
	at org.eclipse.debug.internal.ui.launchConfigurations.LaunchShortcutExtension.evalEnablementExpression(LaunchShortcutExtension.java:287)
	at org.eclipse.debug.ui.actions.ContextualLaunchAction.isApplicable(ContextualLaunchAction.java:295)
	at org.eclipse.debug.ui.actions.ContextualLaunchAction.fillMenu(ContextualLaunchAction.java:218)
	at org.eclipse.debug.ui.actions.ContextualLaunchAction$1.menuShown(ContextualLaunchAction.java:137)
```

问题: 这里加断点后导致整个操作系统图像界面卡住,
无法进行调试, 使用 jstack 导出得到上述堆栈.

根据堆栈找到加载 launchShortcuts 的代码在包
"org.eclipse.debug.ui_3.9.0.v20130516-1713.jar"
类 `org.eclipse.debug.ui.actions.ContextualLaunchAction`
方法 `protected void fillMenu(Menu menu)`.
大概过程是先找到所有 launchShortcuts 再过滤,
代码片段:

```java
		List allShortCuts = getLaunchConfigurationManager().getLaunchShortcuts();
		Iterator iter = allShortCuts.iterator();
		List filteredShortCuts = new ArrayList(10);
... ...
		while (iter.hasNext()) {
			LaunchShortcutExtension ext = (LaunchShortcutExtension) iter.next();
			try {
				if (!WorkbenchActivityHelper.filterItem(ext) && isApplicable(ext, context)) {
					filteredShortCuts.add(ext);
				}
			} 
			catch (CoreException e) {
				IStatus status = new Status(IStatus.ERROR, DebugUIPlugin.getUniqueIdentifier(), "Launch shortcut '" + ext.getId() + "' enablement expression caused exception. Shortcut was removed.", e); //$NON-NLS-1$ //$NON-NLS-2$
				DebugUIPlugin.log(status);
				iter.remove();
			}
		}
```

注意, 过滤 launchShortcuts 时, 测试扩展所在的插件不会被自动加载,
测试扩展和 launchShortcuts 由同一个插件提供时可能是个坑,
需要指定 `forcePluginActivation="true"`,
如 jetty 插件配置如下:

```xml
<enablement>
	<with variable="selection">
	 	<count value="1"/>
    	<iterate>
    	 	<and>
    	 	 	<adapt type="org.eclipse.core.resources.IResource">
    	 	 	<!-- After tracing code and find document,
	 	 			By default it's lazy loaded (will return true at that case) ,
    	 	 		have to force it or it won't work...what the hell... -->
					<test property="runjettyrun.webapp"  forcePluginActivation="true" />
				</adapt>
			</and>
		</iterate>
     </with>
</enablement>
```

开发时犯了一个错误, 后来看到文档才明白.
树, 表格视图下的选择结果是结构化选择, 是一个 collection,
必须用 `count` 和 `iterate` 测试,
直接用 `adapt` 测试是不行的, 导致菜单项没有显示.

## 三方库

[eclipse orbit](http://eclipse.org/orbit/) 
项目提供了一些可以在 eclipse 中使用的 3 方库的 bundle,
如 logback.classic 二进制包和源码.
从 orbit 下载页面, 
如 [R20130827064939](http://download.eclipse.org/tools/orbit/downloads/drops/R20130827064939/),
可以找到 update site 链接
http://download.eclipse.org/tools/orbit/downloads/drops/R20130827064939/repository/
,
或者直接从页面链接下载.

