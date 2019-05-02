import discord
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver import Chrome, ChromeOptions
import youtube_dl
import os
import asyncio
TOKEN = "NTcyODU3ODc2MzM5NDkwODI5.XMiZjQ.4a1iHpZzcHlTMITMLuBKUiOi2MY"
youtube_url = "https://www.youtube.com/?gl=JP"
discord_voice_channel_id = ""
voice = None
player = None
client = discord.Client()
loop = asyncio.get_event_loop()
a = 1
def nextm(music_list):
    async def nex(music_list):
        CHANNEL_ID = 573056770025455636
        channel = client.get_channel(CHANNEL_ID)
        print("ok")
        if music_list != None:
            await channel.send("次の曲は")
        print(CHANNEL_ID)
    loop.run_until_complete(nex(music_list))
async def saisei(msg,music_list):
    CHANNEL_ID = 573031928857362452
    channel = client.get_channel(CHANNEL_ID)
    youtube_url = "https://www.youtube.com/results?search_query="
    serch_url = youtube_url + msg
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = Chrome(options=options)
    driver.get(serch_url)
    url_now = driver.find_element_by_id('thumbnail').get_attribute("href")
    print(url_now)
    await channel.send(url_now)
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl':  "sample_music" + '.%(ext)s',
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'},
        {'key': 'FFmpegMetadata'},
    ],
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(url_now, download=True)
    voice.play(discord.FFmpegPCMAudio('sample_music.mp3'),after = lambda e: nextm(music_list))
@client.event
async def on_ready():
    CHANNEL_ID = 573056770025455636
    channel = client.get_channel(CHANNEL_ID)
    msg = "MUSICBOTカッコカリがログインしました\n「起動」と打つと起動されます\n? 曲名で曲を再生\nhelpでコマンド一覧を表示します"
    await channel.send(msg)
    music_list = []
    return music_list
@client.event
async def on_message(message):
    global voice, player
    global music_list
    CHANNEL_ID = 573056770025455636
    channel = client.get_channel(CHANNEL_ID)
    msg = message.content
    mess = str(message)
    music_kind = mess.lstrip("起動")
    try:
        print(music_list)
    except:
        pass
    if message.author.bot:
        if msg == "次の曲は":
            nextmusic = music_list.pop(0)
            await channel.send(nextmusic + "です")
            loop.run_until_complete(saisei(nextmusic,music_list))
            return music_list
    elif msg in "起動":
        if message.author.voice.channel is None:
            await message.channel.send("ボイスチャンネルに参加してから起動してください")
        if voice == None:
            cha = message.author.voice.channel
            voice = await cha.connect()
            if cha == "部屋1":
                await channel.send("部屋1に接続しました")
        elif voice.is_connected() == True:
            if voice.is_playing:
                voice.stop()
                await voice.disconnect()
            cha = message.author.voice.channel
            voice = await cha.connect()
    elif msg == "移動":
        move = message.author.voice.channel
        await voice.disconnect()
        voice = await move.connect()
        voice.play(discord.FFmpegPCMAudio('sample_music.mp3'),after = lambda: os.remove("sample_music.mp3"))
    elif msg == "停止":
        if voice.is_playing():
            voice.stop()
            nextm(music_list)
            return
    elif msg == "切断":
        if voice is not None:
            await voice.disconnect()
            voice = None
            os.remove("sample_music.mp3")
            return
    elif "?" in msg:
        msg = msg.replace("?", "")
        if voice.is_playing():
            try:
                music_list.append(msg)
            except:
                music_list = [msg]
            CHANNEL_ID = 573056770025455636
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(msg + "を再生リストに追加しました")
        else:
            music_list = None
            loop.run_until_complete(saisei(msg,music_list))
    elif "リスト" == msg:
        count = 1
        for music in music_list:
            senmess = str(count) + "曲目..." + music
            await channel.send(senmess)
            count += 1
    elif "音量" in msg:
        msg = msg.replace("音量 ","")
        try:
            msg = int(msg) / 100
            voice.source = discord.PCMVolumeTransformer(voice.source,volume=1.0)
            voice.source.volume = float(msg)
            a *= float(msg) * 100
            vol = "現在の音量は" + str(a) + "%です"
            await channel.send(vol)
        except:
            pass
    elif "help" == msg:
        await message.channel.send("起動/BOTをサーバーに呼ぶ\n? 曲名で曲を再生\n停止/曲を止める\n切断/BOTをボイスチャンネルから追い出す\nhelp/コマンド一覧を表示する\n移動/前に再生していた曲を維持してBOTをサーバーに呼ぶ")
client.run(TOKEN)