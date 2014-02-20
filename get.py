import autopy
import time
import sys
import os
try:
    import ctypes
except:
    print "no ctypes"

if __name__ == '__main__':
    # raw_input("Corner 1")
    # x1, y1 = autopy.mouse.get_pos()
    # raw_input("Corner 2")
    # x2, y2 = autopy.mouse.get_pos()
    # while True:
    #     name = raw_input("Number: ")
    #     main = autopy.bitmap.capture_screen()
    #     area = main.get_portion((x1, y1), (x2 - x1, y2 - y1))
    #     area.save("image/number/" + name + ".png", "png")

    print "Select corner of playfield (left corner of 1-18 box)..."
    time.sleep(5)
    fieldx, fieldy = autopy.mouse.get_pos()
    fieldy -= 85
    print " Using point (" + str(fieldx) + ", " + str(fieldy) + ")"

    while True:
        number = raw_input("Number: ")
        number = int(number)

        if number < 25:
            positionx = fieldx + (number + 2 - (3 * ((number - 1)/ 3))) * 22 + (((number - 1) / 3) * (22 + (number * 0.2)))
            offsety = 3 + (3 * ((number - 1)/ 3))
            positiony = fieldy + ((offsety - number) * 23) + (((number - 1) / 3) * (18 - (number * 0.15)))

        else:
            positionx = fieldx + (number + 2 - (3 * ((number - 1)/ 3))) * 22 + (((number - 1) / 3) * (22 + (number * 0.15)))
            offsety = 3 + (3 * ((number - 1)/ 3))
            positiony = fieldy + ((offsety - number) * 23) + (((number - 1) / 3) * (18 - (number * 0.05)))
        ctypes.windll.user32.SetCursorPos(int(round(positionx)), int(round(positiony)))