为保证运行效果，请尽量使用新版`powershell`运行。

需求语言环境：>= `python3.8`

#### 运行指南：
请确保你的电脑已安装符合需求的`python`环境
在本文件夹下打开`powershell`终端，键入  python .\main.py`

#### 打包指南：
本文件夹不包含打包所需文件库，请确保你已经安装了`pyinstaller`库。
若无，请在终端键入

`pip install pyinstaller`

在本文件夹下打开`powershell`终端，键入  

`pyinstaller --onefile main.py`
完成后运行`dist`文件夹下的`main.exe`文件或在`powershell`键入

 `.\main.exe`

即可