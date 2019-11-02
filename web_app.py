from flask import Flask, render_template, request, redirect, send_file
from downloader import downloader
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    url_to_download = username = request.args.get('url_to_download')
    if url_to_download == '':
        return redirect('/')
    else:
        output_file_name = downloader({ 'url': url_to_download})
        return send_file(os.path.join('Files', output_file_name), attachment_filename=output_file_name)

@app.route('/error_503', methods=['GET'])
def error_503():
    return render_template('error_503.html')


if __name__ == '__main__':
    app.run(debug = True)