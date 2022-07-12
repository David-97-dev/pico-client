import network
import time
import urequests
from secret import SSID, PASSWORD
import machine
led = machine.Pin("LED", machine.Pin.OUT)
led.off()
led.on()

#wifi setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

def getApiStatus():
    try:
        getResponse = urequests.get("http://192.168.1.234:8080/status")
        print(getResponse.text)
        getResponse.close()
        return True;
    except Exception as e:
        print("[PICO W]" + str(e) + " Check API")
        return False;

def connectWifi():
    #connect to wifi
    print('[PICO W] Connecting to wifi...')
    while wlan.isconnected() == False:
        pass

    print("[PICO W] Connected to " + str(wlan.ifconfig()))
         
TempSensor = machine.ADC(4)
conversion_factor = 3.3 / 65535
connectWifi()

apiStatus = getApiStatus()

if(apiStatus == True):
    print("[PICO W] API Connected")
else:
    print("[PICO W] No connection to API")
        

while wlan.isconnected():
    led.on()
    tempData = TempSensor.read_u16() * conversion_factor 
    temperature = 27-(tempData-0.706)/0.001721
    try:
        postResponse = urequests.post("http://192.168.1.234:8080/", data = str(round(temperature,1)))
        print(postResponse.text)
        postResponse.close()
    except Exception as e:
        while True:
            status = getApiStatus();
            if (status):
                break;
            else:
                led.off()
                time.sleep_ms(1000)
                led.on()
            
        
    time.sleep_ms(1000)
    
    if (wlan.isconnected() == False):
        connectWifi();
        break;
        
    

