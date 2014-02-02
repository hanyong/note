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

## 上下文运行

直接点击工具栏上的运行按钮, 会优先根据上下文运行.

0. 找到 `org.eclipse.debug.ui.DebugUITools` 类所在的 jar 包.
0. 找到插件 `plugin.xml` 配置文件.
0. 找到 `org.eclipse.debug.internal.ui.actions.RunLastAction`.
0. 找到类 `org.eclipse.debug.ui.actions.RelaunchLastAction`.

上下文运行 action 代码如下:

```java
	public void run(IAction action){		
		if(LaunchingResourceManager.isContextLaunchEnabled()) {
			ILaunchGroup group = DebugUIPlugin.getDefault().getLaunchConfigurationManager().getLaunchGroup(getLaunchGroupId());
			ContextRunner.getDefault().launch(group);
			return;
		}
```

## 运行程序

`org.eclipse.debug.core.DebugPlugin` 提供了运行进程和包装进程的静态方法.

```java
	public static Process exec(String[] cmdLine, File workingDirectory, String[] envp) throws CoreException;
	public static IProcess newProcess(ILaunch launch, Process process, String label, Map attributes);
```

在 `DebugPlugin.newProcess()` 方法上打断点, 
可以跟踪到运行外部程序的功能在插件
"org.eclipse.core.externaltools_1.0.200.v20130402-1741.jar"
下的类
`org.eclipse.core.externaltools.internal.launchConfigurations.ProgramLaunchDelegate`
.
一些常量, 包括运行配置属性的 key, 定义在类
`org.eclipse.core.externaltools.internal.IExternalToolConstants`.
主要配置有:

```java
	public static final String UI_PLUGIN_ID = "org.eclipse.ui.externaltools"; //$NON-NLS-1$;
	public static final String ID_PROGRAM_LAUNCH_CONFIGURATION_TYPE = "org.eclipse.ui.externaltools.ProgramLaunchConfigurationType"; //$NON-NLS-1$

	/**
	 * Identifier for external tools launch configuration category. Launch
	 * configuration types for external tools that appear in the external tools
	 * launch configuration dialog should belong to this category.
	 */
	public static final String ID_EXTERNAL_TOOLS_LAUNCH_CATEGORY = "org.eclipse.ui.externaltools"; //$NON-NLS-1$

	/**
	 * String attribute identifying the location of an external. Default value
	 * is <code>null</code>. Encoding is tool specific.
	 */
	public static final String ATTR_LOCATION = UI_PLUGIN_ID + ".ATTR_LOCATION"; //$NON-NLS-1$

	/**
	 * String attribute containing the arguments that should be passed to the
	 * tool. Default value is <code>null</code>, and encoding is tool specific.
	 */
	public static final String ATTR_TOOL_ARGUMENTS = UI_PLUGIN_ID + ".ATTR_TOOL_ARGUMENTS"; //$NON-NLS-1$

	/**
	 * String attribute identifying the working directory of an external tool.
	 * Default value is <code>null</code>, which indicates a default working
	 * directory, which is tool specific.
	 */
	public static final String ATTR_WORKING_DIRECTORY = UI_PLUGIN_ID + ".ATTR_WORKING_DIRECTORY"; //$NON-NLS-1$
```

## eclipse 提供的基础服务

* Platform, OS 类型等基础环境信息

```java
	// org.eclipse.debug.core.DebugPlugin
	public static String[] parseArguments(String args) {
		if (args == null)
			return new String[0];
		
		if (Constants.OS_WIN32.equals(Platform.getOS()))
			return parseArgumentsWindows(args);
		
		return parseArgumentsImpl(args);
	}
```

* CoreException 异常

```java
	/**
	 * Throws a core exception with an error status object built from
	 * the given message, lower level exception, and error code.
	 * @param message the status message
	 * @param exception lower level exception associated with the
	 *  error, or <code>null</code> if none
	 * @param code error code
	 */
	protected static void abort(String message, Throwable exception, int code) throws CoreException {
		throw new CoreException(new Status(IStatus.ERROR, IExternalToolConstants.PLUGIN_ID, code, message, exception));
	}
```

* IStringVariableManager, 配置属性变量替换

```java
	private static IStringVariableManager getStringVariableManager() {
		return VariablesPlugin.getDefault().getStringVariableManager();
	}

	public static IPath getWorkingDirectory(ILaunchConfiguration configuration) throws CoreException {
		String location = configuration.getAttribute(IExternalToolConstants.ATTR_WORKING_DIRECTORY, (String) null);
		if (location != null) {
			String expandedLocation = getStringVariableManager().performStringSubstitution(location);
	...
	}
```

* DebugPlugin, 运行程序相关基础功能

```java
	// org.eclipse.debug.core.DebugPlugin
	public static String[] parseArguments(String args);
	public static Process exec(String[] cmdLine, File workingDirectory, String[] envp) throws CoreException;
```

```
	// org.eclipse.core.externaltools.internal.launchConfigurations.ExternalToolsCoreUtil
	public static String[] getArguments(ILaunchConfiguration configuration) throws CoreException {
		String args = configuration.getAttribute(IExternalToolConstants.ATTR_TOOL_ARGUMENTS, (String) null);
		if (args != null) {
			String expanded = getStringVariableManager().performStringSubstitution(args);
			return parseStringIntoList(expanded);
		}
		return null;
	}
```

```java
		// resolve arguments
		String[] arguments = ExternalToolsCoreUtil.getArguments(configuration);
		String[] envp = DebugPlugin.getDefault().getLaunchManager()
				.getEnvironment(configuration);
		Process p = DebugPlugin.exec(cmdLine, workingDir, envp);

		Map processAttributes = new HashMap();
		processAttributes.put(IProcess.ATTR_PROCESS_TYPE, programName);
		IProcess process = DebugPlugin.newProcess(launch, p, location.toOSString(),
				processAttributes);
		if (p == null || process == null) {
			if (p != null)
				p.destroy();
			throw new CoreException(new Status(IStatus.ERROR,
					IExternalToolConstants.PLUGIN_ID,
					IExternalToolConstants.ERR_INTERNAL_ERROR,
					ExternalToolsProgramMessages.ProgramLaunchDelegate_4, null));
		}
		process.setAttribute(IProcess.ATTR_CMDLINE,
				generateCommandLine(cmdLine));

		// wait for process to exit
		while (!process.isTerminated()) {
			try {
				if (monitor.isCanceled()) {
					process.terminate();
					break;
				}
				Thread.sleep(50);
			} catch (InterruptedException e) {
			}
		}

		// refresh resources
		RefreshUtil.refreshResources(configuration, monitor);
```

* ResourcesPlugin 资源管理

```java
	public static IWorkspace getWorkspace();
```

```java
IProject project= ResourcesPlugin.getWorkspace().getRoot().getProject(name);
```

