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
        self.notice = "\x1b[35m[NOTICE]\x1b[0m"
        self.succes = "\x1b[32m[SUCCES]\x1b[0m"
        self.prompt = "\x1b[34m[PROMPT]\x1b[0m"
        self.fatal  = "\x1b[31m[FATAL]\x1b[0m"

    #
    # Moves the mouse to position x,y.
    # Param: x, y
    #
    def moveMouseAbs(self, x, y):
        # print self.notice + " Moving to (" + str(x) + ", " + str(y) + ")."
        autopy.mouse.move(x, y)
        # print self.succes + " Moved to (" + str(x) + ", " + str(y) + ")."

    #
    # Moves the mouse x and y from current position.
    # Param: x, y, hold mouse, sleep after
    #
    def moveMouseRel(self, xoff, yoff, hold, sleep):
        # print self.notice + " " + str(xoff) + "x and " + str(yoff) + "y."
        x, y = autopy.mouse.get_pos()

        if(hold == True):
            autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
            autopy.mouse.move(x + xoff, y + yoff)
            autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        else:
            autopy.mouse.move(x + xoff, y + yoff)

        # print self.succes + " Moved " + str(xoff) + "x and " + str(yoff) + "y."
        time.sleep(sleep)

    #
    # Tries to find a image on screen
    #
    def findImage(self, imagename, click, offsetx, offsety, sleep):
        print self.notice + " Searching for " + imagename + "..."
        target = autopy.bitmap.Bitmap.open("image/" + imagename, "png")

        while(True):
            screen = autopy.bitmap.capture_screen()
            result = screen.find_bitmap(target, 0.0)
            if not(result == None) :
                print self.succes + " Found " + imagename + ". Moving to target..."
                autopy.mouse.smooth_move(result[0] + offsetx, result[1] + offsety)
                if(click == True):
                    autopy.mouse.click(autopy.mouse.LEFT_BUTTON)
                return
            time.sleep(sleep)

    #
    # Moves the mouse to the defined spinbutton location and clicks.
    #
    def spin(self):
        self.moveMouseAbs(self.spinx, self.spiny)
        time.sleep(0.100)
        autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

    #
    # Returns the color of the pixel at cursor position
    #
    def getColor(self):
        x, y = autopy.mouse.get_pos()
        screen = autopy.bitmap.capture_screen()
        print screen.get_color(x, y)

    #
    # Scans for a color in the workspace.
    #
    def scanColor(self):
        area = autopy.bitmap.capture_screen(self.workspace)
        result = area.find_color(9243915, 0.1)
        if(result != None):
            print self.notice + " Found red"
        else:
            result = area.find_color(1907997, 0.1)
            if(result != None):
                print self.notice + " Found black"
            else:
                print self.notice + " Found green"

    #
    # USELESS ATM
    #
    def scan(self):
        print self.notice + " Scanning for results..."
        area = autopy.bitmap.capture_screen(self.workspace)
        target = autopy.bitmap.Bitmap.open("image/control/black.PNG", "png")
        result = area.find_bitmap(target, 0.3)
        if(result != None):
            autopy.mouse.smooth_move(result[0], result[1])
            print "FOUND BLACK "
        target = autopy.bitmap.Bitmap.open("image/control/red.PNG", "png")
        result = area.find_bitmap(target, 0.3)
        if(result != None):
            print "FOUND RED"

    #
    # Gets the workspace. Prompts the user for input.
    #
    def getWorkspace(self):
        print self.notice + " Setting up workspace..."
        print self.prompt + " Select left upper corner..."
        time.sleep(3)
        x1, y1 = autopy.mouse.get_pos()
        print self.succes + " Left upper corner: (" + str(x1) + ", " + str(y1) + ")."

        print self.prompt + " Select right bottom corner..."
        time.sleep(3)
        x2, y2 = autopy.mouse.get_pos()
        print self.succes + " Right bottom corner: (" + str(x2) + ", " + str(y2) + ")."

        if(x1 >= x2 or y1 >= y2):
            # TODO: restart
            print self.fatal + " Invalid dimensions. Shutting down"
            sys.exit(1)
        else:
            print self.succes + " Using rectangle (" + str(x1) + ", " + str(y1) + ", " + str(x2) + ", " + str(y2) + ")."
            self.workspace = ((x1, y1), (x2 - x1, y2 - y1))

        # print "\x1b[34m[PROMPT]\x1b[0m Select red..."
        # time.sleep(3)
        # self.redx, self.redy = autopy.mouse.get_pos()
        # print "\x1b[32m[SUCCES]\x1b[0m Using point (" + str(self.redx) + ", " + str(self.redy) + ")"

        # print "\x1b[34m[PROMPT]\x1b[0m Select black..."
        # time.sleep(3)
        # self.blackx, self.blacky = autopy.mouse.get_pos()
        # print "\x1b[32m[SUCCES]\x1b[0m Using point (" + str(self.blackx) + ", " + str(self.blacky) + ")"

        print self.prompt + " Select spin..."
        time.sleep(3)
        self.spinx, self.spiny = autopy.mouse.get_pos()
        print self.succes + " Using point (" + str(self.spinx) + ", " + str(self.spiny) + ")"