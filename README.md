# 1.简介
这是一款基于Python的简易音乐播放器, 使用pygame库实现播放音乐</p>
<p>运行方式很简单, 执行main.py或main2.py</p>
<p>main.py的GUI使用Python标准库tkinter</p>
<p>main2.py使用ttkbootstrap库</p>
<p>提示: </p>
<p>    1.如果要打开其他音乐文件夹(或打开单个音乐文件), 请单击左上方的"文件"</p>
<p>    2.程序读取的歌词文件格式: 音乐文件名(不加后缀名).lrc</p>
<img src="https://gitee.com/lowyyh/own-images/raw/master/img.png">

# 2.安装
## 1.克隆仓库

```bash
git clone https://gitee.com/lowyyh/music-player.git
```
## 2.安装第三方库:
### linux:
首先安装Python3-tk包和pil包

基于Debian的Linux发行版（如Ubuntu、Linux Mint等）
```bash
sudo apt-get update
sudo apt-get install python3-tk
sudo apt-get install python3-pil
```
在基于RHEL的Linux发行版（如CentOS、Fedora等）
```bash
sudo yum install python3-tk
sudo yum install python3-pillow
```
或者，如果你使用的是基于Arch的Linux发行版（如Manjaro、Antergos等）
```bash
sudo pacman -S python-tk
sudo pacman -S python-pillow
```
然后安装Python第三方库(在这之前, 请确保已安装了pip包)

pip包的安装
```bash
sudo apt-get install python3-pip
```
pip安装pygame库
```bash
# 标准版
pip3 install pygame
# 社区版
pip3 install pygame-ce
```
### Windows
```cmd
pip install pillow
# 标准版
pip install pygame
# 社区版
pip install pygame-ce
```