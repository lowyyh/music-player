import os
import time
import pygame
import ctypes
import inspect
import threading
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk


def async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    async_raise(thread.ident, SystemExit)


def buttonChooseClick():
    """
    添加文件夹
    :return:
    """
    global folder
    global res
    global lb
    global fr1
    global label
    global text_window
    if not folder:
        folder = tkinter.filedialog.askdirectory()
        musics = [folder + '\\' + music
                  for music in os.listdir(folder) \
 \
                  if music.endswith(('.mp3', '.wav', '.ogg'))]
        ret = []
        for i in musics:
            ret.append(i.split('\\')[1:])
            res.append(i.replace('\\', '/'))

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
    global play_l
    playing = True
    play_l = True
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
            if len(res):
                pygame.mixer.init()
                global num
                if not pygame.mixer.music.get_busy():
                    next_music = lb.curselection()
                    if next_music == ():
                        nextMusic = res[num]
                        print(nextMusic)
                        print(num)
                        pygame.mixer.music.load(nextMusic.encode())
                        # 播放
                        pygame.mixer.music.play(1)
                        if len(res) - 1 == num:
                            num = 0
                        else:
                            num = num + 1
                        netxMusic = nextMusic.split('\\')[1:]
                        musicName.set('                                      playing......' + ''.join(netxMusic))
                    else:
                        num = next_music[0]
                        nextMusic = res[num]
                        print(nextMusic)
                        print(num)
                        pygame.mixer.music.load(nextMusic.encode())
                        # 播放
                        pygame.mixer.music.play(1)
                        if len(res) - 1 == num:
                            num = 0
                        else:
                            num = num + 1
                        netxMusic = nextMusic.split('\\')[1:]
                        musicName.set('                                      playing......' + ''.join(netxMusic))
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
        global play_l
        playing = True
        play_l = True

        # 创建一个线程来播放音乐，当前主线程用来接收用户操作
        t = threading.Thread(target=play)
        t.daemon = True
        global t_lyric
        t_lyric = threading.Thread(target=lyric)
        t_lyric.daemon = True
        t.start()
        t_lyric.start()

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
    global play_l
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
    global play_l
    playing = False
    play_l = False
    play_state = False
    pygame.mixer.music.stop()
    global num
    if len(res) == num:
        num = 0

    playing = True
    play_l = True
    play_state = True
    # 创建线程播放音乐,主线程用来接收用户操作
    t = threading.Thread(target=play)
    t.daemon = True
    global t_lyric
    # stop_thread(t_lyric)
    t_lyric = threading.Thread(target=lyric)
    t_lyric.daemon = True
    t.start()
    t_lyric.start()


def closeWindow():
    """
    关闭窗口
    :return:
    """
    # 修改变量，结束线程中的循环

    global playing
    global play_l
    playing = False
    play_l = False
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
    声音控制
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
    global play_l
    global play_state

    playing = False
    play_l = False
    play_state = False

    pygame.mixer.music.stop()
    #
    # pygame.mixer.quit()
    global num
    # num += 1
    # num -= 1
    if num == 0:
        num = len(res) - 2
        # num -= 1
    elif num == len(res) - 1:
        num -= 2
    else:
        num -= 2
        # num -= 1
    print(num)

    playing = True
    play_l = True
    play_state = True

    # 创建一个线程来播放音乐，当前主线程用来接收用户操作

    t = threading.Thread(target=play)
    t.daemon = True
    global t_lyric
    # stop_thread(t_lyric)
    t_lyric = threading.Thread(target=lyric)
    t_lyric.daemon = True
    t.start()
    t_lyric.start()


def vido():
    global if_
    global fr
    if if_:
        fr = tk.Frame(root, relief=tk.RAISED, bd=2)
        s = tk.Scale(fr, label='音量', from_=0, to=100, orient=tk.VERTICAL,
                     length=250, showvalue=True, tickinterval=25, resolution=1, command=control_voice)
        s.pack(side=tk.LEFT, anchor='nw')
        fr.pack(side=tk.BOTTOM, anchor='se')
        if_ = False
    else:
        fr.destroy()
        if_ = True


