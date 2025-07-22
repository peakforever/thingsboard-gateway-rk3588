import cv2
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# 替换为你的摄像头地址和流路径（如有用户名密码，可写为 rtsp://user:pass@192.168.3.27:554/xxx）
RTSP_URL = "rtsp://admin:59In59In@192.168.3.27:554/stream1"

def generate_frames():
    cap = cv2.VideoCapture(RTSP_URL)

    if not cap.isOpened():
        raise RuntimeError(f"无法连接到摄像头：{RTSP_URL}")

    while True:
        success, frame = cap.read()
        if not success:
            continue

        # 编码为 JPEG 格式
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # 按照 MJPEG 流格式推送
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template_string("""
        <html>
            <head><title>IP Camera Stream</title></head>
            <body>
                <h2>实时摄像头图像</h2>
                <img src="/video_feed"> 
            </body>
        </html>
    """)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
