import time
import robohat


robohat.init()


try:
    dist = robohat.getDistance()
    print(int(dist))    

except KeyboardInterrupt:
    print
    pass

finally:
    robohat.cleanup()
    
