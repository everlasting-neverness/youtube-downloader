import youtube_dl
import os
import uuid

class Downloader:
    def __init__(self):
        self.file_name = ''
        self.new_dir_uid = ''

    def create_dir_with_uuid(self):
        new_dir_uid = str(uuid.uuid4())
        os.mkdir(os.path.join(os.getcwd(),new_dir_uid))
        return new_dir_uid

    def getConvertedFileName(self, file_name='new_rec'):
        fa = file_name.split('.webm')
        if len(fa) == 1:
            return file_name
        elif len(fa) > 1:
            return fa[0] + '.mp3'

    def download(self, params):
        if params['url'] == '':
            return False

        def get_title_hook(d, file_name=self.file_name):
            if d['status'] == 'finished':
                # global file_name
                self.file_name = self.getConvertedFileName(d['filename'])

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

        self.new_dir_uid = self.create_dir_with_uuid()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '{}/%(title)s.%(ext)s'.format(self.new_dir_uid),
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
                    ydl.download([params['url']])

        print ('Convertation is done')

        output_data = { "file_name": self.file_name, "dir_uid": self.new_dir_uid }

        return output_data
        