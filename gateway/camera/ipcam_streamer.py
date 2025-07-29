import cv2
from flask import Flask, Response, render_template_string
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

app = Flask(__name__)

# 替换为你的摄像头地址和流路径（如有用户名密码，可写为 rtsp://user:pass@192.168.3.27:554/xxx）
RTSP_URL = "rtsp://admin:59In59In@192.168.3.27:554/stream1"

def generate_frames():
    count = 0
    start = time.time()
    cap = cv2.VideoCapture(RTSP_URL)

    if not cap.isOpened():
        raise RuntimeError(f"无法连接到摄像头：{RTSP_URL}")

    while True:
        #for _ in range(5):
        #    cap.grab()
        
        success, frame = cap.read()
        if not success:
            continue
        count += 1
        if time.time() - start >= 1:
            print("fps", count, "fps")
            count = 0
            start = time.time()
        text = "ECU处理图像中，添加静态文本"
        # 将 OpenCV 图像转为 PIL 格式
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 创建绘图对象
        draw = ImageDraw.Draw(img_pil)

        # 加载字体（路径需替换为实际中文字体路径）
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/msyh.ttf", 64)
        # 在图像上绘制中文
        draw.text((30, 60), text , font=font, fill=(0, 255, 0))  # 颜色是 RGB

        # 转回 OpenCV 格式（BGR）
        #frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        frame = cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)

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
                <img src="/video_feed" width="720"> 
            </body>
        </html>
    """)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
