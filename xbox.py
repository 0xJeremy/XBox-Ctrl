import subprocess
import select
import time

DEADZONE = 4000

MAPPING = {
    "leftX":           (3, 9),
    "leftY":           (13, 19),
    "rightX":          (24, 30),
    "rightY":          (34, 40),
    "dpadUp":          (45, 46),
    "dpadDown":        (50, 51),
    "dpadLeft":        (55, 56),
    "dpadRight":       (60, 61),
    "Back":            (68, 69),
    "Guide":           (76, 77),
    "Start":           (84, 85),
    "leftThumbstick":  (90, 91),
    "rightThumbstick": (95, 96),
    "A":               (100, 101),
    "B":               (104, 105),
    "X":               (108, 109),
    "Y":               (112, 113),
    "leftBumper":      (118, 119),
    "rightBumper":     (123, 124),
    "leftTrigger":     (129, 132),
    "rightTrigger":    (136, 139)
}

class ctrl:

    def __init__(self,refreshRate = 30):
        self.proc = subprocess.Popen(['xboxdrv','--no-uinput','--detach-kernel-driver'], stdout=subprocess.PIPE, bufsize=0)
        self.pipe = self.proc.stdout

        self.connectStatus = False  #will be set to True once controller is detected and stays on
        self.reading = '0' * 140    #initialize stick readings to all zeros

        self.refreshTime = 0    #absolute time when next refresh (read results from xboxdrv stdout pipe) is to occur
        self.refreshDelay = 1.0 / refreshRate   #joystick refresh is to be performed 30 times per sec by default

        # Read responses from 'xboxdrv' for upto 2 seconds, looking for controller/receiver to respond
        found = False
        waitTime = time.time() + 2
        while waitTime > time.time() and not found:
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                response = self.pipe.readline()
                # Hard fail if we see this, so force an error
                if response[0:7] == b'No Xbox':
                    raise IOError('No Xbox controller/receiver found')
                # Success if we see the following
                if response[0:12].lower() == b'press ctrl-c':
                    found = True
                # If we see 140 char line, we are seeing valid input
                if len(response) == 140:
                    found = True
                    self.connectStatus = True
                    self.reading = response
        # if the controller wasn't found, then halt
        if not found:
            self.close()
            raise IOError('Unable to detect Xbox controller/receiver - Run python as sudo')

    def refresh(self):
        # Refresh the joystick readings based on regular defined freq
        if self.refreshTime < time.time():
            self.refreshTime = time.time() + self.refreshDelay  #set next refresh time
            # If there is text available to read from xboxdrv, then read it.
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                # Read every line that is availabe.  We only need to decode the last one.
                while readable:
                    response = self.pipe.readline()
                    # A zero length response means controller has been unplugged.
                    if len(response) == 0:
                        raise IOError('Xbox controller disconnected from USB')
                    readable, writeable, exception = select.select([self.pipe],[],[],0)
                # Valid controller response will be 140 chars.  
                if len(response) == 140:
                    self.connectStatus = True
                    self.reading = response
                else:  #Any other response means we have lost wireless or controller battery
                    self.connectStatus = False

    def connected(self):
        self.refresh()
        return self.connectStatus

    # Left stick X axis value scaled between -1.0 (left) and 1.0 (right) with deadzone tolerance correction
    def leftX(self, deadzone=DEADZONE):
        return self.axisScale(self._getValue("leftX"), deadzone)

    # Left stick Y axis value scaled between -1.0 (down) and 1.0 (up)
    def leftY(self, deadzone=DEADZONE):
        return self.axisScale(self._getValue("leftY"), deadzone)

    # Right stick X axis value scaled between -1.0 (left) and 1.0 (right)
    def rightX(self, deadzone=DEADZONE):
        return self.axisScale(self._getValue("rightX"), deadzone)

    # Right stick Y axis value scaled between -1.0 (down) and 1.0 (up)
    def rightY(self, deadzone=DEADZONE):
        return self.axisScale(self._getValue("rightY"), deadzone)

    # Scale raw (-32768 to +32767) axis with deadzone correcion
    # Deadzone is +/- range of values to consider to be center stick (ie. 0.0)
    def axisScale(self, raw, deadzone):
        if abs(raw) < deadzone:
            return 0.0
        else:
            if raw < 0:
                return (raw + deadzone) / (32768.0 - deadzone)
            else:
                return (raw - deadzone) / (32767.0 - deadzone)

    def _getValue(self, key):
        self.refresh()
        (start, end) = MAPPING[key]
        return int(self.reading[start:end])

    # Dpad Up status - returns 1 (pressed) or 0 (not pressed)
    def dpadUp(self):
        return self._getValue("dpadUp")
        
    # Dpad Down status - returns 1 (pressed) or 0 (not pressed)
    def dpadDown(self):
        return self._getValue("dpadDown")
        
    # Dpad Left status - returns 1 (pressed) or 0 (not pressed)
    def dpadLeft(self):
        return self._getValue("dpadLeft")
        
    # Dpad Right status - returns 1 (pressed) or 0 (not pressed)
    def dpadRight(self):
        return self._getValue("dpadRight")
        
    # Back button status - returns 1 (pressed) or 0 (not pressed)
    def Back(self):
        return self._getValue("Back")

    # Guide button status - returns 1 (pressed) or 0 (not pressed)
    def Guide(self):
        return self._getValue("Guide")

    # Start button status - returns 1 (pressed) or 0 (not pressed)
    def Start(self):
        return self._getValue("Start")

    # Left Thumbstick button status - returns 1 (pressed) or 0 (not pressed)
    def leftThumbstick(self):
        return self._getValue("leftThumbstick")

    # Right Thumbstick button status - returns 1 (pressed) or 0 (not pressed)
    def rightThumbstick(self):
        return self._getValue("rightThumbstick")

    # A button status - returns 1 (pressed) or 0 (not pressed)
    def A(self):
        return self._getValue("A")
        
    # B button status - returns 1 (pressed) or 0 (not pressed)
    def B(self):
        return self._getValue("B")

    # X button status - returns 1 (pressed) or 0 (not pressed)
    def X(self):
        return self._getValue("X")

    # Y button status - returns 1 (pressed) or 0 (not pressed)
    def Y(self):
        return self._getValue("Y")

    # Left Bumper button status - returns 1 (pressed) or 0 (not pressed)
    def leftBumper(self):
        return self._getValue("leftBumper")

    # Right Bumper button status - returns 1 (pressed) or 0 (not pressed)
    def rightBumper(self):
        return self._getValue("rightBumper")

    # Left Trigger value scaled between 0.0 to 1.0
    def leftTrigger(self):
        return self._getValue("leftTrigger")
        
    # Right trigger value scaled between 0.0 to 1.0
    def rightTrigger(self):
        return self._getValue("rightTrigger")

    # Returns tuple containing X and Y axis values for Left stick scaled between -1.0 to 1.0
    # Usage:
    #     x,y = joy.leftStick()
    def leftStick(self, deadzone=DEADZONE):
        self.refresh()
        return (self.leftX(deadzone),self.leftY(deadzone))

    # Returns tuple containing X and Y axis values for Right stick scaled between -1.0 to 1.0
    # Usage:
    #     x,y = joy.rightStick() 
    def rightStick(self, deadzone=DEADZONE):
        self.refresh()
        return (self.rightX(deadzone),self.rightY(deadzone))

    # Cleanup by ending the xboxdrv subprocess
    def close(self):
        self.proc.kill()
