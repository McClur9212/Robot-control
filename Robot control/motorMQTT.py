import robohat, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    global keyp
    keyp=str(message.payload.decode("utf-8"))

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
client = mqtt.Client("engine")
client.connect(broker_adresse) #connection au broker MQTT
client.loop_start() #lancement de la boucle
client.subscribe("moteur") #connection au topic "servomoteur"

speed = 60

robohat.init()

# main loop

while True:
    keyp=''
    client.on_message=on_message 
    if keyp == 'avant':
        robohat.forward(speed)
    elif keyp == 'arriere':
        robohat.reverse(speed)
    elif keyp == 'droite':
        robohat.spinRight(speed)
    elif keyp == 'gauche':
        robohat.spinLeft(speed)
    elif keyp == 't':
        speed = min(100, speed+10)
    elif keyp == 'g':
        speed = max (0, speed-10)
    elif keyp == 'stop':
        robohat.stop()
    elif keyp == 'arrêté':
        break

client.loop_stop()
robohat.cleanup()
    
