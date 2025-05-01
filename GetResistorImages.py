from ultralytics import YOLO
import cv2
import time

# load trained YOLO model
model = YOLO("train4/weights/best.pt")

# get image from camera
image = cv2.VideoCapture(0)

#sets resolution (needed for resistor identification)
#image.set(3, 768)
#image.set(4, 1024)
image.set(3, 3840)
image.set(4, 2160)

# checks if image can be obtained
if not image.isOpened():
    print("Error1")

while True:
    # gets image
    result, img = image.read()

    # shows video from camera
    cv2.imshow("TestImage", img)

    if not result:
        print("Error2") #if getting error switch USB port on computer camera is plugged into
        break

    results = model.predict(img, show=True, project='Testing3', name='tests', save=True, save_crop=True)

    # waits 5 seconds before getting another image
    time.sleep(5)

    # breaks loop if 'q' key is hit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

image.release()