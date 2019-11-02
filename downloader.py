from __future__ import unicode_literals
import youtube_dl
import os
from sys import argv

def downloader(params):
    
    if params['url'] == '':
        return False

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    if not os.path.exists('Files'):
        os.mkdir('Files')
    else:
        os.chdir('Files')

    print ('Starting to convert file...')

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # with open('../' + argv[1], 'r') as file:
            # for url in file:
                file_name = ydl.prepare_filename(ydl_opts)
                ydl.download([params['url']])

    print ('Convertation is done')

    return file_name