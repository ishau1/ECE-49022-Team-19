from machine import Pin, PWM, UART
import time

# Initialize UART1 (Use GPIO16 as RX, GPIO17 as TX)
uart1 = UART(1, baudrate=115200, tx=17, rx=16, timeout=100)

# Define Servo Motor Pins
servo_pins = [2, 4, 5, 12, 14, 15]
servos = []

# Initialize Servo Motors with PWM (50Hz)
for pin in servo_pins:
    pwm = PWM(Pin(pin), freq=50)  # 50Hz PWM frequency
    pwm.duty(77)  # Default duty cycle (neutral position ~90 degrees)
    servos.append(pwm)

# Function to convert angle (0-180) to PWM duty cycle (40-115)
def set_servo_angle(servo, angle):
    duty = int(40 + (angle / 180) * 75)  # Convert angle to duty cycle
    servo.duty(duty)

# Function to process classification and control servos
def move_servos(classification):
    print(f"Moving servos for: {classification}")

    if classification == "Resistor_100Ω":
        set_servo_angle(servos[0], 90)  # Move first servo to 90 degrees
    else:
        set_servo_angle(servos[0], 0)   # Move back to 0 degrees
    
    time.sleep(1)  # Simulate movement time

# Main Loop: Receive Data and Move Servos
while True:
    if uart1.any():  # Check if data is available in UART
        received_data = uart1.readline().decode().strip()  # Read and clean data
        print(f"Received: {received_data}")

        # Move servos based on classification
        move_servos(received_data)

        # Send "READY" signal back to the computer
        uart1.write("READY\n")
