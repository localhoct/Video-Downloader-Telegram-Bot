# -*- coding: utf-8 -*-

import requests
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton

api_id = 1691381
api_hash = "a4b862a161f7a320d5524730bbf51bf2"
app = Client("Downlaoder", api_id, api_hash, bot_token='1597462763:AAErfe3g6-_WL1S1yVNctPN607bVBllxebI')


def downloada(url, quality):
    # print(12345)
    if quality == "1":
        ydl_opts_start = {
            'format': 'best',
            'outtmpl': f'localhoct/%(title)s.%(ext)s',
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True

        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            # print(result)
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
    if quality == "2":
        # print(99999999)
        ydl_opts_start = {
            'format': 'best[height=480]',
            'outtmpl': f'localhoct/%(title)s.%(ext)s',
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


@app.on_message(filters.command('start', '/'))
async def start(c, m):
    await m.reply_text('Hi Welcome To @iLoaderBot \n Just Send Video Url To me and i\'ll try to upload the video and send it to you')


@app.on_message(filters.regex(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"))
async def webpage(c, m):
    url1 = m.text
    sample_url = "https://da.gd/s?url={}".format(url1)
    url = requests.get(sample_url).text
    chat_id = m.chat.id
    # await m.reply_text('you send url \n %s' % url)
    keys = await c.send_message(
        chat_id,  # Edit this
        "Okay!!🙄\n %s is Video Url😊 \n\nPlease Select Quality :\n 💡The HD Key is Download the Best Quality is available so I recommend This Key😁 " % url1,
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "HD (Recommended)",
                        callback_data="%s and 1" % url
                    ),

                ],
                [  # Second row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "SD (480p)",
                        callback_data="%s and 2" % url
                    ),

                ]
            ]
        )
        , disable_web_page_preview=True
    )


@app.on_callback_query()
async def download(c, q):
    chat_id = q.from_user.id
    data = q.data
    url, quaitly = data.split(" and ")
    dlmsg = await c.send_message(chat_id, 'Hmm!😋 Downloading...')
    path = downloada(url, quaitly)
    upmsg = await c.send_message(chat_id, 'Yeah😁 Uploading...')
    await dlmsg.delete()
    vid = await c.send_video(chat_id, path, caption='Downloaded by @iLoaderBot')
    await vid.forward("iLoadeBot",as_copy=True)
    await upmsg.delete()


app.run()
