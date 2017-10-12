import cv2
from colorDetector import ColorDetector
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--device", required=False, default=0, type=int, help="camera device")
ap.add_argument("-c", "--calibrate", action='store_true', default=False, required=False, help="re-calibrate colors")
args = vars(ap.parse_args())

camera = cv2.VideoCapture(int(args["device"]))
color_detect = ColorDetector("./colors.json")

if bool(args["calibrate"]):
    color_detect.calibrate(camera)
color_detect.load_colors()
cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
while True:
    _, image = camera.read()
    image = cv2.bilateralFilter(image, 9, 75, 75)
    things = color_detect.find_things(image)
    cv2.imshow("camera", image)
    key = cv2.waitKey(1)
    if key == 27:
        break
camera.release()
cv2.destroyAllWindows()