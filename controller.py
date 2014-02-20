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
import ctypes
colorama.init()

class controller:

    def __init__(self, risk, p):
        self.risk = risk
        self.p = p

        self.notice = "\x1b[35m[NOTICE]\x1b[0m"
        self.succes = "\x1b[32m[SUCCES]\x1b[0m"
        self.prompt = "\x1b[34m[PROMPT]\x1b[0m"
        self.fatal  = "\x1b[31m[FATAL]\x1b[0m"
        self.streakColor = (1, None) #First: streakColor number. Second: color
        self.streakRow = (1, 1)
        self.betstreakRow = 1
        self.lastcolor = None
        self.lastnumber = None
        self.betstreakColor = 1

        self.numbers = {0: ('green', None), 1: ('red', None), 2: ('black', None), 3: ('red', None), 4: ('black', None), 5: ('red', None), 6: ('black', None), 7: ('red', None), 8: ('black', None), 9: ('red', None), 10: ('black', None), 11: ('black', None), 12: ('red', None), 13: ('black', None), 14: ('red', None), 15: ('black', None), 16: ('red', None), 17: ('black', None), 18: ('red', None), 19: ('red', None), 20: ('black', None), 21: ('red', None), 22: ('black', None), 23: ('red', None), 24: ('black', None), 25: ('red', None), 26: ('black', None), 27: ('red', None), 28: ('black', None), 29: ('black', None), 30: ('red', None), 31: ('black', None), 32: ('red', None), 33: ('black', None), 34: ('red', None), 35: ('black', None), 36: ('red', None)}
        for i in range(0,37):
            self.numbers[i] = (self.numbers[i][0], autopy.bitmap.Bitmap.open("image/number/" + str(i) + ".png", "png"))

    #
    # Moves the mouse to position x,y.
    # Param: x, y
    #
    def moveMouseAbs(self, x, y):
        # if(self.p): print self.notice + " Moving to (" + str(x) + ", " + str(y) + ")."
        ctypes.windll.user32.SetCursorPos(x, y)
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
            ctypes.windll.user32.SetCursorPos(x + xoff, y + yoff)
            autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        else:
            ctypes.windll.user32.SetCursorPos(x + xoff, y + yoff)

        # if(self.p): print self.succes + " Moved " + str(xoff) + "x and " + str(yoff) + "y."
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


    def scanNumber(self):
        main = autopy.bitmap.capture_screen()
        area = main.get_portion(self.workspaceNumber[0], self.workspaceNumber[1])
        for i in range(0, 37):
            result = area.find_bitmap(self.numbers[i][1])
            if result != None:
                if(self.p): print self.notice + " Found " + str(i) + " " + self.numbers[i][0]
                self.lastcolor = self.numbers[i][0]
                self.lastnumber = i
                break;

    #
    # Checks if we have a streakColor. if so: start betting.
    #
    def checkDataColor(self):
        if(self.lastcolor == self.streakColor[1]):
            self.streakColor = (self.streakColor[0] + 1, self.streakColor[1])
            if(self.p): print self.notice + " " + str(self.streakColor[0]) + "x " + self.streakColor[1] + " streakColor. "
            
            if(self.streakColor[0] >= self.risk):
                if(self.streakColor[1] == "red"):
                    return "black"
                else:
                    return "red"
            else:
                return None
        else:
            if(self.betstreakColor != 1):
                if(self.lastcolor == "green"):
                    if(self.streakColor[1] == "red"):
                        return "black"
                    else:
                        return "red"
                else:
                    if(self.p): print self.succes + " WON WITH x " + str(self.betstreakColor) + " ON COLOR"
                    self.clearBet()
                    self.betstreakColor = 1
            self.streakColor = (1, self.lastcolor)
            return None


    #
    # MAKE A BUFFER
    # DETECT FROM LAST 4 * RISK ROLLS WHAT THE LEAST ROLLED ROW IS
    # START BETTING ON THAT
    #
    def checkDataRow(self):
        if(self.lastnumber % 3 == 0):
            row = 3
        elif(self.lastnumber % 3 - 2 == 0):
            row = 2
        elif(self.lastnumber % 3 - 1 == 0):
            row = 1
        else:
            row = -1

        if self.streakRow[1] != row:
            self.streakRow = (self.streakRow[0] + 1, self.streakRow[1])
            if(self.p): print self.notice + " " + str(self.streakRow[0]) + "x row " + str(self.streakRow[1]) + " streakRow."

            if(self.streakRow[0] >= self.risk * 2):
                return self.streakRow[1]
            else:
                return None
        else:
            self.streakRow = (1, row)
            if self.betstreakRow != 1:
                if(self.p): print self.succes + " WON WITH x " + str(self.betstreakRow) + " ON ROW"
                self.clearBet()
                self.betstreakRow = 1
            return None


    #
    # Clicks the desired collor n amount of times
    #
    def betColor(self, color):
        if(color == "red"):
            x = self.redx
            y = self.redy
        else:
            x = self.blackx
            y = self.blacky

        if(self.p): print self.notice + " Current betvalue: " + str(self.betstreakColor)

        self.moveMouseAbs(x, y)
        for i in range(0, self.betstreakColor):
            time.sleep(0.2)
            autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

        self.betstreakColor *= 2

    def betNumber(self, number, t):
        if number < 25:
            positionx = self.fieldx + (number + 2 - (3 * ((number - 1)/ 3))) * 22 + (((number - 1) / 3) * (22 + (number * 0.2)))
            offsety = 3 + (3 * ((number - 1)/ 3))
            positiony = self.fieldy + ((offsety - number) * 23) + (((number - 1) / 3) * (18 - (number * 0.15)))

        else:
            positionx = self.fieldx + (number + 2 - (3 * ((number - 1)/ 3))) * 22 + (((number - 1) / 3) * (22 + (number * 0.15)))
            offsety = 3 + (3 * ((number - 1)/ 3))
            positiony = self.fieldy + ((offsety - number) * 23) + (((number - 1) / 3) * (18 - (number * 0.05)))
        ctypes.windll.user32.SetCursorPos(int(round(positionx)), int(round(positiony)))

        if(t == "row"):
            for i in range(0, self.betstreakRow):
                time.sleep(0.2)
                autopy.mouse.click(autopy.mouse.LEFT_BUTTON)
            self.betstreakRow *= 2

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

        if(nx1 >= nx2 or ny1 >= ny2):
            # TODO: restart
            if(self.p): print self.fatal + " Invalid dimensions. Shutting down"
            sys.exit(1)
        else:
            if(self.p): print self.succes + " Using rectangle (" + str(nx1) + ", " + str(ny1) + ", " + str(nx2) + ", " + str(ny2) + ")."
            self.workspaceNumber = ((nx1, ny1), (nx2 - nx1, ny2 - ny1))

        if(self.p): print self.prompt + " Select corner of playfield (left corner of 1-18 box)..."
        time.sleep(3)
        self.fieldx, self.fieldy = autopy.mouse.get_pos()
        self.fieldy -= 85
        if(self.p): print self.prompt + " Using point (" + str(self.fieldx) + ", " + str(self.fieldy) + ")"

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