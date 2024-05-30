from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2



def HomePage(request):
    return render(request,'index.html')

def display_csv(request):
        
    return render(request, 'display_csv.html')




class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)


    def get_frame(self):
        success, frame = self.cap.read()
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def LiveVid(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return render(request, 'LiveVid.html')
