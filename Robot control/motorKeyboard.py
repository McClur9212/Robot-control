# Initio Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python motorTest2.py


import robohat, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios
from getkey import getkey, keys


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

speed = 20

print ("Tests the motors by using the arrow keys to control")
print ("Use , or < to slow down")
print ("Use . or > to speed up")
print ("Speed changes take effect when the next arrow key is pressed")
print ("Press Ctrl-C to end")
print

robohat.init()

# main loop
try:
    while True:
        keyp = getkey()
        if keyp == 'z' or ord(keyp) == 16:
            robohat.forward(speed)
            print ('Forward', speed)
        elif keyp == 's' or ord(keyp) == 17:
            robohat.reverse(speed)
            print ('Reverse', speed)
        elif keyp == 'd' or ord(keyp) == 18:
            robohat.spinRight(speed)
            print ('Spin Right', speed)
        elif keyp == 'q' or ord(keyp) == 19:
            robohat.spinLeft(speed)
            print ('Spin Left', speed)
        elif keyp == 't' or keyp == '>':
            speed = min(100, speed+10)
            print ('Speed+', speed)
        elif keyp == 'g' or keyp == '<':
            speed = max (0, speed-10)
            print ('Speed-', speed)
        elif keyp == ' ':
            robohat.stop()
            print ('Stop')
        elif keyp == 'p' or ord(keyp) == 3:
            break

except KeyboardInterrupt:
    print

finally:
    robohat.cleanup()
    
