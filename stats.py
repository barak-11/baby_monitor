import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '10.100.102.30'
PORT_NUMBER = 9999


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        f = open("/home/pi/Baby_Monitor/demofile.txt", "r")
        datetimestr = f.readline()
        temperature=f.readline()
        humidity=f.readline()
        f.close()
        content = '''        
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Baby Stats</title>
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
<h1 class="text-center">Baby Stats</h1>
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
  <div class="row">
    <div class="col"></div>
    <div class="col"></div>
         <!--   <div class="embed-responsive embed-responsive-16by9"> 
  <iframe class="embed-responsive-item" src="http://10.100.102.30:8000" allowfullscreen></iframe>
-->
</div>
    </div>
  
  </div>
      
  </div>
</div>
</body>
</html>
''' %(datetimestr,temperature,humidity)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
