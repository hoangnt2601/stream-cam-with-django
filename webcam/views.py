from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('webcam/index.html')
    return HttpResponse(template.render({}, request))

def stream():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
