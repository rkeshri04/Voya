from flask import Flask, render_template, send_from_directory, request, jsonify
import os

app = Flask(__name__)

ASL_IMAGE_MAP = {ch: f"/assets/{ch}.png" for ch in list("abcdefghijklmnopqrstuvwxyz0123456789")}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/<filename>')
def asset(filename):
    return send_from_directory(os.path.join(app.root_path, 'assets'), filename)

@app.route('/api/asl-translate', methods=['POST'])
def asl_translate():
    data = request.get_json()
    text = data.get('text', '').lower()
    mode = data.get('mode', 'individual')
    # Remove non-alphanumeric and split
    text = ''.join([c for c in text if c.isalnum() or c == ' '])
    if mode == 'individual':
        chars = [c for c in text if c.isalnum()]
        result = [{
            'char': c,
            'img': ASL_IMAGE_MAP.get(c)
        } for c in chars]
        return jsonify({'mode': 'individual', 'result': result})
    else:
        words = [w for w in text.split(' ') if w]
        result = []
        for word in words:
            word_imgs = [{
                'char': c,
                'img': ASL_IMAGE_MAP.get(c)
            } for c in word if c.isalnum()]
            result.append({'word': word, 'chars': word_imgs})
        return jsonify({'mode': 'group', 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
