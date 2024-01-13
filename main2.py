import os
import json
import time
import pygame
import threading
import tkinter as tk
import ttkbootstrap as ttk
import tkinter.filedialog
from stop import stop_thread
from PIL import Image, ImageTk


def play():  # 播放音乐
    while True:
        while not event.wait():
            time.sleep(0.1)
        if len(music_list):
            pygame.mixer.init()
            global play_num
            global t_lyric
            global music_length
            if not pygame.mixer.music.get_busy():
                nextMusic = music_list[play_num]
                music_length = pygame.mixer.Sound(nextMusic).get_length()
                pygame.mixer.music.load(nextMusic)
                # 播放
                pygame.mixer.music.play(1)

                t_lyric = threading.Thread(target=lyric, args=(play_num,))
                t_lyric.daemon = True
                t_lyric.start()

                if len(music_list) - 1 == play_num:
                    play_num = 0
                else:
                    play_num = play_num + 1
            else:
                time.sleep(0.1)


def buttonPlayClick():  # 点击播放后的事件
    buttonNext['state'] = 'normal'
    buttonPrev['state'] = 'normal'
    if pause_resume.get() == '播 放':  # 只在第一次播放执行
        pause_resume.set('暂 停')

        # 创建线程来播放音乐和显示歌词，主线程负责接收用户操作
        event.set()
        start()

    elif pause_resume.get() == '暂 停':
        pygame.mixer.music.pause()
        pause_resume.set('继 续')
        event.clear()

    elif pause_resume.get() == '继 续':
        pygame.mixer.music.unpause()
        pause_resume.set('暂 停')
        event.set()


def buttonNextClick():  # 下一首
    pygame.mixer.music.pause()
    stop()
    global play_num
    if len(music_list) == play_num:
        play_num = 0

    start()
    pygame.mixer.music.unpause()
    pause_resume.set('暂 停')
    event.set()


