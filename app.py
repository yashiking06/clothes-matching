from flask import Flask, render_template, redirect, Response
import cv2 as cv
from flask_sqlalchemy import SQLAlchemy
from models.take import take

app = Flask(__name__)

# トップページ


@app.route('/')
def index():
    return render_template('index.html')


# 写真を撮るメソッド
camera = cv.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # フレームデータをjpgに圧縮
            ret, buffer = cv.imencode('.jpg', frame)
            # bytesデータ化
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    # imgタグに埋め込まれるResponseオブジェクトを返す
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/takepicture')
def takepicture():
    return render_template('takepicture.html')


@app.route('/takeface', methods=['POST'])
def takeface():
    take()

    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
