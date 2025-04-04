from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import requests
from io import BytesIO
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/')
def home():
    return "Welcome to the Background Color Suggestion API! Use the /suggest-colors endpoint."

@app.route('/suggest-colors', methods=['POST'])
def suggest_colors():
    data = request.get_json()
    if not data or 'image_url' not in data:
        return jsonify({'error': 'Image URL is required'}), 400

    image_url = data['image_url']

    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((150, 150))  # Resize for faster processing
        pixels = list(img.getdata())

        # Filter out fully transparent pixels (if present)
        if img.mode == "RGBA":
            pixels = [pixel[:3] for pixel in pixels if pixel[3] > 0]

        most_common_colors = Counter(pixels).most_common(5)
        hex_colors = ['#%02x%02x%02x' % color for color, _ in most_common_colors]

        return jsonify({'suggested_colors': hex_colors})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
