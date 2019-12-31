from flask import Flask, render_template, request, redirect, send_file, make_response, jsonify
from flask import Flask
from flask_cors import CORS, cross_origin
from downloader import downloader
from server_src.error_utils import InvalidUsage
import os

app = Flask(__name__, static_url_path='/static/public', static_folder='static', template_folder='static/public')
cors = CORS(app)

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
            output_file_name = downloader({'url': url_to_download})
            response = make_response(send_file(os.path.join(
                'Files', output_file_name), attachment_filename=output_file_name, as_attachment=True))
            response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response.headers['X-file-name'] = output_file_name
            return response
        except:
            raise InvalidUsage('There was an error processing the request.', status_code=500)


@app.route('/error_503', methods=['GET'])
def error_503():
    return render_template('error_503.html')


if __name__ == '__main__':
    app.run(debug=True, port=4005)
