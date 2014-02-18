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
from PIL import ImageGrab
import colorama
colorama.init()

class controller:

    def __init__(self):
        self.notice = "\x1b[35m[NOTICE]\x1b[0m"
        self.succes = "\x1b[32m[SUCCES]\x1b[0m"
        self.prompt = "\x1b[34m[PROMPT]\x1b[0m"
        self.fatal  = "\x1b[31m[FATAL]\x1b[0m"
        self.streak = (1, None) #First: streak number. Second: color
        self.lastcolor = None
        self.betstreak = 1

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
        print self.notice + " Spinning..."
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
        main = autopy.bitmap.capture_screen()
        area = main.get_portion(self.workspace[0], self.workspace[1])
        area.save("area.png", "png")
        result = area.find_color(14688800, 0.1)
        if(result != None):
            print self.notice + " Found red"
            self.lastcolor = "red"
        else:
            result = area.find_color(1907997, 0.1)
            if(result != None):
                print self.notice + " Found black"
                self.lastcolor = "black"
            else:
                print self.notice + " Found green"
                self.lastcolor = "green"

    #
    # Checks if we have a streak. if so: start betting.
    #
    def checkData(self):
        if(self.lastcolor == self.streak[1]):
            self.streak = (self.streak[0] + 1, self.streak[1])
            print self.notice + " " + str(self.streak[0]) + "x " + self.streak[1] + " streak. "
            
            if(self.streak[0] >= 4):
                if(self.streak[1] == "red"):
                    return "black"
                else:
                    return "red"
            else:
                return None
        else:
            if(self.betstreak != 1):
                if(self.lastcolor == "green"):
                    if(self.streak[1] == "red"):
                        return "black"
                    else:
                        return "red"
                else:
                    print self.succes + " WON WITH x " + str(self.betstreak)
                    self.clearBet()
                    self.betstreak = 1
            self.streak = (1, self.lastcolor)
            return None

    #
    # Clicks the desired collor n amount of times
    #
    def bet(self, color):
        if(color == "red"):
            x = self.redx
            y = self.redy
        else:
            x = self.blackx
            y = self.blacky

        print self.notice + " Current betvalue: " + str(self.betstreak)

        self.moveMouseAbs(x, y)
        for i in range(0, self.betstreak):
            time.sleep(0.2)
            autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

        self.betstreak *= 2

    #
    # Clicks the clearbet button
    #
    def clearBet(self):
        print self.notice + "Clearing bet..."
        self.moveMouseAbs(self.clearx, self.cleary)
        time.sleep(5)
        autopy.mouse.click(autopy.mouse.LEFT_BUTTON)
        time.sleep(1)

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

        print self.prompt + " Select red..."
        time.sleep(3)
        self.redx, self.redy = autopy.mouse.get_pos()
        print self.prompt + " Using point (" + str(self.redx) + ", " + str(self.redy) + ")"

        print self.prompt + " Select black..."
        time.sleep(3)
        self.blackx, self.blacky = autopy.mouse.get_pos()
        print self.prompt + " Using point (" + str(self.blackx) + ", " + str(self.blacky) + ")"

        print self.prompt + " Select spin..."
        time.sleep(3)
        self.spinx, self.spiny = autopy.mouse.get_pos()
        print self.succes + " Using point (" + str(self.spinx) + ", " + str(self.spiny) + ")"

        print self.prompt + " Select clear..."
        time.sleep(3)
        self.clearx, self.cleary = autopy.mouse.get_pos()
        print self.succes + " Using point (" + str(self.clearx) + ", " + str(self.cleary) + ")"