def closeWindow():  # 关闭窗口
    try :
        stop()
    except AttributeError:  # 没有创建线程(即没有开始播放)的情况
        exit(0)
    with open(r'.\config\config.json', encoding='utf-8') as f:
        data = json.loads(f.read())
    data["volume_num"] = config["volume_num"]
    data["folder"] = config["folder"]
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    with open(r'.\config\config.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    time.sleep(0.1)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    root.destroy()


def control_voice(value=50):  # 音量控制
    """
    :param value: 0.0-1.0
    """
    try:
        global config
        config["volume_num"] = value
        pygame.mixer.music.set_volume(float(value) / 100)
    except pygame.error:  # 未播放音乐的情况
        pass


def buttonPrevClick():  # 上一首
    pygame.mixer.music.pause()
    stop()
    global play_num
    if play_num == 0:
        play_num = len(music_list) - 2
    elif play_num == len(music_list) - 1:
        play_num -= 2
    else:
        play_num -= 2

    start()
    pygame.mixer.music.unpause()
    pause_resume.set('暂 停')
    event.set()


def setting():  # 设置
    pass


def move(value=-1):
    if value != -1:
        pass
        # print(value)
    else:
        try:
            long = music_length * 1000
            while not event.wait():
                time.sleep(0.1)
            # now_long = pygame.mixer.music.get_pos()
            speech.set((pygame.mixer.music.get_pos() / long) * 100)
        except ZeroDivisionError:
            pass


def move2():
    clock = pygame.Clock()
    while True:
        clock.tick(60)
        move()


def lyric(play_num):  # 显示歌词
    time_last = 0
    text_window.delete(1.0, tk.END)
    directory_name = os.path.dirname(music_list[play_num])
    file_name = os.path.basename(music_list[play_num])
    lyric_file_name = directory_name + '/' + os.path.splitext(file_name)[0] + ".lrc"
    if os.path.exists(lyric_file_name):
        with open(lyric_file_name, encoding="ANSI") as f:
            lyric_list = f.readlines()
        for i in lyric_list:
            while not event.wait():
                time.sleep(0.1)
            text_window.see(tk.END)
            lyric_text = i.strip()
            if lyric_text:
                if lyric_text[-1] == "]":
                    text_window.insert('insert', lyric_text + '\n')
                    continue
                else:
                    minute, second = lyric_text[1:9].split(":")
                    second = int(minute) * 60 + float(second)
                    time.sleep(second - time_last)
                    text_window.insert('insert', lyric_text[10:] + "\n")
                    time_last = second
            elif i == "\n":
                pass
            else:
                break
        exit()
    else:
        text_window.insert('insert', "没有歌词")


def start():
    global t_play
    global t_music

    t_play = threading.Thread(target=play)
    t_play.daemon = True

    t_music = threading.Thread(target=move2)
    t_music.daemon = True

    t_play.start()
    t_music.start()


def stop():  # 强制结束线程
    stop_thread(t_play)
    stop_thread(t_music)
    stop_thread(t_lyric)
    event.set()


if __name__ == '__main__':
    event = threading.Event()
    root = ttk.Window()
    root.title('音乐播放器')
    # root.geometry('0x0')
    # root.resizable(False, False)  # 不能拉伸

    t_lyric = None
    t_play = None
    t_music = None

    music_list = []  # 文件夹下的音乐路径
    play_num = 0  # 当前正在播放音乐的位置
    music_length = 0
    config = {"volume_num": 50, "image_path": './lib/python.jpg', "folder": ''}
    now_music = ''
    lb = None

    # 窗口关闭
    root.protocol('WM_DELETE_WINDOW', closeWindow)
    # 按钮
    fr1 = tk.Frame(root, relief=tk.RAISED, bd=0)
    # 进度
    speech = tkinter.Scale(fr1, from_=0, to=100, orient=tk.HORIZONTAL, variable=1, resolution=1, showvalue=True,
                           width=5,
                           length=300, tickinterval=0, command=move)
    speech.grid(row=0, column=0, sticky="ew", padx=20, pady=5)
    # 音量
    volume = tkinter.Scale(fr1, from_=0, to=100, orient=tkinter.HORIZONTAL, variable=10, resolution=10, showvalue=True,
                           width=5,
                           length=300, tickinterval=2, command=control_voice)
    volume.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    fr2 = tk.Frame(root, relief=tk.RAISED, bd=0)
    # 上一首
    buttonPrev = tk.Button(fr2, text='上一首', command=buttonPrevClick)
    buttonPrev.grid(row=0, column=0, sticky="ew", padx=60, pady=5)
    buttonPrev['state'] = 'disabled'
    # 播放
    pause_resume = tk.StringVar(fr2, value='播 放')
    buttonPlay = tk.Button(fr2, textvariable=pause_resume, command=buttonPlayClick)
    buttonPlay.grid(row=0, column=1, sticky="ew", padx=60, pady=5)
    buttonPlay['state'] = 'disabled'
    # 下一首
    buttonNext = tk.Button(fr2, text='下一首', command=buttonNextClick)
    buttonNext.grid(row=0, column=2, sticky="ew", padx=60, pady=5)
    buttonNext['state'] = 'disabled'
    # 设置
    b4 = tk.Button(fr2, text=" 设 置 ", command=setting)
    b4.grid(row=0, column=3, sticky="ew", padx=60, pady=5)
    # 读取配置文件
    with open(r'.\config\config.json', "r",encoding='utf-8') as f:
        data_str = f.read()
        data = json.loads(data_str)
    for i in config:
        if i in data:  # 根据配置文件设置信息
            config[i] = data[i]

    volume.set(config["volume_num"])
    image = Image.open(config["image_path"])
    pyt = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=pyt)
    text_window = tk.Text(root)
    if not config["folder"] or not os.path.exists(config["folder"]):
        config["folder"] = tkinter.filedialog.askdirectory()
        if not config["folder"]:
            exit(0)
    else:
        pass

    musics = [config["folder"] + '\\' + music for music in os.listdir(config["folder"]) if music.endswith(('.mp3', '.wav', '.ogg'))]
    for i in musics:
        music_list.append(i.replace('\\', '/'))

    var2 = tk.StringVar()
    var2.set([i.split('/')[-1] for i in music_list])
    lb = tk.Listbox(root, listvariable=var2)
    lb.pack(side=tk.LEFT, anchor='e', fill=tk.Y)
    fr2.pack(side=tk.BOTTOM, fill=tk.X)
    fr1.pack(side=tk.BOTTOM, fill=tk.X)
    label.pack(side=tk.TOP, anchor='s', fill=tk.Y)
    text_window.pack(side=tk.TOP, anchor='s', fill=tk.Y)

    # 根据情况禁用和启用相应的按钮
    buttonPlay['state'] = 'normal'
    pause_resume.set('播 放')

    root.mainloop()
