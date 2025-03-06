import serial
import time

# Initialize USB-UART connection
esp32 = serial.Serial("COM3", 115200, timeout=1)
time.sleep(2)

def classify_component(image_path): # Dummy model
    return "100Ω"

# Function to send classification
def send_classification(image_path):
    classification = classify_component(image_path)


    data = f"{classification}\n"
    esp32.write(data.encode())  # Send data to ESP32
    print(f"Sent: {data}")

    # Wait for ESP32 response
    while True:
        response = esp32.readline().decode().strip()
        if response == "READY":
            print("ESP32 is ready for next classification.")
            break

# Example usage
send_classification("image.jpg")

