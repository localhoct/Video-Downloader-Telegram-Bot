# -*- coding: utf-8 -*-

import requests, os, validators
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton

api_id = 123456789 #int of api id get from my.telegram.org
api_hash = " Your Api Hash Here " #str of api hash get from my.telegram.org
token = ' Your Bot Token here ' #str of token get from BotFather
app = Client("Downlaoder", api_id, api_hash, bot_token=token) # You Can Change The Session Name by Replace "Downlaoder" to your session name


def downloada(url, quality):
    
    if quality == "1":
        ydl_opts_start = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', #This Method Need ffmpeg
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'http_chunk_size': 20097152,
            'writethumbnail': True

        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return title
    
    if quality == "2":
        ydl_opts_start = {
            'format': 'best', #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
    
    if quality == "3":
        ydl_opts_start = {
            'format': 'best[height=480]',
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'

# here you can Edit Start message
@app.on_message(filters.command('start', '/'))
def start(c, m): # c Mean Client | m Mean Message
    m.reply_text('Hi Welcome To @iLoaderBot \n Just Send Video Url To me and i\'ll try to upload the video and send it to you') #Edit it and add your Bot ID :)


@app.on_message(filters.regex(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"))
def webpage(c, m): # c Mean Client | m Mean Message
    url1 = m.text
    if validators.url(url1):
        sample_url = "https://da.gd/s?url={}".format(url1)
        url = requests.get(sample_url).text
        chat_id = m.chat.id
        keys = c.send_message(
            chat_id,
            f"Okay!!🙄\n {url1} is Video Url😊 \n\nPlease Select Quality :\n💡The HD Button is Download the Best Quality is available so I recommend This Button😁 ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "HD (Recommended) - Need ffmpeg",
                            callback_data="%s and 1" % url
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "HD - Don't Need ffmpeg",
                            callback_data="%s and 2" % url
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "SD (480) Maybe Don't Work",
                            callback_data= "%s and 3" % url
                        ),
                    ]
                ]
            ), disable_web_page_preview=True
        )
    else:
        c.send_message(m.chat.id,"Send The Valid Url Please")


@app.on_callback_query()
def download(c, q): # c Mean Client | q Mean Query
    global check_current
    check_current = 0
    def progress(current, total): #Thanks to my dear friend Hassan Hoot for Progress Bar :)
        global check_current
        if ((current//1024//1024) % 50 )== 0 :
            if check_current != (current//1024//1024):
                check_current = (current//1024//1024)
                upmsg.edit(f"{current//1024//1024}MB of {total//1024//1024}MB Uploaded 😁")
        elif (current//1024//1024) == (total//1024//1024):
            upmsg.delete()
    
    chat_id = q.message.chat.id
    data = q.data
    url, quaitly = data.split(" and ")
    dlmsg = c.send_message(chat_id, 'Hmm!😋 Downloading...')
    path = downloada(url, quaitly)
    upmsg = c.send_message(chat_id, 'Yeah😁 Uploading...')
    dlmsg.delete()
    thumb = path.replace('.mp4',".jpg",-1)
    if  os.path.isfile(thumb):
        thumb = open(thumb,"rb")
        path = open(path, 'rb')
        c.send_photo(chat_id,thumb,caption='Thumbnail of the video Downloaded by @iLoaderBot') #Edit it and add your Bot ID :)
        c.send_video(chat_id, path, caption='Downloaded by @iLoaderBot',
                    file_name="iLoader", supports_streaming=True, progress=progress) #Edit it and add your Bot ID :)
        upmsg.delete()
    else:
        path = open(path, 'rb')
        c.send_video(chat_id, path, caption='Downloaded by @iLoaderBot',
                    file_name="iLoader", supports_streaming=True, progress=progress)
        upmsg.delete()

app.run()
