import autopy
import time
import sys

if __name__ == '__main__':
    raw_input("Corner 1")
    x1, y1 = autopy.mouse.get_pos()
    raw_input("Corner 2")
    x2, y2 = autopy.mouse.get_pos()
    while True:
        name = raw_input("Number: ")
        main = autopy.bitmap.capture_screen()
        area = main.get_portion((x1, y1), (x2 - x1, y2 - y1))
        area.save("image/number/" + name + ".png", "png")