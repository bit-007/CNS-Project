from flask import Flask, request, render_template, flash, redirect
import os
import binascii
import sys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

# Function to display warning message
def unsafe():
    return "Warning!!! This Gif is not safe."

# Function to skip the extension blocks
def extension(idx, hexc):
    idx = idx + 2  # Skip 21h
    while True:
        if hexc[idx:idx + 2] == 'f9':  # Graphics controller extension
            idx = idx + 14  # Skip the rest of the extension block

        if hexc[idx:idx + 2] == '01':  # Plain Text extension
            s = int(hexc[idx + 2:idx + 4], 16)  # Calculate the number of bytes to skip
            idx = idx + 2
            idx = idx + (s * 2)  # Skip the rest of the extension. After this, there will be an image data block.
            return idx

        if hexc[idx:idx + 2] == 'ff':  # Application extension
            s = int(hexc[idx + 2:idx + 4], 16)  # Calculate the number of bytes to skip
            idx = idx + 2
            idx = idx + (s * 2)  # Skip the rest of the extension. After this, there will be an image data block.
            return idx

        if hexc[idx:idx + 2] == 'fe':  # Comment extension
            idx = idx + 2
            return idx  # After this, there will be an image data block.

        if hexc[idx:idx + 2] == '2c':  # Image separator
            packed = hexc[idx + 18:idx + 20]  # Packed field
            packed = "{0:08b}".format(int(packed, 16))
            LCT = 0  # Number of Local colour table entries

            if (packed[7] == '1'):  # If Local colour table exists
                N = int(packed[0:3], 2)
                N = N + 1
                LCT = pow(2, N)  # Calculate number of Local colour table entries

            idx = idx + 20  # Skip Image descriptor
            idx = idx + (3 * LCT)  # Skip local colour table
            idx = idx + 2  # Skip LZW minimum code size
            return idx

# Function to check the safety of the GIF
def check_gif_safety(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
    except IOError:
        return "File not found!"

    hexc = binascii.hexlify(content).decode("utf-8")

    if hexc[0:4] != '4749':  # Check file type
        return "The file is not a GIF."

    if hexc[8:12] != '3961':  # Check GIF file version
        return "The file is not an 89a GIF."

    packed = hexc[20:22]  # Packed field of the Logical Screen Descriptor
    packed = "{0:08b}".format(int(packed, 16))
    GCT = 0  # Number of Global colour table entries

    if packed[0] == '1':  # If Global colour table exists
        N = int(packed[5:8], 2)
        N = N + 1
        GCT = pow(2, N)  # Calculate number of Global colour table entries

    skip = (6 * 2) + (7 * 2) + (3 * GCT)  # Skip header, logical screen descriptor and global colour table
    idx = skip

    while True:
        if hexc[idx:idx + 2] == '2c':  # Image separator
            packed = hexc[idx + 18:idx + 20]  # Packed field
            packed = "{0:08b}".format(int(packed, 16))
            LCT = 0  # Number of Local colour table entries

            if packed[7] == '1':  # If Local colour table exists
                N = int(packed[0:3], 2)
                N = N + 1
                LCT = pow(2, N)  # Calculate number of Local colour table entries

            idx = idx + 20  # Skip Image descriptor
            idx = idx + (3 * LCT)  # Skip local colour table
            idx = idx + 2  # Skip LZW minimum code size

        if hexc[idx:idx + 2] == '3b':  # Trailer
            break

        elif hexc[idx:idx + 2] == '21':  # Extension block
            idx = extension(idx, hexc)  # Skip extension blocks

        else:  # Image data blocks
            while hexc[idx:idx + 2] != '00':  # While block size not equal to zero
                s = int(hexc[idx:idx + 2], 16)  # Number of bytes to skip
                idx = idx + 2
                idx = idx + (s * 2)
            idx = idx + 2

    if len(hexc) != idx + 2:  # If there exists some data after the trailer 0x3b
        return unsafe()
    else:
        return "Congratulations!! This GIF is safe to use"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'gif_file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['gif_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            message = check_gif_safety(filepath)
            return render_template('result.html', message=message)
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
