from ultralytics import YOLO
import cv2
import os
import time
import main_function
import shutil
import serial

# Change this to match your ESP32 port (e.g., COM3 on Windows, /dev/ttyACM0 on Linux)
SERIAL_PORT = "COM7"
BAUD_RATE = 115200

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

# function to get image from camera
def get_image(image):
    # gets image
    result, img = image.read()

    # shows video from camera
    #cv2.imshow("TestImage", img)

    # gets image and identifies object when space bar is hit
    #if cv2.waitKey(1) & 0xFF == 32:
    key = 1
    if not result:
        print("Error2")  # if getting error switch USB port on computer camera is plugged into

    return(img, key)

def check_num_class(model, image, results):
    num_class = len(results[0].boxes.conf)
    while num_class != 1:
        shutil.rmtree("Testing2")

        # gets image
        result, img = image.read()

        # gets results for image from object detection model
        results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)
        num_class = len(results[0].boxes.conf)
    return results

def get_classification(image, model):
    key = 0
    bin_num = 0
    img, key = get_image(image)
    if key == 1:
        # gets results from model for image
        results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)

        # gets number corresponding to object classification
        path_txt = "Testing2/tests/labels/test.txt"
        results[0].save_txt(path_txt)

        # check if txt file exists, indicating if object is detected if not keep checking until path exists
        while not os.path.exists(path_txt):
            # gets image
            result, img = image.read()

            # gets results for image from object detection model
            results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)
            path_txt = "Testing2/tests/labels/test.txt"
            results[0].save_txt(path_txt)

        results = check_num_class(model, image, results)

        # get number corresponding to object identified and the confidence
        confidence = results[0].boxes.conf
        component_num = int(results[0].boxes[0].cls)

        # checks confidence
        if confidence[0] <= 0.60:
            for i in range(3):
                # gets second image
                key = 0
                img, key = get_image(image)

                # delete Testing2 folder
                shutil.rmtree("Testing2")

                # gets results for second image
                results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)

                # if confidence is still low, classify component as miscellaneous
                if confidence[0] <= 0.60:
                    component_num = 7
                else:
                    component_num = int(results[0].boxes[0].cls)

        shutil.rmtree("Testing2")

        # if resistor identified pass to resistor identification function
        comp_num1 = 0
        comp_num2 = 1
        if component_num == 0:
            while comp_num1 != comp_num2:
                img, key = get_image(image)
                results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)

                results = check_num_class(model, image, results)

                if int(results[0].boxes[0].cls) == 0:
                    path_image_crop = "Testing2/tests/crops/Resistor/image0.jpg"
                    comp_num1 = main_function.fun1(path_image_crop)
                    shutil.rmtree("Testing2")
                else:
                    shutil.rmtree("Testing2")
                    img, key = get_image(image)
                    results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)
                    results = check_num_class(model, image, results)
                    if int(results[0].boxes[0].cls) == 0:
                        path_image_crop = "Testing2/tests/crops/Resistor/image0.jpg"
                        comp_num1 = main_function.fun1(path_image_crop)
                    else:
                        comp_num1 == 7
                        comp_num2 == 7

                # delete Testing2 folder
                if os.path.exists("Testing2"):
                    shutil.rmtree("Testing2")

                img, key = get_image(image)
                results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)
                results = check_num_class(model, image, results)

                if int(results[0].boxes[0].cls) == 0:
                    path_image_crop = "Testing2/tests/crops/Resistor/image0.jpg"
                    comp_num2 = main_function.fun1(path_image_crop)
                else:
                    shutil.rmtree("Testing2")
                    img, key = get_image(image)
                    results = model.predict(img, project='Testing2', name='tests', save=True, save_crop=True)
                    results = check_num_class(model, image, results)

                    if int(results[0].boxes[0].cls) == 0:
                        path_image_crop = "Testing2/tests/crops/Resistor/image0.jpg"
                        comp_num2 = main_function.fun1(path_image_crop)
                    else:
                        comp_num1 == 7
                        comp_num2 == 7

                # delete Testing2 folder
                shutil.rmtree("Testing2")
            component_num = comp_num1
            bin_num = component_num

        print(f"The component is a {component_num} with a confidence of {float(confidence[0]) * 100}%")

        if component_num == 1:
            bin_num = 1
        elif component_num == 2:
            bin_num = 2
        elif component_num == 3 or component_num == 4 or component_num == 5:
            bin_num = 3
        elif component_num == 6:
            bin_num = 4
        elif component_num == 7:
            bin_num = 7
        elif component_num == 14:
            bin_num = 5
        elif component_num == 15:
            bin_num = 6

        # deletes tests folder with cropped image
        if os.path.exists("Testing2"):
            shutil.rmtree("Testing2")

        # breaks loop if 'q' key is hit
        # elif cv2.waitKey(1) & 0xFF == ord("q"):
        #    break

    return(str(bin_num))

def main():
    # load trained YOLO model
    model = YOLO("train4/weights/best.pt")

    # get image from camera
    image = cv2.VideoCapture(0)

    # sets resolution
    #image.set(3, 768)  # lower resolution, used for testing
    #image.set(4, 1024)
    image.set(3, 3840)  # higher resolution, needed for resistor identification, will be used in final design
    image.set(4, 2160)

    # checks if image can be obtained
    if not image.isOpened():
        print("Error1")

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    ser.setDTR(False)
    ser.setRTS(False)

    while True:
        #component_num = get_classification(image, model)

        # print(component_num)
        # time.sleep(5)
        
        try:
            #with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print("Waiting for ESP32 to be ready...")
            wait_for_ready(ser)

            component_num = get_classification(image, model)

            send_data(ser, component_num)
            #wait_for_ready(ser)

            # End signal
            #send_data(ser, "end")
            #print("Finished sending classifications.")

            # deletes tests folder with cropped image
            if os.path.exists("Testing2"):
                shutil.rmtree("Testing2")

            # breaks loop if 'q' key is hit
            #elif cv2.waitKey(1) & 0xFF == ord("q"):
            #    break
            #wait_for_ready(ser)
            time.sleep(12)
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        
    image.release()

if __name__ == "__main__":
    main()