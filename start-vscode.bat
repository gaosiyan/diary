@echo off

:: 当前目录压栈并切换到当前脚本所在的目录
pushd % ~dp0

:: 定义路径
set pixi_home=D:\bin\pixi-x86_64-pc-windows-msvc
set python_home=%cd%\.pixi\envs\default
set vscode_home=D:\bin\vs_code\VSCode-win32-x64-1.107.1_Sphinx

set path=%pixi_home%;%python_home%;%python_home%\Library\mingw-w64\bin;%python_home%\Library\usr\bin;%python_home%\Library\bin;%python_home%\Scripts;%python_home%\bin;%vscode_home%;%path%

start code .

:: 恢复目录
popd

exit /b 0