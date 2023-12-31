import os
import time
import pygame
import threading
import tkinter as tk
import ttkbootstrap as ttk
import tkinter.filedialog
from stop import stop_thread
from PIL import Image, ImageTk


def play():
    """
    播放音乐
    :return:
    """
    # clock = pygame.time.Clock()
    while True:
        if not event.wait():
            time.sleep(0.1)
        elif len(music_list):
            # clock.tick(60)
            pygame.mixer.init()
            global play_num
            if not pygame.mixer.music.get_busy():
                next_music = lb.curselection()
                if next_music == ():
                    nextMusic = music_list[play_num]
                    pygame.mixer.music.load(nextMusic.encode())
                    # 播放
                    pygame.mixer.music.play(1)
                    if len(music_list) - 1 == play_num:
                        play_num = 0
                    else:
                        play_num = play_num + 1
                else:
                    play_num = next_music[0]
                    nextMusic = music_list[play_num]
                    pygame.mixer.music.load(nextMusic.encode())
                    # 播放
                    pygame.mixer.music.play(1)
                    if len(music_list) - 1 == play_num:
                        play_num = 0
                    else:
                        play_num = play_num + 1
            else:
                time.sleep(0.1)


def buttonPlayClick():
    """
    点击播放
    :return:
    """
    buttonNext['state'] = 'normal'
    buttonPrev['state'] = 'normal'
    # 选择要播放的音乐文件夹
    if pause_resume.get() == '播放':  # 只执行一次
        pause_resume.set('暂停')
        global folder

        if not folder:
            folder = tkinter.filedialog.askdirectory()

        if not folder:
            return

        # 创建一个线程来播放音乐，当前主线程用来接收用户操作
        event.set()
        start()

    elif pause_resume.get() == '暂停':
        pygame.mixer.music.pause()
        pause_resume.set('继续')
        event.clear()

    elif pause_resume.get() == '继续':
        pygame.mixer.music.unpause()
        pause_resume.set('暂停')
        event.set()


def buttonNextClick():
    """
    下一首
    :return:
    """
    stop()
    pygame.mixer.music.pause()
    global play_num
    if len(music_list) == play_num:
        play_num = 0

    # 创建线程播放音乐,主线程用来接收用户操作
    start()


def closeWindow():
    """
    关闭窗口
    :return:
    """
    # 修改变量，结束线程中的循环

    global playing
    playing = False
    time.sleep(0.3)

    try:

        # 停止播放，如果已停止，

        # 再次停止时会抛出异常，所以放在异常处理结构中

        pygame.mixer.music.stop()

        pygame.mixer.quit()

    except:

        pass

    root.destroy()


def control_voice(value=0.5):
    """
    音量控制
    :param value: 0.0-1.0
    :return:
    """
    pygame.mixer.music.set_volume(float(int(value) / 100))


def buttonPrevClick():
    """
    上一首
    :return:
    """
    pygame.mixer.music.pause()
    stop()
    global play_num
    if play_num == 0:
        play_num = len(music_list) - 2
    elif play_num == len(music_list) - 1:
        play_num -= 2
    else:
        play_num -= 2

    # 创建一个线程来播放音乐，当前主线程用来接收用户操作
    start()


def vido():
    global show
    global volume_control
    if show:
        volume_control = tk.Frame(root, relief=tk.RAISED, bd=2)
        s = tk.Scale(volume_control, label='音量', from_=0, to=100, orient=tk.VERTICAL,
                     length=250, showvalue=True, tickinterval=25, resolution=1, command=control_voice)
        s.pack(side=tk.LEFT, anchor='nw')
        volume_control.pack(side=tk.BOTTOM, anchor='se')
        show = False
    else:
        volume_control.destroy()
        show = True


def setting():
    pass


