from __future__ import unicode_literals
import youtube_dl
import os
# from sys import argv

def getListDiff(list1, list2):
    return (list(set(list1) - set(list2)))

def getFileNamesInDirectory():
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
    print (files)
    return files

def getFileName(listBefore, listAfter):
    listDiff = getListDiff(listBefore, listAfter)
    if len(listDiff) == 0:
        # need to update logic
        return listAfter[0]
    elif len(listDiff) > 1:
        return listDiff[-1]
    else:
        return ''

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

    print (os.getcwd())
    print ('---current dir')

    print(os.getcwd().endswith('Files'))
    print ('---is for current dir')

    # need to fix change of path
    if os.path.exists('Files'):
        print('path exists and we change dir there')
        os.chdir('Files')
    elif os.getcwd().endswith('Files'):
        print('path exists and we are there')
    elif not os.getcwd().endswith('Files'):
        print ('make new dir because getcwd !endswith(Files)')
        os.makedirs('Files', exist_ok=True)
        os.chdir('Files')
    elif not os.path.exists('Files'):
        print ('make new dir because no path "Files"')
        os.makedirs('Files', exist_ok=True)
        os.chdir('Files')
    else:
        return False

    print ('Starting to convert file...')

    files_before_work = getFileNamesInDirectory()

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # with open('../' + argv[1], 'r') as file:
            # for url in file:
                ydl.download([params['url']])

    print ('Convertation is done')

    files_after_work = getFileNamesInDirectory()

    file_name = getFileName(files_before_work, files_after_work)

    return file_name