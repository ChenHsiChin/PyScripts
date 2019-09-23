rem cheneyjin@outlook.com
@set /p input= pip install what? 
set user_input_lib=%input%
set ali_mirrors= -i https://mirrors.aliyun.com/pypi/simple
set command=pip install %user_input_lib%%ali_mirrors%
call %%command%%
