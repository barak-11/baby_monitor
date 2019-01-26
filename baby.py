#!/usr/bin/python
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
from datetime import datetime


f = open("/home/pi/Baby_Monitor/demofile.txt", "r")
datetimestr = f.readline()
temperature=f.readline()
humidity=f.readline()
f.close()

PAGEnew ="""\
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Baby Monitor</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="shortcut icon" type="image/png" href="https://gracememorial.net/wp-content/uploads/2016/06/favicon.ico"/>-
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  
  <script>
    $(document).ready(function(){
        setInterval(function(){ location.reload(); }, 60000);
    });

    $(document).ready(function (e) {
    var $worked = $("#worked");

    function update() {
        var myTime = $worked.html();
        var ss = myTime.split(":");
        var dt = new Date();
        dt.setHours(0);
        dt.setMinutes(ss[0]);
        dt.setSeconds(ss[1]);
        
        var dt2 = new Date(dt.valueOf() + 1000);
        var temp = dt2.toTimeString().split(" ");
        var ts = temp[0].split(":");
        
        $worked.html(ts[1]+":"+ts[2]);
        setTimeout(update, 1000);
    }

    setTimeout(update, 1000);
});
  </script>
</head>
<body>

<div class="container">
<h1 class="text-center">Yair Schieber</h1>
  <div class="row text-center">
     <div class="col-sm-4">
      <h3>Time</h3>
      <p>%s</p>
    </div>
    <div class="col-sm-4">
      <h3>Temperature</h3>
      <p>%s</p>
    </div>
    <div class="col-sm-4">
      <h3>Humidity</h3>
      <p>%s</p>
    </div>
  </div>
    <div class="row text-center">
      <div class="col-sm-12">
          <div id="worked">00:00</div>
            <img src="stream.mjpeg" class="img-responsive" alt="sumsum"  width="640" height="480">
      </div>
  </div>
</div>

</body>
</html>

""" %(datetimestr,temperature,humidity)


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
        
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGEnew.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)         
        elif self.path == '/stream.mjpeg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:

                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
try:
    with picamera.PiCamera(resolution='1080x720', framerate=64) as camera:
        output = StreamingOutput()
                
        dt=datetime.now()
        dtTemp = dt.strftime('%Y-%m-%d - %H-%M-%S')
        filename = '/home/pi/baby_lapse/%s.jpg' % dtTemp
        #camera.rotation = 180
        camera.capture(filename, resize=(640, 480))
            #camera.resolution=(1080,720)
        camera.start_recording(output, format='mjpeg')
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
finally:
    print('test')
