#!/usr/bin/python
# servoTest.py

import robohat
#qfrom getkey import getkey, keys

# Define pins for Pan/Tilt
pan = 0
tilt = 1

centre = [15,30]
tVal = centre[0]
pVal = centre[1]

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

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


robohat.init()
#print "Robohat version: ", robohat.version()

def doServos():
    robohat.setServo(pan, pVal)
    robohat.setServo(tilt, tVal)

#print ("Use z-Up, s-Down, q-Left, d-Right Space=Centre, p = Exit:")

doServos()
            
try:
    while True:
        key = input()
#        if len(key)!=1:
#            print('one character svp')
        if key == ' ':
            tVal = centre[0]
            pVal = centre[1]
            doServos()
            #print ("Centre", tVal, pVal)
#        elif key.upper() == 'a':
#            tVal = -90
#            pVal = -90
#            doServos()
#            print ("Left", tVal, pVal)
#        elif key.upper() == 'e':
#            tVal = 90
#            pVal = 90
#            doServos()
#            print ("Right", tVal, pVal)
#        elif key ==' x' or key == '.':
#            initio.stopServos()
#            print ("Stop")

        elif key == 'z' or ord(key) == 16:
            pVal = min(90, pVal+10)
            doServos()
            #print ("Up", pVal)

        elif key == 'q' or ord(key) == 19:
            tVal = max (-70, tVal-10)
            doServos()
            #print ("Left", tVal)

        elif key == 'd' or ord(key) == 18:
            tVal = min(90, tVal+10)
            doServos()
            #print ("Right", tVal)

        elif key == 's' or ord(key) == 17:
            pVal = max(-30, pVal-10)
            doServos()
            #print ("Down", pVal)

#        elif key == 'g':
#            robohat.startServos()
#            print ("Down")
        elif key == 'p':
            break
        #else:
            #print('Unexpected character')

except KeyboardInterrupt:
    print

finally:
    robohat.cleanup()
