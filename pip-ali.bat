rem cheneyjin@outlook.com
@set /p input= pip install what? 
set user_input=%input%
set ali_mirrors= -i https://mirrors.aliyun.com/pypi/simple
set command=%user_input%%ali_mirrors%
call %%command%%