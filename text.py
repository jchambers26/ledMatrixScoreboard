from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
from enum import Enum

class Standings:
    def __init__(self): 
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = 'adafruit-hat'
        self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False

        self.path = "/home/pi/Documents/Scoreboard/"
        self.font_path = "/home/pi/Documents/rpi-rgb-led-matrix/fonts/"


    def renderStandings(self, printer=False):

        State = Enum('State', ['FIRST', 'SECOND', 'THIRD'])

        state = State.SECOND
        matrix = RGBMatrix(options=self.options)

        canvas = matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont(self.font_path + "7x13.bdf")
        textColor = graphics.Color(255, 0, 0)
        pos1 = 0
        pos2 = canvas.width
        pos3 = canvas.width

        font2 = graphics.Font()
        font2.LoadFont(self.font_path + "5x8.bdf")

        while True:
            canvas.Clear()
            len1 = graphics.DrawText(canvas, font2, pos1, 6, graphics.Color(255, 255, 255), "EPL Standings")
            graphics.DrawLine(canvas, 0, 7, 64, 7, graphics.Color(255, 255, 255))
            yPos = 18
            len2 = graphics.DrawText(canvas, font, pos2, yPos, textColor, "5. Manchester United")
            yPos += 10
            len3 = graphics.DrawText(canvas, font, pos3, yPos, graphics.Color(255, 255, 255), "23 Points 7-2-4")

            if (pos2 != canvas.width - len2 - 1 and state == State.SECOND):
                pos2 -= 1
            elif (pos3 != canvas.width - len3 - 1 and state == State.THIRD):
                pos3 -= 1
        
            if (pos2 == canvas.width - len2 - 1 and state == state.SECOND):
                state = State.THIRD
                pos2 = 0
                time.sleep(0.5)
                pos3 = canvas.width
                continue
            elif (pos3 == canvas.width - len3 - 1 and state == state.THIRD):
                state = State.SECOND
                pos3 = 0
                time.sleep(0.5)
                pos2 = canvas.width
                continue

            time.sleep(0.05)
            canvas = matrix.SwapOnVSync(canvas)

if __name__=='__main__':
    while True:
        Standings().renderStandings()
