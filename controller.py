#
# FILE: controler.py
#
# DESCRIPTION:
#
# AUTHOR: Tristan van Vaalen
#

import autopy
import time
import sys

class controller:

    def __init__(self):
        pass

    #
    # Moves the mouse to position x,y.
    # Param: x, y
    #
    def moveMouseAbs(self, x, y):
        print "\x1b[35m[NOTICE]\x1b[0m Moving to (" + str(x) + ", " + str(y) + ")."
        autopy.mouse.move(x, y)
        print "\x1b[32m[SUCCES]\x1b[0m Moved to (" + str(x) + ", " + str(y) + ")."

    #
    # Moves the mouse x and y from current position.
    # Param: x, y, hold mouse, sleep after
    #
    def moveMouseRel(self, xoff, yoff, hold, sleep):
        print "\x1b[35m[NOTICE]\x1b[0m Moving " + str(xoff) + "x and " + str(yoff) + "y."
        x, y = autopy.mouse.get_pos()

        if(hold == True):
            autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
            autopy.mouse.move(x + xoff, y + yoff)
            autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        else:
            autopy.mouse.move(x + xoff, y + yoff)

        print "\x1b[32m[SUCCES]\x1b[0m Moved " + str(xoff) + "x and " + str(yoff) + "y."
        time.sleep(sleep)

    #
    # ...
    #
    def findImage(self, imagename, click, offsetx, offsety, sleep):
        print "\x1b[35m[NOTICE]\x1b[0m Searching for " + imagename + "..."
        target = autopy.bitmap.Bitmap.open("image/" + imagename, "png")

        while(True):
            screen = autopy.bitmap.capture_screen()
            result = screen.find_bitmap(target, 0.0)
            if not(result == None) :
                print "\x1b[32m[SUCCES]\x1b[0m Found " + imagename + ". Moving to target..."
                autopy.mouse.smooth_move(result[0] + offsetx, result[1] + offsety)
                if(click == True):
                    autopy.mouse.click(autopy.mouse.LEFT_BUTTON)
                return
            time.sleep(sleep)

    #
    # ...
    #
    def getWorkspace(self):
        print "\x1b[35m[NOTICE]\x1b[0m Setting up workspace..."
        print "\x1b[34m[PROMPT]\x1b[0m Select left upper corner..."
        time.sleep(3)
        x1, y1 = autopy.mouse.get_pos()
        print "\x1b[32m[SUCCES]\x1b[0m Left upper corner: (" + str(x1) + ", " + str(y1) + ")."

        print "\x1b[34m[PROMPT]\x1b[0m Select right bottom corner..."
        time.sleep(3)
        x2, y2 = autopy.mouse.get_pos()
        print "\x1b[32m[SUCCES]\x1b[0m Right bottom corner: (" + str(x2) + ", " + str(y2) + ")."

        if(x1 >= x2 or y1 >= y2 or x2 - x1 < 100 or y2 - y1 < 100):
            # TODO: restart
            print "\x1b[31m[FATAL]\x1b[0m Invalid dimensions. Needs at least 100*100px rectangle. Shutting down"
            sys.exit(1)
        else:
            print "\x1b[32m[SUCCES]\x1b[0m Using rectangle (" + str(x1) + ", " + str(y1) + ", " + str(x2) + ", " + str(y2) + ")."
            self.workspace = (x1, y1, x2, y2)