def setting():
    pass


def next_lyric_function(file_name):
    with open(file_name) as f:
        lyric_text = True
        number = 0
        while lyric_text:
            try:
                global play_l
                lyric_text = f.readline()
                lyric_text.strip()
                # print(lyric_text[1:9])
                minute, second = lyric_text[1:9].split(":")
                one, two = second.split('.')
                second = int(minute) * 60 + int(one) + int(one) / 100
                if not number:
                    yield lyric_text[10:] + "\n"
                else:
                    # time.sleep(second - last_second)
                    stopping = True
                    while stopping:
                        if not play_l:
                            yield "exit"
                        done = True
                        while play_state and done:
                            if time_stamp + second - last_second <= time.time():
                                yield lyric_text[10:] + "\n"
                                done = False
                                stopping = False
                                continue
                            if not play_l:
                                yield "exit"
                        if not play_l:
                            yield "exit"
                        if not play_state:
                            yield "[I have been to sleep..."
                            time_stamp = time.time()
                            continue
                last_second = second
                number += 1
                time_stamp = time.time()
                done = True
            except:
                pass
        yield None


def lyric():
    text_window.delete(1.0, tk.END)
    global res
    global num
    directory_name = os.path.dirname(res[num])
    file_name = os.path.basename(res[num])
    filename_without_ext, file_extension = os.path.splitext(file_name)
    try:
        # print(directory_name + '/' + filename_without_ext + ".lrc")
        with open(directory_name + '/' + filename_without_ext + ".lrc") as f:
            pass
    except FileNotFoundError:
        text_window.insert('insert', "没有歌词")
    else:
        next_lyric = next_lyric_function(directory_name + '/' + filename_without_ext + ".lrc")
        while playing:
            text = next(next_lyric)
            if text is None:
                break
            elif text == "[I have been to sleep...":
                while not play_state:
                    pass
                text = next(next_lyric)
                text_window.insert('insert', text)
            elif text == "exit":
                return
                # exit(0)
                # "i"-1
            else:
                text_window.insert('insert', text)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('音乐播放器')
    root.geometry('800x400')
    # root.resizable(False, False)  # 不能拉伸

    folder = ''  # 文件夹路径
    res = []
    num = 0
    t_lyric = None
    play_l = False
    playing = None
    now_music = ''  # 播放音乐路径
    if_ = True
    fr = None
    lb = None
    play_state = False

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

    # # 停止按钮
    # buttonStop = tk.Button(fr1, text='停止', command=buttonStopClick)
    # buttonStop.pack(side=tk.LEFT, anchor='nw', fill=tk.BOTH)
    # buttonStop['state'] = 'disabled'

    # 下一首
    buttonNext = tk.Button(fr1, text='下一首', command=buttonNextClick)
    buttonNext.pack(side=tk.LEFT, anchor='nw', fill=tk.BOTH, padx=50, ipadx=10)
    buttonNext['state'] = 'disabled'
    # 上一首

    b4 = tk.Button(fr1, text="音量", command=vido)
    b4.pack(side=tk.LEFT, anchor='nw', fill=tk.BOTH, padx=25, ipadx=10)

    b4 = tk.Button(fr1, text="设置", command=setting)
    b4.pack(side=tk.RIGHT, anchor='w', fill=tk.BOTH, ipadx=10)

    # 标签
    musicName = tk.StringVar(root)
    labelName = tk.Label(root, textvariable=musicName)
    labelName.pack(side=tk.TOP, anchor='s')

    image = Image.open(r".\lib\python.jpg")
    pyt = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=pyt)

    text_window = tk.Text(root, )

    buttonChooseClick()
    # 显示
    root.mainloop()
