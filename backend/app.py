from flask import Flask, request, send_file
from flask_cors import CORS
import os
from audio_to_gif import generate_visual_from_audio
import json

app = Flask(__name__)
CORS(app)  # allow React to access this backend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    blur = float(request.form.get("blur", 0.5))
    speed = int(request.form.get("speed", 200))
    pixel_limit = int(request.form.get("pixel_limit", 0))
    tint = request.form.get('tint')
    tint_color = None

    if tint:
        try:
            tint_color = json.loads(tint)  # Expecting [r, g, b]
        except:
            pass

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    output_path = generate_visual_from_audio(filepath, blur=blur, speed=speed, pixel_limit=pixel_limit, tint=tint_color)

    return send_file(output_path, mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True)

