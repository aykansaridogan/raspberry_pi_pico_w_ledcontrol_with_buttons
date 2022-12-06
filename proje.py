import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket

# Set country to avoid possible errors
rp2.country('TR')

led1 = machine.Pin(15, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)


# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 5
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    for i in range(num_blinks):
        led1.on()
        led2.on()
        time.sleep(1)
        led1.off()
        led2.off()
        time.sleep(1)


wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
mutfak = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
kombi = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)

last_state = False
current_state = False

while True:
    current_state = mutfak.value()
    last_state = kombi.value()
    if last_state == False and current_state == True:
        ifttt_url = 'https://maker.ifttt.com/trigger/{event}/json/with/key/{your key}'
        request = requests.get(ifttt_url)
        print(request.content)
        request.close()
        time.sleep(.01)
        led1.on()
        led2.off()
        last_state = current_state
        
    if current_state == False and last_state == True:
        ifttt_url =  'https://maker.ifttt.com/trigger/{event}/json/with/key/{your key}'
        request = requests.get(ifttt_url)
        print(request.content)
        request.close()
        time.sleep(.01)
        led1.off()
        led2.on()
        last_state = current_state
        
