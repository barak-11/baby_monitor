var express = require('express');
var app = express();
var fs = require("fs");
const port = 7000

app.get('/reboot', function (req, res) {
   res.send('rebooting');
   reboot();
});
app.get('/test', function (req, res) {
   res.send('testing worked');
});
app.get('/stats', function (req,res){
   //res.send('getting stats please wait');
   getStats(res);
});
app.listen(port, () => console.log(`Server listening on port ${port}!`))

function reboot(){
console.log('reboot.js is running');
require('child_process').exec('sudo /sbin/shutdown -r now', function (msg) { console.log(msg) });
}

function getStats(res){
try {  
    var data = fs.readFileSync('/home/pi/Baby_Monitor/demofile.txt', 'utf8');
    // console.log(data.toString());
    res.header("Access-Control-Allow-Origin", "*");
    res.send(data.toString());
} catch(e) {
    console.log('Error:', e.stack);
}
}
