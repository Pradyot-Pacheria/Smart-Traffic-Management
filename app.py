from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import shutil
import moviepy.editor as moviepy


app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

VIDEO_PATH = " "
@app.route("/")
def hello_world():
    return render_template('index.html')



@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    VIDEO_PATH = os.path.join(uploads_dir, secure_filename(video.filename))
    video.save(VIDEO_PATH)
    with open("vp.txt", "w") as fp:
        fp.write(f"{VIDEO_PATH}[*]{video.filename}")
    print(video)
    subprocess.run("ls",shell=True)
    subprocess.run(['python', 'detect.py', '--source', VIDEO_PATH],shell=True)

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    obj = secure_filename(video.filename)
    src_path = os.path.join('results',secure_filename(video.filename))
    print(f"source path is {src_path}")
    dst_path = os.path.join('static',secure_filename(video.filename))
    shutil.copy(src_path,dst_path)
    return obj

@app.route("/op")
def op():
    vp = ''
    with open("vp.txt", 'r') as fp:
        vp = fp.read()
    _, name = vp.split("[*]")
    return render_template('videos.html', parameter=[f"../static/{name}.mp4",f'../static/{name}'])

# xyz.mp4
# xyz.mp4.mp4

@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    print(obj)
#    loc = os.path.join("runs/detect", obj)
    loc = os.path.join("results", obj)
    print(loc)
    try:
        return send_file(os.path.join("results", obj), attachment_filename=obj)
        # return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)

# @app.route('/display/<filename>')
# def display_video(filename):
# 	#print('display_video filename: ' + filename)
# 	return redirect(url_for('static/video_1.mp4', code=200))

if __name__ == "__main__":
    port = 8080
    app.run(host='0.0.0.0', port=port)