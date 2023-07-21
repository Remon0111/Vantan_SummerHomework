# 下の文でtkinterをpythonファイルにインポート
from tkinter import *
# 下の文でtkinterの拡張系であるttkをインポート
from tkinter import ttk
# 下の文でplaysoundをインポート
from playsound import playsound


# 曲を流す処理
def play_music():
    with playsound(r"/Users/hashimotoren/Desktop/likemusic/FujiiKaze-Garden.mp3"):
        pass

# 一つ目のウィンドウを追加
window = Tk()
window.title("音楽プレイヤー")

# 曲を最初から再生するボタンを追加
playButton = ttk.Button(window, text = "曲を最初から再生", command = play_music)
# 曲をランダムに再生するボタンを追加
randomButton = ttk.Button(window, text = "曲をランダムに再生")

playButton.pack(side = LEFT)
randomButton.pack(side = LEFT)

#ここまでが一番最初のウィンドウの処理

secondWindow = Toplevel()
secondWindow.title("新しい曲を追加")

# musicAlbumNameLabel = ttk.Label(secondWindow, text = "追加したい曲のアルバム写真の名前を追加してください")
# musicAlbumNameEntry = ttk.Entry(secondWindow)
musicNameLabel = ttk.Label(secondWindow, text = "追加したい曲名を記入してください")
musicNameEntry = ttk.Entry(secondWindow)
musicComposerLabel = ttk.Label(secondWindow, text = "追加したい曲の作曲者名を記入してください")
musicComposerEntry = ttk.Entry(secondWindow)
musicPathLabel = ttk.Label(secondWindow, text = "追加したい曲のpathを記入してください")
musicPathEntry = ttk.Entry(secondWindow)

# musicAlbumNameLabel.pack()
# musicAlbumNameEntry.pack()
musicNameLabel.pack()
musicNameEntry.pack()
musicComposerLabel.pack()
musicComposerEntry.pack()
musicPathLabel.pack()
musicPathEntry.pack()

# 下の文は曲を追加するボタンの処理です
newMusicButton = ttk.Button(secondWindow, text = "曲を追加する", command = playMusic)
newMusicButton.pack()

window.mainloop()