# app.py
import os
import secrets
from flask import Flask, render_template, request, flash, redirect, send_from_directory
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])


@app.route("/")
def hello_world():
    return render_template("index.html", title="Remove BG")


@app.route('/', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)

    # Sanitize the file name
    filename = secure_filename(file.filename)

    # Save the uploaded file
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Process the image
    inp = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    out = remove(inp)

    output_filename = 'image_wo_bg.png'  # Define the output filename

    # Save the processed image
    out.save(os.path.join(app.config['OUTPUT_FOLDER'], output_filename))

    return render_template("result.html", output_filename=output_filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


# if __name__ == "__main__":
app.run(host='0.0.0.0', port=81)
