from flask import Flask, request, jsonify
from services.doc_to_png_cls import ImageConverter

app = Flask(__name__)

@app.route("/<file_name>/", methods=['GET'])
def doc_to_png(file_name):
    return jsonify(ImageConverter(file_name).convert()), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
