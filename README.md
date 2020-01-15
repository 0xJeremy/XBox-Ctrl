# XBox-Ctrl

This library is a lightweight python wrapper for the linux xboxdrv library. To get started, use `sh setup.sh` to install the xboxdrv library, and set the proper permissions.

### Example Usage

```python
import xbox
ctrl = xbox.ctrl()

if ctrl.X():
	print("X Button Pressed")

x_axis = ctrl.leftX()
(x, y) = ctrl.leftStick()
rtrigg = ctrl.rightTrigger()
```

### Interface

```python
ctrl.__init__(refreshRate=30, timeout=2) -> The constructor for the controller. Refreshrate denotes how often the controller refreshes, the timeout refers to initial connection time limit.

.connected() -> Returns True if the controller is connected, False otherwise
.close() -> Closes the processes connected to the controller.

.leftX()           -> returns a scaled value between -1.0 (left), and 1.0 (right)
.leftY()           -> returns a scaled value between -1.0 (down), and 1.0 (up)
.rightX()          -> returns a scaled value between -1.0 (left), and 1.0 (right)
.rightY()          -> returns a scaled value between -1.0 (down), and 1.0 (up)
.dpadUp()          -> return 1 if pressed, 0 if not pressed
.dpadDown()        -> return 1 if pressed, 0 if not pressed
.dpadLeft()        -> return 1 if pressed, 0 if not pressed
.dpadRight()       -> return 1 if pressed, 0 if not pressed
.Back()            -> return 1 if pressed, 0 if not pressed
.Guide()           -> return 1 if pressed, 0 if not pressed
.Start()           -> return 1 if pressed, 0 if not pressed
.leftThumbstick()  -> return 1 if pressed, 0 if not pressed
.rightThumbstick() -> return 1 if pressed, 0 if not pressed
.A()               -> return 1 if pressed, 0 if not pressed
.B()               -> return 1 if pressed, 0 if not pressed
.X()               -> return 1 if pressed, 0 if not pressed
.Y()               -> return 1 if pressed, 0 if not pressed
.leftBumper()      -> return 1 if pressed, 0 if not pressed
.rightBumper()     -> return 1 if pressed, 0 if not pressed
.leftTrigger()     -> return 1 if pressed, 0 if not pressed
.rightTrigger()    -> return 1 if pressed, 0 if not pressed
.leftStick()       -> return 1 if pressed, 0 if not pressed
.rightStick()      -> return 1 if pressed, 0 if not pressed
```
