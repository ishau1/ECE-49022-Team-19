from ultralytics import YOLO
import cv2
import os
import time
import ResistorType
import shutil

# function to get image from camera
def get_image(image, key):
    # gets image
    result, img = image.read()

    # shows video from camera
    cv2.imshow("TestImage", img)

    # gets image and identifies object when space bar is hit
    if cv2.waitKey(1) & 0xFF == 32:
        key = 1
        if not result:
            print("Error2")  # if getting error switch USB port on computer camera is plugged into

    return(img, key)

# function to get name of component from number classification
def num_to_name(component_num):
    if component_num == 0:
        comp_type = "resistor"
    elif component_num == 1:
        comp_type = "IC"
    elif component_num == 2:
        comp_type = "LED"
    elif component_num == 3:
        comp_type = "Capacitor_G"
    elif component_num == 4:
        comp_type = "Capacitor_Y"
    elif component_num == 5:
        comp_type = "Capacitor_B"
    elif component_num == 6:
        comp_type = "Transistor"
    elif component_num == 7:
        comp_type = "Miscellaneous"
    return(comp_type)

# load trained YOLO model
model = YOLO("runs/detect/train2/weights/best.pt")

# get image from camera
image = cv2.VideoCapture(0)

# sets resolution
image.set(3, 768)  # lower resolution, used for testing
image.set(4, 1024)
#image.set(3, 3840)  # higher resolution, needed for resistor identification, will be used in final design
#image.set(4, 2160)

# checks if image can be obtained
if not image.isOpened():
    print("Error1")

while True:
    key = 0
    img, key = get_image(image, key)
    if key == 1:
        # gets results from model for image
        results = model.predict(img, show=True, project='Testing2', name='tests', save=True, save_crop=True)

        # gets number corresponding to object classification
        path_txt = "Testing2/tests/labels/test.txt"
        results[0].save_txt(path_txt)

        # check if txt file exists, indicating if object is detected if not keep checking until path exists
        while not os.path.exists(path_txt):
            # gets image
            result, img = image.read()
            # gets results for image from object detection model
            results = model.predict(img, show=True, project='Testing2', name='tests', save=True, save_crop=True)
            path_txt = "Testing2/tests/labels/test.txt"
            results[0].save_txt(path_txt)

        # get number corresponding to object identified and the confidence
        confidence = results[0].boxes.conf
        component_num = int(results[0].boxes[0].cls)

        # checks confidence
        if confidence[0] <= 0.60:
            for i in range(2):
                # gets second image
                key = 0
                img, key = get_image(image, key)

                # gets results for second image
                results = model.predict(img, show=True, project='Testing2', name='tests', save=True, save_crop=True)
                # if confidence is still low, classify component as miscellaneous
                if confidence[0] <= 0.60:
                    component_num = 7
                else:
                    component_num = int(results[0].boxes[0].cls)

        # gets name of component based on number classification
        comp_type = num_to_name(component_num)

        # if resistor identified pass to resistor identification function
        if component_num == 0:
            path_image_crop = "Testing2/tests/crops/Resistor/image0.jpg"
            component_num = ResistorType.ResistorIdentification(path_image_crop)

        print(f"The component is a {comp_type} with a confidence of {float(confidence[0])*100}%")

        # deletes tests folder with cropped image
        shutil.rmtree("Testing2/tests")

        # waits 5 seconds before getting another image
        #time.sleep(5)

    # breaks loop if 'q' key is hit
    elif cv2.waitKey(1) & 0xFF == ord("q"):
        break

image.release()