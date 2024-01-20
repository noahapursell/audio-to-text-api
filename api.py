from flask import Flask, request, jsonify
import whisper
from werkzeug.utils import secure_filename
import os
from audio_to_text import AudioToText

# Define the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

audio_converter = AudioToText()

# Define the route for audio file upload
@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'audio' not in request.files:
        return 'No audio file part', 400
    file = request.files['audio']
    if file.filename == '':
        return 'No selected file', 400

    filename = secure_filename(file.filename)
    print(f'{filename=}')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    try:
        text = audio_converter.convert_audio_to_text(file_path)
        print(text)
        os.remove(file_path)  # Clean up the uploaded file
        return jsonify({"text": text})
    except Exception as e:
        print('issue')
        return str(e), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=40002)