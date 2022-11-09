import robohat
# Define pins for Pan/Tilt
pan = 0
tilt = 1
tVal = 15
pVal = 30

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    global key
    key=str(message.payload.decode("utf-8"))

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

broker_adresse = "10.3.141.1"
client = mqtt.Client("servo")
client.connect(broker_adresse) #connection au broker MQTT
client.loop_start() #lancement de la boucle
client.subscribe("servomoteur") #connection au topic "servomoteur"

robohat.init()

def doServos():
    robohat.setServo(pan, pVal)
    robohat.setServo(tilt, tVal)

#doServos()
            
while True:
    key=''
    client.on_message=on_message
    if key == 'centre':
        tVal = 15
        pVal = 30
        doServos()
    elif key == 'haut':
        pVal = min(90, pVal+10)
        doServos()
    elif key == 'gauche':
        tVal = max (-70, tVal-10)
        doServos()
    elif key == 'droite':
        tVal = min(90, tVal+10)
        doServos()
    elif key == 'bas':
        pVal = max(-30, pVal-10)
        doServos()
    elif key == 'arrêté':
        break

client.loop_stop()
robohat.cleanup()
