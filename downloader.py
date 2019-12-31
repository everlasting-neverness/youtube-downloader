import youtube_dl
import os
import uuid
# from sys import argv

global file_name
global new_dir_uid
file_name = ''
new_dir_uid = ''

def create_dir_with_uuid():
    new_dir_uid = str(uuid.uuid4())
    os.mkdir(os.path.join(os.getcwd(), new_dir_uid))
    return new_dir_uid

def getConvertedFileName(file_name='new_rec'):
    fa = file_name.split('.webm')
    if len(fa) == 1:
        return file_name
    elif len(fa) > 1:
        return fa[0] + '.mp3'

def downloader(params):
    global file_name
    global new_dir_uid

    if params['url'] == '':
        return False

    def get_title_hook(d):
        if d['status'] == 'finished':
            global file_name
            file_name = getConvertedFileName(d['filename'])

    if os.path.exists('Files'):
        print('path exists and we change dir there')
        os.chdir('Files')
    elif os.getcwd().endswith('Files'):
        print('path exists and we are there')
    elif not os.getcwd().endswith('Files') or not os.path.exists('Files'):
        print ('make new dir')
        os.makedirs('Files', exist_ok=True)
        os.chdir('Files')
    else:
        return False

    print('Creating file dir...')

    new_dir_uid = create_dir_with_uuid()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '{}/%(title)s.%(ext)s'.format(new_dir_uid),
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'progress_hooks': [get_title_hook],
    }
    
    print ('Starting to convert file...')

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # with open('../' + argv[1], 'r') as file:
            # for url in file:
                ydl.download([params['url']])

    print ('Convertation is done')

    output_data = { "file_name": file_name, "dir_uid": new_dir_uid }

    return output_data