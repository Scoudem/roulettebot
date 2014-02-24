#
# FILE: roulettebot.py
#
# DESCRIPTION:
#
# AUTHOR: Tristan van Vaalen
# VERSION: 0.0.1.0
#

import controller
import graphics
import time
import sys, getopt
import autopy
import colorama
colorama.init()

class roulettebot:

    def __init__(self, argv):
        risk = 4
        p = True

        try:
            opts, args = getopt.getopt(argv,"r:h", ["help", "risk", "noprint"])
        except getopt.GetoptError:
            self.error("Invalid argument. Use <roulettebot.py -help> for instructions.")

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print "DISPLAY HELP HERE"
            elif opt in ("--noprint"):
                p = False
            elif opt in ("-r", "--risk"):
                try:
                    r = int(arg)
                except ValueError:
                    self.error(opt + " requires an int > 0")
                
                if r >= 1:
                    print "\x1b[35m[NOTICE]\x1b[0m Using risklevel " + arg
                    risk = r
                else:
                    self.error(opt + " requires and int > 0")

        self.controller = controller.controller(risk, p)
        self.graphics = graphics.graphics()

    def error(self, string):
        print "\x1b[31m[FATAL]\x1b[0m " + string
        sys.exit(1)

    def setup(self):
        print "\x1b[36m[STARTUP]\x1b[0m ROULETTEBOT VERSION 0.0.1.0"
        self.controller.getWorkspace()

    def main(self):
        while(True):
            self.controller.checkTimeout()
            time.sleep(0.1)
            self.controller.spin()
            time.sleep(1)
            self.controller.scanNumber()
            time.sleep(0.1)

            result1 = self.controller.checkDataColor()
            result2 = self.controller.checkDataRow()
            self.controller.checkWin()

            if(result1 != None):
                self.controller.betColor(result1)
            if(result2 != None):
                self.controller.betNumber(result2 + 36, "row")
#
# Default run
#
if __name__ == '__main__':
    roulettebot = roulettebot(sys.argv[1:])
    roulettebot.setup()
    roulettebot.main()
    