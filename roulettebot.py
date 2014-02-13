#
# FILE: roulettebot.py
#
# DESCRIPTION:
#
# AUTHOR: Tristan van Vaalen
# VERSION: 0.0.0.2
#

import controller
import graphics
import time
import autopy

class roulettebot:

    def __init__(self):
        self.controller = controller.controller()
        self.graphics = graphics.graphics()

    def setup(self):
        print "\x1b[36m[STARTUP]\x1b[0m ROULETTEBOT VERSION 0.0.0.2"
        self.controller.getWorkspace()

    def main(self):
        while(True):
            time.sleep(1)
            screen = autopy.bitmap.capture_screen(self.controller.workspace)
            result = screen.find_color(16777003, 0.0)
            #ZWART 16777003
            #ROOD 16192018
            self.controller.moveMouseAbs(result[0] + self.controller.workspace[0][0], result[1]+ self.controller.workspace[0][1])

#
# Default run
#
if __name__ == '__main__':
    roulettebot = roulettebot()
    roulettebot.setup()
    roulettebot.main()
    