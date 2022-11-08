from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time

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
        matrix = RGBMatrix(options=self.options)

        canvas = matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont(self.font_path + "7x13.bdf")
        textColor = graphics.Color(255, 0, 0)
        pos1 = -1
        pos2 = 0
        pos3 = 0

        font2 = graphics.Font()
        font2.LoadFont(self.font_path + "7x13.bdf")

        while True:
            canvas.Clear()
            len1 = graphics.DrawText(canvas, font2, pos1, 9, graphics.Color(255, 255, 255), "EPL Standings")
            yPos = 18
            len2 = graphics.DrawText(canvas, font, pos2, yPos, textColor, "5. Manchester United")
            yPos += 10
            len3 = graphics.DrawText(canvas, font, pos3, yPos, graphics.Color(255, 255, 255), "23 Points 7-2-4")
            if (pos1 != 0):
                pos1 -= 1
            elif (pos2 != 0):
                pos2 -= 1
            elif (pos3 != 0):
                pos3 -= 1
        
            if (pos1 + len1 < canvas.width):
                time.sleep(0.5)
                pos1 = 0
                pos2 = -1
            elif (pos2 + len2 < canvas.width):
                time.sleep(0.5)
                pos2 = 0
                pos3 = -1
            elif (pos3 + len3 < canvas.width):
                time.sleep(0.5)
                pos3 = 0
                pos1 = -1

            time.sleep(0.05)
            canvas = matrix.SwapOnVSync(canvas)

if __name__=='__main__':
    while True:
        Standings().renderStandings()
