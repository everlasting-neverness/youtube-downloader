from flask import Flask, render_template, request, redirect, send_file, make_response, jsonify
from flask_cors import CORS, cross_origin
from downloader import Downloader
from server_src.error_utils import InvalidUsage
import os

app = Flask(__name__, static_url_path='/static/public', static_folder='static', template_folder='static/public')
cors = CORS(app)

def getPureFileName(dir_uid, file_name):
    if not dir_uid in file_name:
        return file_name
    fa = file_name.split('{}/'.format(dir_uid))
    if len(fa) == 1:
        return file_name
    elif len(fa) > 1:
        return fa[1]

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template('index_prod.html')

@cross_origin()
@app.route('/download', methods=['GET'])
def upload_link():
    url_to_download = request.args.get('url_to_download')
    if url_to_download == '':
        return redirect('/')
    else:
        try:
            dwnloader = Downloader()
            output_data = dwnloader.download({'url': url_to_download})
            file_name = getPureFileName(output_data['dir_uid'], output_data['file_name'])
            response = make_response(send_file(os.path.join(
                'Files', output_data['file_name']), attachment_filename=file_name, as_attachment=True))
            response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response.headers['X-file-name'] = file_name
            return response
        except:
            raise InvalidUsage('There was an error processing the request.', status_code=500)


@app.route('/error_503', methods=['GET'])
def error_503():
    return render_template('error_503.html')


if __name__ == '__main__':
    app.run(debug=True, port=4005)
