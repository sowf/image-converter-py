import io

from flask import Flask
from flask import request, make_response
from PIL import Image


app = Flask(__name__)


def jpeg_to_png(jpg_image_data: bytes) -> bytes:
    jpg_image = Image.open(io.BytesIO(jpg_image_data))
    png_image_data = io.BytesIO()
    jpg_image.save(png_image_data, format='PNG')
    return png_image_data.getvalue()


@app.route("/", methods=['POST'])
def convert_image_api():
    if request.method == 'POST':
        content = request.files['image'].read()
        response = make_response(jpeg_to_png(content))
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='result.png')
        return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
