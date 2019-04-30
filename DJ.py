import discord
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver import Chrome, ChromeOptions
import youtube_dl
import os
TOKEN = "NTcyODU3ODc2MzM5NDkwODI5.XMiZjQ.4a1iHpZzcHlTMITMLuBKUiOi2MY"
youtube_url = "https://www.youtube.com/?gl=JP"
discord_voice_channel_id = ""
voice = None
player = None
client = discord.Client()
@client.event
async def on_ready():
    CHANNEL_ID = 389693148923691009
    channel = client.get_channel(CHANNEL_ID)
    msg = "MUSICBOTカッコカリがログインしました\n「起動」と打つと起動されます\n? 曲名で曲を再生\nhelpでコマンド一覧を表示します"
    await channel.send(msg)

@client.event
async def on_message(message):
    global voice, player
    msg = message.content
    mess = str(message)
    music_kind = mess.lstrip("起動")
    cha = message.author.voice.channel
    if message.author.bot:
        return
    elif msg in "起動":
        if message.author.voice.channel is None:
            await message.channel.send("ボイスチャンネルに参加してから起動してください")
        if voice == None:
            if discord_voice_channel_id == "":
                voice = await cha.connect()
            else:
                voice = await cha.connect()
        elif voice.is_connected() == True:
            if voice.is_playing:
                player.stop()
            if discord_voice_channel_id:
                await voice.move_to(message.author.voice_chnnel)
            else:
                await voice.move_to(client.get_channel(discord_voice_channel_id))
    elif msg == "停止":
        if voice.is_playing():
            voice.stop()
            os.remove("sample_music.mp3")
            return
    elif msg == "切断":
        if voice is not None:
            await voice.disconnect()
            voice = None
            return
    elif "?" in msg:
        msg.replace("?","")
        youtube_url = "https://www.youtube.com/results?search_query="
        serch_url = youtube_url + msg
        options = ChromeOptions()
        options.add_argument("--headless")
        driver = Chrome(options=options)
        driver.get(serch_url)
        url_now = driver.find_element_by_id('thumbnail').get_attribute("href")
        print(url_now)
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
        voice.play(discord.FFmpegPCMAudio('sample_music.mp3'))
    elif "help" == msg:
        message.channel.send("起動/BOTをサーバーに呼ぶ\n? 曲名で曲を再生\n停止/曲を止める\n切断/BOTをボイスチャンネルから追い出す\nhelp/コマンド一覧を表示する")
client.run(TOKEN)