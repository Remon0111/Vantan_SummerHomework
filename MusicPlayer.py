from tkinter import *
import tkinter as ttk
import sqlite3
import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')
import random
import threading
from pydub import AudioSegment
from pydub.playback import play
import threading

# 一つ目のウィンドウを追加
window = Tk()
window.geometry("500x700+450+100")
window.title("音楽プレイヤー")

mainMusicLabel = ttk.Label(window, text="RemonMusic!", font=("MSゴシック", "35", "bold"))
mainMusicLabel.grid(column=0, row=0, columnspan=4, ipadx=150, sticky=ttk.NW)


# ここでデーターベースと接続している
conn = sqlite3.connect("MusicList.db")
c = conn.cursor()

# 下の文ではデーターベースで何を取り出すのか決めている
def createNewMusic():
    # テーブルの作成
    c.execute("""
        CREATE TABLE IF NOT EXISTS AdvancedSetting(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musicVolume INTEGER NOT NULL,
            nowMusicPlayList TEXT NOT NULL
        )""")
    volume_list = "SELECT musicVolume FROM AdvancedSetting"
    Volume = c.execute(volume_list).fetchall()
    if len(Volume)==0:
        x = "INSERT INTO AdvancedSetting(musicVolume,nowMusicPlayList) VALUES(50,'music')"
        c.execute(x)
        conn.commit()
    music_list = "SELECT nowMusicPlayList FROM AdvancedSetting"
    musicList = c.execute(music_list).fetchall()
    Volume = c.execute(volume_list).fetchall()

    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {musicList[0][0]}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musicName TEXT NOT NULL,
            musicComposer TEXT NOT NULL,
            musicPath TEXT NOT NULL
        )""")

    nowMusicVolume = ttk.Label(window, text=f"音量:{Volume[0][0]}", font=("MSゴシック", "15"))
    nowMusicVolume.grid(column=0, row=0, sticky=ttk.NW)
    nowMusicPlayList = ttk.Label(window, text=f"プレイリスト:{musicList[0][0]}", font=("MSゴシック", "15"))
    nowMusicPlayList.grid(column=0, row=0, pady=20, sticky=ttk.NW)

    query = "SELECT musicPath FROM music"


    def play_music():
        c.execute(query)
        for play_list in c.fetchall():
            audio = AudioSegment.from_file(play_list[0])
            x = Volume[0][0] - 50
            playAudio = audio + x
            print(playAudio)
            play(playAudio)
            thread1 = threading.Thread(target=play_music)
            thread1.start()
            thread1.join()

    # ランダムに曲を再生する処理
    def random_music():
        c.execute(query)
        random_list = []
        for randomSerect in c.fetchall():
            random_list.append(randomSerect)
        random.shuffle(random_list)
        SerectNumber1 = 0
        for random_PlayMusic in random_list:
            audio = AudioSegment.from_file(random_PlayMusic[SerectNumber1])
            x = Volume[0][0] - 50
            playAudio = audio + x
            print(playAudio)
            play(playAudio)
            SerectNumber1 += 1
        thread2 = threading.Thread(target=random_music)
        thread2.start()
        thread2.join()

    # 曲を最初から再生するボタンを追加
    playButton = ttk.Button(window, text="曲を最初から再生", command=play_music)
    # 曲をランダムに再生するボタンを追加
    randomButton = ttk.Button(window, text = "曲をランダムに再生", command=random_music)

    playButton.grid(column=0, row=1, ipadx=56, ipady=2, sticky=ttk.NW, padx=0)
    randomButton.grid(column=0, row=1, ipadx=56, ipady=2, sticky=ttk.NW, padx=245)

    # 下の文は曲の番号を出力する処理です。

    musicIdDb = "SELECT id FROM music"
    c.execute(musicIdDb)
    serectNumber1 = 2
    for Id in c.execute(musicIdDb):
        musicId = ttk.Label(window, text = Id, font=("MSゴシック", "18"))
        musicId.grid(column=0, row=serectNumber1, sticky=ttk.W, padx=(50, 0))
        m = ttk.Label(window, text="|", font=("MSゴシック", "18"))
        m.grid(column=0, row=serectNumber1, sticky=ttk.W, padx=(90, 0))
        serectNumber1 = serectNumber1 + 1


    # 下の文は曲名を出力する処理です。
    musicNameDb = "SELECT musicName FROM music"
    c.execute(musicNameDb)
    musicName_list = []
    serectNumber2 = 2
    for MusicNameSerect in c.execute(musicNameDb):
        musicName_list.append(MusicNameSerect)
    SerectNumber2 = 0
    for i in musicName_list:
        musicName = ttk.Label(window, text = i, font=("MSゴシック", "18"))
        musicName.grid(column=0, row=serectNumber2, sticky=ttk.W, padx=(120, 0))
        serectNumber2 = serectNumber2 + 1
        SerectNumber2 += 1

    # 下の文は作曲者の名前を出力する処理です。
    musicComposerDb = "SELECT musicComposer FROM music"
    c.execute(musicComposerDb)
    serectNumber3 = 2
    for composer in c.execute(musicComposerDb):
        musicComposer = ttk.Label(window, text = composer, font=("MSゴシック", "18"))
        musicComposer.grid(column=0, row=serectNumber3, sticky=ttk.W, padx=(250, 0))
        s = ttk.Label(window, text="|", font=("MSゴシック", "18"))
        s.grid(column=0, row=serectNumber3, sticky=ttk.W, padx=(220, 0))
        serectNumber3 = serectNumber3 + 1
createNewMusic()

# ここまでが一つ目のウィンドウの処理
def newMusicWindow():
    global secwinopen
    if not secwinopen:
        secwinopen = True
        secondWindow = Toplevel()
        secondWindow.title("新しい曲を追加")

        # musicAlbumNameLabel = ttk.Label(secondWindow, text = "追加したい曲のアルバム写真の名前を追加してください")
        # musicAlbumNameEntry = ttk.Entry(secondWindow)
        musicNameLabel = ttk.Label(secondWindow, text = "追加したい曲名を記入してください", font=("MSゴシック", "15", "bold"))
        musicNameEntry = ttk.Entry(secondWindow)
        musicComposerLabel = ttk.Label(secondWindow, text = "追加したい曲の作曲者名を記入してください", font=("MSゴシック", "15", "bold"))
        musicComposerEntry = ttk.Entry(secondWindow)
        musicPathLabel = ttk.Label(secondWindow, text = "追加したい曲のpathを記入してください", font=("MSゴシック", "15", "bold"))
        musicPathEntry = ttk.Entry(secondWindow)

        # musicAlbumNameLabel.pack()
        # musicAlbumNameEntry.pack()
        musicNameLabel.pack()
        musicNameEntry.pack()
        musicComposerLabel.pack()
        musicComposerEntry.pack()
        musicPathLabel.pack()
        musicPathEntry.pack()

        musicError = ttk.Label(secondWindow, text="", font=("MSゴシック", "13"))

    # 下の関数の処理はEntryに入力された情報の取得とEntryに情報が入力されなかった場合の処理です
        def playMusic():
            global MusicName
            global MusicComposer
            global MusicPath
            MusicName = musicNameEntry.get().lstrip()
            MusicComposer = musicComposerEntry.get().rstrip()
            MusicPath = musicPathEntry.get().lstrip()
            # 下の関数はEntryに情報が入力されていなかった場合の処理です
            if MusicName == "" or MusicComposer == "" or MusicPath == "":
                musicError["text"] = "*必要な情報が入力されていません"
            else :
                list = "INSERT INTO music(musicName, musicComposer, musicPath) VALUES (?, ?, ?)"
                c.execute(list, (MusicName, MusicComposer, MusicPath))
                conn.commit()
                click_close_sub()

        # 下の文はDBにEntryの情報を入れる処理を作りました
        newMusicButton = ttk.Button(secondWindow, text = "曲を追加する", command = lambda:[playMusic()])
        newMusicButton.pack()

        musicError.pack()
        secondWindow.resizable(width=False, height=False)

        def click_close_sub():
            global secwinopen
            secwinopen = False
            secondWindow.destroy()

        secondWindow.protocol("WM_DELETE_WINDOW", click_close_sub)


newMusicWindowButton = ttk.Button(window, text="曲を追加する", command=newMusicWindow)
newMusicWindowButton.place(x=380, y=-4)

def settingWindow():
    global thiwinopen
    if not thiwinopen:
        thiwinopen = True
        thirdWindow = Toplevel()
        thirdWindow.title("詳細設定")

        volume_list = "SELECT musicVolume FROM AdvancedSetting"
        Volume = c.execute(volume_list).fetchall()
        volumeSet_label = ttk.Label(thirdWindow, text="音量設定")
        volumeSet_label.grid(column=0,  row=0)
        # 音量調整用の変数
        volume = ttk.DoubleVar()
        volume.set(Volume)
        # ttkのスライダーバーの作成
        scale = ttk.Scale(thirdWindow, variable=volume, from_=0.0, to=100.0, orient="horizontal", length=300, label=f"現在音量:{Volume[0][0]}")
        scale.grid(column=0, row=1)
        # 音量を表示するラベル
        volume_label = ttk.Label(thirdWindow, text="音量: 0.0")
        volume_label.grid(column=0, row=1)

        # スライダーバーの値が変更されたときに呼び出される関数
        def update_volume_label(event):
            volume_label.config(text=f"音量: {volume.get()}")

        # スライダーバーの値変更イベントを関数にバインド
        scale.bind("<Motion>", update_volume_label)

        musicVolume = volume.get()
        def updateMusicVolume():
            volume_list = f"UPDATE AdvancedSetting SET musicVolume = {volume.get()}"
            c.execute(volume_list)
            conn.commit()

        playlist_label = ttk.Label(thirdWindow, text="プレイリスト")
        playlist_label.grid(column=0, row=4, ipady=15)

        playlist_entry = ttk.Entry(thirdWindow)
        playlist_entry.grid(column=0, row=5)

        nowplaylist = ttk.Label(thirdWindow, text="現在のプレイリスト")
        nowplaylist.grid(column=0, row=6,)

        music_list = "SELECT nowMusicPlayList FROM AdvancedSetting"
        musicList = c.execute(music_list).fetchall()
        nowplaylist= ttk.Label(thirdWindow, text=musicList[0][0])
        nowplaylist.grid(column=0, row=7)

        def update_playlist_list():
            PlayList = f"UPDATE AdvancedSetting SET nowMusicPlayList = '{playlist_entry.get().lstrip()}'"
            c.execute(PlayList)
            conn.commit()

        volume_button = ttk.Button(thirdWindow, text="変更を確定する", command=lambda:[update_playlist_list(),  updateMusicVolume(), createNewMusic(), click_close_sub()])
        volume_button.grid(column=0, row=8)

        def click_close_sub():
            global thiwinopen
            thiwinopen = False
            thirdWindow.destroy()

        thirdWindow.protocol("WM_DELETE_WINDOW", click_close_sub)

settingWindowButton = ttk.Button(window, text="詳細設定", command=settingWindow)
settingWindowButton.place(x=380, y=22)

# def deleteMusicWindow():

window.resizable(width=False, height=False)
secwinopen = False
thiwinopen = False
window.mainloop()
conn.close()
