#!/usr/bin/python3
#
from gpiozero import MCP3008, LED, Button, PWMLED, OutputDevice
from time import sleep
import datetime
import urllib
import urllib.request, urllib.error, urllib.parse
#
moisture = MCP3008(channel=0)
msensor = OutputDevice(25, active_high=True, initial_value=False)

out_file = open('moisture_thingspeak.txt','a',buffering=1,)

def sendData(url,key,field1,moisture):
  # Setup data
  values = {'api_key' : key,'field1' : moisture}
  postdata = urllib.parse.urlencode(values).encode("utf-8")
  req = urllib.request.Request(url, postdata)
  # Send data to Thingspeak
  response = urllib.request.urlopen(req, None, 5)
  #print(response.read())
  response.close()


while True:
        msensor.on()
        sleep(1)
        moistadjusted = moisture.value * 1024
        msensor.off()
        moistdecimal = int(moistadjusted)
        sendData('https://api.thingspeak.com/update','xxxxxxxxxxxxxxxx','field1',moistdecimal)
        out_file.write('{:%d-%m-%Y %H:%M:%S} '.format(datetime.datetime.now()))
        moistdecimalstring = str(moistdecimal)
        out_file.write(moistdecimalstring)
        out_file.write('\n')
        sleep(300)
