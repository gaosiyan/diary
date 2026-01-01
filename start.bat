@echo off

:: 当前目录压栈并切换到当前脚本所在的目录
pushd % ~dp0
call setup-env.bat
set path=%pixi_home%;%python_home%;%python_home%\Library\mingw-w64\bin;%python_home%\Library\usr\bin;%python_home%\Library\bin;%python_home%\Scripts;%python_home%\bin;%vscode_home%;%path%

sphinx-autobuild source build/html --open-browser --port=0