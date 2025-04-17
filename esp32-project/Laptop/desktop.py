import serial
import time

# Change this to match your ESP32 port (e.g., COM3 on Windows, /dev/ttyACM0 on Linux)
SERIAL_PORT = "COM3"
BAUD_RATE = 115200

# Data to send (the same classification numbers)
classifications = ["1", "2", "3", "4", "5", "6"]

def wait_for_ready(ser):
    buffer = ""
    start_time = time.time()

    while True:
        if ser.in_waiting > 0:
            byte = ser.read().decode('utf-8', errors='ignore')
            buffer += byte
            if "READY" in buffer:
                elapsed = time.time() - start_time
                print(f"ESP32 is ready (response time: {elapsed:.3f} seconds)")
                return
        else:
            time.sleep(0.05)

def send_data(ser, data):
    message = f"{data}\n"
    ser.write(message.encode('utf-8'))
    print(f"Sent: {data}")

def main():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print("Waiting for ESP32 to be ready...")
            wait_for_ready(ser)

            # Send classification data multiple times
            for _ in range(5):
                for val in classifications:
                    send_data(ser, val)
                    wait_for_ready(ser)

            # End signal
            send_data(ser, "end")
            print("Finished sending classifications.")
    
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()
