import can

bus = can.Bus(channel="slcan0", interface="socketcan", receive_own_messages=True)

msg = can.Message(arbitration_id=0x001, data=[0x11,0x22,0x33,0x44], is_extended_id=False)
bus.send(msg)

print("Message sent on", bus.channel_info)

try:
    while True:
        msg = bus.recv(timeout=1.0)
        if msg:
            print(f"ID={hex(msg.arbitration_id)} Data={list(msg.data)}")
except KeyboardInterrupt:
    bus.shutdown()


# import pyCandle
# import sys
# import time

# # Set your device path here
# USB_DEVICE = "/dev/ttyACM3"  # change if needed

# # Create CANdle object
# try:
#     candle = pyCandle.Candle(
#         pyCandle.CAN_BAUD_1M,   # 1 Mbps baud rate
#         True,                   # debug mode
#         pyCandle.USB,           # USB bus type
#         USB_DEVICE              # USB device path
#     )
# except Exception as e:
#     print(f"Failed to initialize CANdle: {e}")
#     sys.exit(1)

# print("[CANDLE] Initialized successfully.")

# # Ping the bus to find all motors
# try:
#     motor_ids = candle.ping()
# except Exception as e:
#     print(f"Ping failed: {e}")
#     candle.end()
#     sys.exit(1)

# if not motor_ids:
#     print("No motors found.")
#     candle.end()
#     sys.exit(0)

# print(f"Found motors: {motor_ids}")

# # Blink LEDs on each motor to verify communication
# for motor_id in motor_ids:
#     print(f"Blinking motor ID {motor_id} LED...")
#     candle.configMd80Blink(motor_id)
#     time.sleep(0.5)  # small delay between blinks

# print("Finished blinking LEDs.")

# # Clean up
# candle.end()
# print("CANdle session closed.")


# import can
# import time
# from collections import defaultdict

# # Open CAN bus
# bus = can.Bus(channel="slcan0", interface="socketcan")

# # Dictionary to store observed motor IDs and their last messages
# motor_data = defaultdict(list)

# print("Listening for motor messages on slcan0... (Ctrl+C to stop)")

# try:
#     while True:
#         msg = bus.recv(timeout=1.0)
#         if msg:
#             motor_id = msg.arbitration_id
#             data_bytes = list(msg.data)

#             # Store latest message per motor
#             motor_data[motor_id].append(data_bytes)
#             if len(motor_data[motor_id]) > 10:
#                 motor_data[motor_id].pop(0)  # keep last 10 messages

#             # Print received data
#             print(f"Motor ID 0x{motor_id:X}: Data {data_bytes}")

#         # Optional: every 5 seconds, print summary of detected motors
#         if int(time.time()) % 5 == 0:
#             if motor_data:
#                 detected = ', '.join(f"0x{mid:X}" for mid in motor_data.keys())
#                 print(f"Detected motor IDs: {detected}")

# except KeyboardInterrupt:
#     print("\nStopped listening.")

# finally:
#     bus.shutdown()
#     print("CAN bus shut down.")
