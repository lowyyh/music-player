<!--
 * @Author: lowyyh lowyyh.com@outlook.com
 * @Date: 2024-01-06 10:54:39
 * @LastEditors: lowyyh lowyyh.com@outlook.com
 * @LastEditTime: 2024-01-14 17:19:10
 * @FilePath: \undefinedd:\desktop\programme\GUI项目\音乐播放器\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 1.简介
这是一款基于Python的简易音乐播放器, 使用pygame库实现播放音乐

运行方式很简单, 执行main.py或main2.py

main.py的GUI使用Python标准库tkinter

main2.py使用ttkbootstrap库

## 截图

## Windows

![Windows](https://gitee.com/lowyyh/own-images/raw/master/img.png)

## linux(以kali示范)

![Linux](https://gitee.com/lowyyh/own-images/raw/master/img2.png)

# 2.安装
## 1.克隆仓库

```bash
git clone https://gitee.com/lowyyh/music-player.git
```
## 2.安装第三方库:
### linux
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

# 注意:

    1.如果要打开其他音乐文件夹(或打开单个音乐文件), 请单击左上方的"文件"

    2.程序读取的歌词文件格式: 音乐文件名(不加后缀名).lrc