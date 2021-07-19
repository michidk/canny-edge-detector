from flask import Flask, request, send_file
from canny import CannyEdge

app = Flask(__name__)
canny = CannyEdge()

# just a test route, to verify that the app is running
@app.route("/")
def hello():
    return "Hi! Use /upload to post an image!"

# runs canny edge detection on a .png image
@app.route("/detect", methods = ["POST"])
def detect():
    file = request.files['file']

    image = canny.detect_edges(file)
    image.seek(0)

    return send_file(
        image,
        as_attachment = True,
        attachment_filename = 'output.png',
        mimetype = 'image/png'
        )

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host = "0.0.0.0", debug = True, port = 80)
