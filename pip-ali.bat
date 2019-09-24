rem cheneyjin@outlook.com
@echo off
@set /p input= pip install what? 
if not "%input%"=="" ( call:downloadPythonLibs %input% )
goto:finish

:downloadPythonLibs
set user_input_lib=%1
set ali_mirrors=-i https://mirrors.aliyun.com/pypi/simple
set command=pip install %user_input_lib% %ali_mirrors%
call %command%
goto:eof

:finish
