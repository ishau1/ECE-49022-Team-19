# This is pretty heavily ChatGPTd just for sake of having a framework

from machine import Pin, PWM, UART
import time

# Initialize UART1 (Use GPIO16 as RX, GPIO17 as TX)
uart1 = UART(1, baudrate=115200, tx=17, rx=16, timeout=100)

# Define Servo Motor Pins
servo_pins = [2, 4, 5, 12, 14, 15]
servos = []

# Initialize Servo Motors with PWM (50Hz)
for pin in servo_pins:
    pwm = PWM(Pin(pin), freq=50) 
    pwm.duty(77)  # Default duty cycle
    servos.append(pwm)

# Function to convert angle (0-180) to PWM duty cycle (40-115)
def set_servo_angle(servo, angle):
    duty = int(40 + (angle / 180) * 75)  # Convert angle to duty cycle
    servo.duty(duty)

def move_servos(classification):
    print(f"Moving servos for: {classification}")

    if classification == "1":
        set_servo_angle(servos[0], 45)
    elif classification == "2":
        set_servo_angle(servos[0], 135)
    elif classification == "3":
        set_servo_angle(servos[0], 135)
    elif classification == "4":
        set_servo_angle(servos[0], 135)
    elif classification == "5":
        set_servo_angle(servos[0], 135)
    elif classification == "6":
        set_servo_angle(servos[0], 135)
    elif classification == "7":
        set_servo_angle(servos[0], 135)
    else:
        print("Unknown classification, defaulting all servos to 0 degrees")
        for servo in servos:
            set_servo_angle(servo, 0)

    time.sleep(1)


while True:
    if uart1.any():  # Check if data is available in UART
        received_data = uart1.readline().decode().strip()
        print(f"Received: {received_data}")

        move_servos(received_data)
        uart1.write("READY\n")
