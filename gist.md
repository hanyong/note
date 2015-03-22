```sh
# java 调试参数, tomcat, eclipse 使用 "-agentlib:jdwp="
-agentlib:jdwp=transport=$JPDA_TRANSPORT,address=$JPDA_ADDRESS,server=y,suspend=$JPDA_SUSPEND 
-agentlib:jdwp=transport=dt_socket,address=8000,server=y,suspend=n
# maven 使用 "-Xrunjdwp:"
-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000

# eclipse 调试参数
eclipse -vmargs -agentlib:jdwp=transport=dt_socket,address=8000,server=y,suspend=n
```
