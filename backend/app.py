from flask import Flask, request, send_file
from flask_cors import CORS
import os
from audio_to_gif import generate_visual_from_audio

app = Flask(__name__)
CORS(app)  # allow React to access this backend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    output_path = generate_visual_from_audio(filepath)
    return send_file(output_path, mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True)
