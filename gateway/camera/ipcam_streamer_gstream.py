import subprocess
import time
from flask import Flask, Response

app = Flask(__name__)

GST_COMMAND = [
    "gst-launch-1.0",
    "rtspsrc", "location=rtsp://admin:59In59In@192.168.3.27:554/stream1", "latency=100", "protocols=tcp",
    "!", "rtph264depay",
    "!", "parsebin",
    "!", "mppvideodec",  # 替换成你实际设备支持的硬解插件
    "!", "jpegenc",
    "!", "multipartmux", "boundary=frame",
    "!", "filesink", "location=/tmp/mjpeg_pipe"
]

def start_gst():
    # 创建命名管道文件（如果不存在）
    import os
    pipe_path = "/tmp/mjpeg_pipe"
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
    
    # 启动 GStreamer 子进程
    gst_proc = subprocess.Popen(GST_COMMAND)
    return gst_proc

def mjpeg_generator():
    with open('/tmp/mjpeg_pipe', 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            yield data

@app.route('/video_feed')
def video_feed():
    return Response(mjpeg_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''<html><body><h1>RTSP MJPEG Stream</h1><img src="/video_feed" /></body></html>'''

if __name__ == '__main__':
    gst_process = start_gst()
    time.sleep(2)  # 等待GStreamer启动稳定
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        gst_process.terminate()
