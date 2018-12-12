#!/usr/bin/python
from datetime import datetime
import time
import sys
import Adafruit_DHT
while True:
    # Parse command line parameters.
    #sensor_args = { '11': Adafruit_DHT.DHT11,
    #                '22': Adafruit_DHT.DHT22,
    #                '2302': Adafruit_DHT.AM2302 }
    #if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = Adafruit_DHT.AM2302
    pin = 4
    #else:
    #    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    #    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    #    sys.exit(1)

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


    # Un-comment the line below to convert the temperature to Fahrenheit.
    # temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!

    dt = datetime.now()
    dtTemp = dt.strftime('%d\%b\%Y - %H:%M:%S')
    if humidity is not None and temperature is not None:
        #print (dtTemp)
        text = 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
        humid = '{0:0.1f}%'.format(humidity)
        tempa = '{0:0.1f}*'.format(temperature)

        f = open("/home/pi/Baby_Monitor/demofile.txt", "w")
        f.write(dtTemp)
        f.write("\n")
        f.write(tempa)
        f.write("\n")
        f.write(humid)

	f = open("/home/pi/Baby_Monitor/temperature-stats.txt", "a")
        f.write(dtTemp)
        f.write("\n")
        f.write(tempa)
        f.write("\n")
        f.write(humid)        
    else:
        print('Failed to get reading. Try again!')
        f = open("/home/pi/Baby_Monitor/demofile.txt", "w")
        f.write(dtTemp)
        f.write("\n")
        f.write('Failed to get reading. Try again!')
        
        f = open("/home/pi/Baby_Monitor/temperature-stats.txt", "a")
        f.write(dtTemp)
        f.write("\n")
        f.write('Failed to get reading. Try again!')
        
    time.sleep(5)
        