def lyric():
    time_last = 0
    text_window.delete(1.0, tk.END)
    directory_name = os.path.dirname(music_list[play_num])
    file_name = os.path.basename(music_list[play_num])
    filename_without_ext, file_extension = os.path.splitext(file_name)  # 区分文件名和后缀
    lyric_file_name = directory_name + '/' + filename_without_ext + ".lrc"
    if os.path.exists(lyric_file_name):
        with open(lyric_file_name) as f:
            lyric_list = f.readlines()
        for i in lyric_list:
            lyric_text = i.strip()
            if lyric_text:
                if lyric_text[-1] == "]":
                    text_window.insert('insert', lyric_text+'\n')
                    continue
                else:
                    minute, second = lyric_text[1:9].split(":")
                    second = int(minute) * 60 + float(second)
                    time.sleep(second - time_last)
                    text_window.insert('insert', lyric_text[10:]+"\n")
                    time_last = second
            elif i == "\n":
                pass
            else:
                break
        exit()
    else:
        text_window.insert('insert', "没有歌词")


def start():
    global t_lyric
    global t_play
    t_lyric = threading.Thread(target=lyric)
    t_lyric.daemon = True
    t_lyric.start()
    t_play = threading.Thread(target=play)
    t_play.daemon = True
    t_play.start()


def stop():
    try:
        stop_thread(t_lyric)
        stop_thread(t_play)
    except ValueError:  # 线程提前退出
        pass


if __name__ == '__main__':
    event = threading.Event()
    root = ttk.Window()
    root.title('音乐播放器')
    root.geometry('1000x500')
    # root.resizable(False, False)  # 不能拉伸

    t_lyric = None
    t_play = None
    folder = ''  # 文件夹路径

    music_list = []  # 文件夹下的音乐路径
    play_num = 0  # 当前正在播放音乐的路径

    now_music = ''  # 正在播放音乐路径
    lb = None
    show = True  # 是否显示音量调整框
    volume_control = None  # 音量控制

    play_state = False  # 播放状态，决定“播放”按钮的text为“播放”还是“暂停”

    # 窗口关闭
    root.protocol('WM_DELETE_WINDOW', closeWindow)
    # 播放按钮
    fr1 = tk.Frame(root, relief=tk.RAISED, bd=5)
    buttonPrev = tk.Button(fr1, text='上一首', command=buttonPrevClick)
    buttonPrev.pack(side=tk.LEFT, anchor='nw', fill=tk.BOTH, padx=50, ipadx=10)
    buttonPrev['state'] = 'disabled'

    pause_resume = tk.StringVar(fr1, value='播放')
    buttonPlay = tk.Button(fr1, textvariable=pause_resume, command=buttonPlayClick)
    buttonPlay.pack(side=tk.LEFT, anchor='nw', fill=tk.BOTH, padx=40, ipadx=10)
    buttonPlay['state'] = 'disabled'

    buttonNext = tk.Button(fr1, text='下一首', command=buttonNextClick)
    buttonNext.pack(side=tk.LEFT, anchor='nw', fill=tk.BOTH, padx=50, ipadx=10)
    buttonNext['state'] = 'disabled'
    # 上一首

    b4 = tk.Button(fr1, text="音量", command=vido)
    b4.pack(side=tk.LEFT, anchor='nw', fill=tk.BOTH, padx=25, ipadx=10)

    b4 = tk.Button(fr1, text="设置", command=setting)
    b4.pack(side=tk.RIGHT, anchor='w', fill=tk.BOTH, ipadx=10)

    image = Image.open(r".\lib\python.jpg")
    pyt = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=pyt)
    text_window = tk.Text(root,)

    if not folder:
        folder = tkinter.filedialog.askdirectory()
        musics = [folder + '\\' + music for music in os.listdir(folder) if music.endswith(('.mp3', '.wav', '.ogg'))]
        ret = []
        for i in musics:
            ret.append(i.split('\\')[1:])
            music_list.append(i.replace('\\', '/'))

        var2 = tk.StringVar()
        var2.set(ret)
        lb = tk.Listbox(root, listvariable=var2)
        lb.pack(side=tk.LEFT, anchor='e', fill=tk.Y)
        fr1.pack(side=tk.BOTTOM, fill=tk.X)
        label.pack(side=tk.TOP, anchor='s', fill=tk.Y)
        text_window.pack(side=tk.TOP, anchor='s', fill=tk.Y)

    if not folder:
        exit(1)

    playing = True
    # 根据情况禁用和启用相应的按钮
    buttonPlay['state'] = 'normal'
    pause_resume.set('播放')
    # 显示
    root.mainloop()
