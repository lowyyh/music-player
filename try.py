import os
import time
import pygame
import ctypes
import inspect
import threading
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk


def buttonChooseClick():
    """
    添加文件夹
    :return:
    """
    global folder
    global music_list
    global lb
    global fr1
    global label
    if not folder:
        folder = tkinter.filedialog.askdirectory()
        musics = [folder + '\\' + music
                  for music in os.listdir(folder) \
 \
                  if music.endswith(('.mp3', '.wav', '.ogg'))]
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
        return

    global playing
    playing = True
    # 根据情况禁用和启用相应的按钮
    buttonPlay['state'] = 'normal'
    # buttonStop['state'] = 'normal'
    # buttonPause['state'] = 'normal'
    pause_resume.set('播放')


def play():
    """
    播放音乐
    :return:
    """
    global lb
    while playing:
        if play_state:
            if len(music_list):
                pygame.mixer.init()
                global play_num
                if not pygame.mixer.music.get_busy():
                    next_music = lb.curselection()
                    if next_music == ():
                        nextMusic = music_list[play_num]
                        print(nextMusic)
                        print(play_num)
                        pygame.mixer.music.load(nextMusic.encode())
                        # 播放
                        pygame.mixer.music.play(1)
                        if len(music_list) - 1 == play_num:
                            play_num = 0
                        else:
                            play_num = play_num + 1
                        play_num = next_music[0]
                        nextMusic = music_list[play_num]
                        print(nextMusic)
                        print(play_num)
                        pygame.mixer.music.load(nextMusic.encode())
                        # 播放
                        pygame.mixer.music.play(1)
                        if len(music_list) - 1 == play_num:
                            play_num = 0
                        else:
                            play_num = play_num + 1
                        netxMusic = nextMusic.split('\\')[1:]
                else:
                    time.sleep(0.1)


def buttonPlayClick():
    """
    点击播放
    :return:
    """
    global play_state
    buttonNext['state'] = 'normal'

    buttonPrev['state'] = 'normal'
    # 选择要播放的音乐文件夹
    if pause_resume.get() == '播放':
        play_state = True
        pause_resume.set('暂停')
        global folder

        if not folder:
            folder = tkinter.filedialog.askdirectory()

        if not folder:
            return

        global playing
        playing = True

        # 创建一个线程来播放音乐，当前主线程用来接收用户操作
        t = threading.Thread(target=play)
        t.daemon = True
        t.start()

    elif pause_resume.get() == '暂停':
        # pygame.mixer.init()
        play_state = False
        pygame.mixer.music.pause()

        pause_resume.set('继续')

    elif pause_resume.get() == '继续':
        # pygame.mixer.init()
        play_state = True
        pygame.mixer.music.unpause()

        pause_resume.set('暂停')


def buttonStopClick():
    """
    停止播放
    :return:
    """
    global playing
    global play_state
    playing = False
    play_state = False
    pygame.mixer.music.stop()


def buttonNextClick():
    """
    下一首
    :return:
    """
    global playing
    global play_state
    playing = False
    play_state = False
    pygame.mixer.music.stop()
    global play_num
    if len(music_list) == play_num:
        play_num = 0

    play_state = True
    # 创建线程播放音乐,主线程用来接收用户操作
    t = threading.Thread(target=play)
    t.daemon = True
    t.start()


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
    global playing
    global play_state

    playing = False
    play_state = False

    pygame.mixer.music.stop()
    #
    # pygame.mixer.quit()
    global play_num
    # num += 1
    # num -= 1
    if play_num == 0:
        play_num = len(music_list) - 2
        # num -= 1
    elif play_num == len(music_list) - 1:
        play_num -= 2
    else:
        play_num -= 2
        # num -= 1
    print(play_num)

    playing = True
    play_state = True

    # 创建一个线程来播放音乐，当前主线程用来接收用户操作

    t = threading.Thread(target=play)
    t.daemon = True
    t.start()


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


def next_lyric_function(file_name):
    pass


def lyric():
    time_stamp = time.time()
    text_window.delete(1.0, tk.END)
    directory_name = os.path.dirname(music_list[play_num])
    file_name = os.path.basename(music_list[play_num])
    filename_without_ext, file_extension = os.path.splitext(file_name)  # 区分文件名和后缀
    lyric_file_name = directory_name + '/' + filename_without_ext + ".lrc"
    if os.path.exists(lyric_file_name):
        with open(lyric_file_name) as f:
            lyric_text = True
            number = 0
            while lyric_text:
                try:
                    lyric_text = f.readline()
                    lyric_text.strip()
                    if lyric_text[-1] == "]":
                        text_window.insert('insert', lyric_text)
                        continue
                    else:
                        minute, second = lyric_text[1:9].split(":")
                        second += int(minute) * 60
                except:
                    pass
    else:
        text_window.insert('insert', "没有歌词")


def start():
    event.set()
    t_lyric = threading.Thread(target=lyric)
    t_lyric.daemon = True
    t = threading.Thread(target=play)
    t.daemon = True
    t.start()


if __name__ == '__main__':
    event = threading.Event()
    root = tk.Tk()
    root.title('音乐播放器')
    root.geometry('800x400')
    # root.resizable(False, False)  # 不能拉伸

    folder = ''  # 文件夹路径
    music_list = []  # 文件夹下的音乐路径
    play_num = 0  # 当前正在播放音乐的路径

    playing = None  # 是否正在播放

    now_music = ''  # 正在播放音乐路径
    show = True  # 是否显示音量调整框
    volume_control = None  # 音量控制
    lb = None
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
    text_window = tk.Text(root, )

    buttonChooseClick()
    # 显示
    root.mainloop()
