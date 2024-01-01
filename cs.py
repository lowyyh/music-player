import pygame
import time
from threading import Thread ,Event
import tkinter as tk


def main():
    music_long = length * 1000
    global now_long
    while True:
        while not event.wait():
            time.sleep(0.1)
        now_long = pygame.mixer.music.get_pos()
        event2.clear()
        volume.set((now_long / music_long)*100)
        event2.set()


def control_voice(vales):
    if event.wait():
        now_long = vales


event = Event()
event2 = Event()
now_long = 0
pos = 0
root = tk.Tk()
pygame.mixer.init()
music_file = "Daylight (cover：贵族乐团) (恶魔城西变速版) - Seredris.mp3"  # 请将此处替换为你的音乐文件路径
length = pygame.mixer.Sound(music_file).get_length()
# 设置音量
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(1)
volume = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=1, resolution=1, showvalue=True, width=5,
                  length=500, tickinterval=20, command=control_voice)
volume.grid(row=0, column=0)
bt1 = tk.Button(root, text="继续", command=pygame.mixer.music.unpause)
bt2 = tk.Button(root, text="暂停", command=pygame.mixer.music.pause)
bt1.grid(row=0, column=1)
bt2.grid(row=0, column=2)
event.set()
t = Thread(target=main)
t.daemon = True
t.start()
root.mainloop()
# 加载音乐文件
# music_file = "Daylight (cover：贵族乐团) (恶魔城西变速版) - Seredris.mp3"  # 请将此处替换为你的音乐文件路径
# m = pygame.mixer.Sound(music_file)
# # 设置音量
# pygame.mixer.music.set_volume(1.0)
#
# pygame.mixer.music.load(music_file)
# pygame.mixer.music.play(1)
#
# music_duration = pygame.mixer.Sound.get_length(m)
# print(music_duration)
# print()
# n = 0
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             exit(0)
#         elif event.type == pygame.KEYDOWN:
#             start = pygame.mixer.music.get_pos()
#             pygame.mixer.music.set_pos(30)
#             end = pygame.mixer.music.get_pos()
#             print(end - start)
#             print(end)
#             print()
#     if not n:
#         s = pygame.mixer.music.get_pos()
#         time.sleep(1)  # 1000
#         print(pygame.mixer.music.get_pos() - s)
#         n += 1
#         print()
#     else:
#         start = pygame.mixer.music.get_pos()
#         pygame.mixer.music.set_pos(30)
#         end = pygame.mixer.music.get_pos()
#         print(end - start)
#         print(end)
#         print()
