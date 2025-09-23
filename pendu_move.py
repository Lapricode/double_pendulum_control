import pyCandle
import time
import math
import sys


# create CANdle object
candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True, pyCandle.USB)

# ping to search for motor drives
motor_ids = candle.ping(pyCandle.CAN_BAUD_1M)  
print(f"Motor ids: {motor_ids}")
if len(motor_ids) == 0: sys.exit("EXIT FAILURE")

# add all found motor drives to the update list
for id in motor_ids:
    candle.addMd80(id)
    
# reset encoders at 0, and set control mode to impedance control
# enable the motor drives
for id in motor_ids:
    candle.controlMd80SetEncoderZero(id)
    candle.controlMd80Mode(id, pyCandle.IMPEDANCE)
    candle.controlMd80Enable(id, True)

t = 0.0
dt = 0.01

# begin auto update loop (it starts in the background)
# it periodically updates the data in candle.md80s vector
candle.begin()

motor1 = candle.md80s[1]
motor2 = candle.md80s[0]
motor1.setImpedanceControllerParams(0.2, 0.02)
motor2.setImpedanceControllerParams(0.2, 0.02)
for i in range(1000):
    motor1.setTargetPosition(math.pi * math.sin(t))
    motor2.setTargetPosition(math.pi * math.sin(t))
    # motor1.setTargetPosition(math.pi)
    # motor2.setTargetPosition(0.0)
    # motor1.setTargetPosition(math.pi)
    # motor2.setTargetPosition(math.pi)
    # motor1.setTargetPosition(0.0)
    # motor2.setTargetPosition(math.pi)
    t += dt
    time.sleep(dt)
    
# close auto update loop
candle.end()

sys.exit("EXIT SUCCESS")
