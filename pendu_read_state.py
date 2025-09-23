import pyCandle
import time
import sys


# create CANdle object
candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True, pyCandle.USB)

# ping to search for motor drives
motor_ids = candle.ping(pyCandle.CAN_BAUD_1M)
print(f"Motor ids: {motor_ids}")
if len(motor_ids) == 0: sys.exit("EXIT FAILURE")

# blink all motor drives
for id in motor_ids:
    candle.configMd80Blink(id)

# add all found motor drives to the update list
for id in motor_ids:
    candle.addMd80(id)

# print all motor drives objects
print(f"Motor drives objects: {candle.md80s}")

# reset encoders at 0, and enable the motor drives
for id in motor_ids:
    candle.controlMd80SetEncoderZero(id)
    candle.controlMd80Enable(id, True)

# begin auto update loop (it starts in the background)
# it periodically updates the data in candle.md80s vector
candle.begin()

# read positions and velocities of the two motor drives
motor1 = candle.md80s[1]
motor2 = candle.md80s[0]
for i in range(1000):
    print(f"Drive id: {str(motor1.getId())}")
    print(f"    Position: {str(motor1.getPosition())}")
    print(f"    Velocity: {str(motor1.getVelocity())}")
    print(f"Drive id: {str(motor2.getId())}")
    print(f"    Position: {str(motor2.getPosition())}")
    print(f"    Velocity: {str(motor2.getVelocity())}")
    time.sleep(0.1)
    
# close auto update loop
candle.end()

sys.exit("EXIT SUCCESS")
