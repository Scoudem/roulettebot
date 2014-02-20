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
import colorama
colorama.init()

class controller:

    def __init__(self, risk, p):
        self.risk = risk
        self.p = p

        self.notice = "\x1b[35m[NOTICE]\x1b[0m"
        self.succes = "\x1b[32m[SUCCES]\x1b[0m"
        self.prompt = "\x1b[34m[PROMPT]\x1b[0m"
        self.fatal  = "\x1b[31m[FATAL]\x1b[0m"
        self.streak = (1, None) #First: streak number. Second: color
        self.lastcolor = None
        self.betstreak = 1

        self.numbers = {}
        for i in range(0,37):
            self.numbers[i] = autopy.bitmap.Bitmap.open("image/number/" + str(i) + ".png", "png")

    #
    # Moves the mouse to position x,y.
    # Param: x, y
    #
    def moveMouseAbs(self, x, y):
        # if(self.p): print self.notice + " Moving to (" + str(x) + ", " + str(y) + ")."
        autopy.mouse.move(x, y)
        # if(self.p): print self.succes + " Moved to (" + str(x) + ", " + str(y) + ")."

    #
    # Moves the mouse x and y from current position.
    # Param: x, y, hold mouse, sleep after
    #
    def moveMouseRel(self, xoff, yoff, hold, sleep):
        # if(self.p): print self.notice + " " + str(xoff) + "x and " + str(yoff) + "y."
        x, y = autopy.mouse.get_pos()

        if(hold == True):
            autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
            autopy.mouse.move(x + xoff, y + yoff)
            autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        else:
            autopy.mouse.move(x + xoff, y + yoff)

        # if(self.p): print self.succes + " Moved " + str(xoff) + "x and " + str(yoff) + "y."
        time.sleep(sleep)

    #
    # Tries to find a image on screen
    #
    def findImage(self, imagename, click, offsetx, offsety, sleep):
        if(self.p): print self.notice + " Searching for " + imagename + "..."
        target = autopy.bitmap.Bitmap.open("image/" + imagename, "png")

        while(True):
            screen = autopy.bitmap.capture_screen()
            result = screen.find_bitmap(target, 0.0)
            if not(result == None) :
                if(self.p): print self.succes + " Found " + imagename + ". Moving to target..."
                autopy.mouse.smooth_move(result[0] + offsetx, result[1] + offsety)
                if(click == True):
                    autopy.mouse.click(autopy.mouse.LEFT_BUTTON)
                return
            time.sleep(sleep)

    #
    # Moves the mouse to the defined spinbutton location and clicks.
    #
    def spin(self):
        if(self.p): print self.notice + " Spinning..."
        self.moveMouseAbs(self.spinx, self.spiny)
        time.sleep(0.100)
        autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

    #
    # Returns the color of the pixel at cursor position
    #
    def getColor(self):
        x, y = autopy.mouse.get_pos()
        screen = autopy.bitmap.capture_screen()
        if(self.p): print screen.get_color(x, y)

    #
    # Scans for a color in the workspace.
    #
    def scanColor(self):
        main = autopy.bitmap.capture_screen()
        area = main.get_portion(self.workspace[0], self.workspace[1])
        area.save("area.png", "png")
        result = area.find_color(14688800, 0.1)
        if(result != None):
            if(self.p): print self.notice + " Found red"
            self.lastcolor = "red"
        else:
            result = area.find_color(1907997, 0.1)
            if(result != None):
                if(self.p): print self.notice + " Found black"
                self.lastcolor = "black"
            else:
                if(self.p): print self.notice + " Found green"
                self.lastcolor = "green"

    def scanNumber(self):
        main = autopy.bitmap.capture_screen()
        area = main.get_portion(self.workspaceNumber[0], self.workspaceNumber[1])
        for i in range(0, 37):
            result = area.find_bitmap(self.numbers[i])
            if result != None:
                if(self.p): print self.notice + " Found " + str(i)
                break;

    #
    # Checks if we have a streak. if so: start betting.
    #
    def checkData(self):
        if(self.lastcolor == self.streak[1]):
            self.streak = (self.streak[0] + 1, self.streak[1])
            if(self.p): print self.notice + " " + str(self.streak[0]) + "x " + self.streak[1] + " streak. "
            
            if(self.streak[0] >= self.risk):
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
                    if(self.p): print self.succes + " WON WITH x " + str(self.betstreak)
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

        if(self.p): print self.notice + " Current betvalue: " + str(self.betstreak)

        self.moveMouseAbs(x, y)
        for i in range(0, self.betstreak):
            time.sleep(0.2)
            autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

        self.betstreak *= 2

    #
    # Clicks the clearbet button
    #
    def clearBet(self):
        if(self.p): print self.notice + "Clearing bet..."
        self.moveMouseAbs(self.clearx, self.cleary)
        time.sleep(5)
        autopy.mouse.click(autopy.mouse.LEFT_BUTTON)
        time.sleep(1)

    #
    # Gets the workspace. Prompts the user for input.
    #
    def getWorkspace(self):
        if(self.p): print self.notice + " Setting up workspace..."
        if(self.p): print self.prompt + " Select left upper corner for NUMBER..."
        time.sleep(3)
        nx1, ny1 = autopy.mouse.get_pos()
        if(self.p): print self.succes + " Left upper corner: (" + str(nx1) + ", " + str(ny1) + ")."

        if(self.p): print self.prompt + " Select right bottom corner for NUMBER..."
        time.sleep(3)
        nx2, ny2 = autopy.mouse.get_pos()
        if(self.p): print self.succes + " Right bottom corner: (" + str(nx2) + ", " + str(ny2) + ")."

        if(self.p): print self.prompt + " Select left upper corner for COLOR..."
        time.sleep(3)
        cx1, cy1 = autopy.mouse.get_pos()
        if(self.p): print self.succes + " Left upper corner: (" + str(cx1) + ", " + str(cy1) + ")."

        if(self.p): print self.prompt + " Select right bottom corner for COLOR..."
        time.sleep(3)
        cx2, cy2 = autopy.mouse.get_pos()
        if(self.p): print self.succes + " Right bottom corner: (" + str(cx2) + ", " + str(cy2) + ")."

        if(nx1 >= nx2 or ny1 >= ny2):
            # TODO: restart
            if(self.p): print self.fatal + " Invalid dimensions. Shutting down"
            sys.exit(1)
        else:
            if(self.p): print self.succes + " Using rectangle (" + str(nx1) + ", " + str(ny1) + ", " + str(nx2) + ", " + str(ny2) + ")."
            self.workspaceNumber = ((nx1, ny1), (nx2 - nx1, ny2 - ny1))

        if(cx1 >= cx2 or cy1 >= cy2):
            # TODO: restart
            if(self.p): print self.fatal + " Invalid dimensions. Shutting down"
            sys.exit(1)
        else:
            if(self.p): print self.succes + " Using rectangle (" + str(cx1) + ", " + str(cy1) + ", " + str(cx2) + ", " + str(cy2) + ")."
            self.workspace = ((cx1, cy1), (cx2 - cx1, cy2 - cy1))

        if(self.p): print self.prompt + " Select red..."
        time.sleep(3)
        self.redx, self.redy = autopy.mouse.get_pos()
        if(self.p): print self.prompt + " Using point (" + str(self.redx) + ", " + str(self.redy) + ")"

        if(self.p): print self.prompt + " Select black..."
        time.sleep(3)
        self.blackx, self.blacky = autopy.mouse.get_pos()
        if(self.p): print self.prompt + " Using point (" + str(self.blackx) + ", " + str(self.blacky) + ")"

        if(self.p): print self.prompt + " Select spin..."
        time.sleep(3)
        self.spinx, self.spiny = autopy.mouse.get_pos()
        if(self.p): print self.succes + " Using point (" + str(self.spinx) + ", " + str(self.spiny) + ")"

        if(self.p): print self.prompt + " Select clear..."
        time.sleep(3)
        self.clearx, self.cleary = autopy.mouse.get_pos()
        if(self.p): print self.succes + " Using point (" + str(self.clearx) + ", " + str(self.cleary) + ")"