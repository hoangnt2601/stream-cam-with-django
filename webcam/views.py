from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, StreamingHttpResponse
import cv2
from imutils.video import WebcamVideoStream
from imutils.video import FPS

# Create your views here.
def index(request):
    template = loader.get_template('webcam/index.html')
    return HttpResponse(template.render({}, request))

def stream():
    vs = WebcamVideoStream(src="rtmp://192.168.100.240:1935/b").start()
    fps = FPS().start()

    while True:
        frame = vs.read()

        if frame is None:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')
        fps.update()
    fps.stop()
    vs.stop()
def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
