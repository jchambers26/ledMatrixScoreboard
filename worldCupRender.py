from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import json
from PIL import Image

class WorldCupRender:
    def __init__(self): 
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = 'adafruit-hat'
        self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False

        self.path = "/home/pi/Documents/Scoreboard/"
        self.font_path = "/home/pi/Documents/rpi-rgb-led-matrix/fonts/"

        self.monthConverter = self.makeMonthConverter()

    
    def renderWorldCupMatches(self):

        with open(self.path + 'worldCupMatches.json', 'r') as file:
            matches = json.load(file)

        matrix = RGBMatrix(options=self.options)
        canvas = matrix.CreateFrameCanvas()

        teamFont = graphics.Font()
        teamFont.LoadFont(self.font_path + "5x7.bdf")

        dataFont = graphics.Font()
        dataFont.LoadFont(self.font_path + "4x6.bdf")

        for t in sorted(matches):
            for match in matches[t]:

                away = match['away']
                home = match['home']
                year = match['year']
                month = match['month']
                day = match['day']
                dayString = match['dayString']
                hour = match['hour']
                minute = match['minute']
                matchTime = match['time']
                finished = match['finished']
                group = match['group']
                homeScore = match['homeScore']
                awayScore = match['awayScore']


                awayLogo = Image.open(f"./worldCupFlags/{away}.png")
                homeLogo = Image.open(f"./worldCupFlags/{home}.png")

                awayWidth = awayLogo.width
                awayHeight = awayLogo.height

                awayRatio = awayWidth / 24
                awayHeight = int(awayHeight / awayRatio)

                homeWidth = homeLogo.width
                homeHeight = homeLogo.height

                homeRatio = homeWidth / 24
                homeHeight = int(homeHeight / homeRatio)

                awayLogo.thumbnail((24, awayHeight), Image.ANTIALIAS)
                homeLogo.thumbnail((24, homeHeight), Image.ANTIALIAS)

                awayLogo = awayLogo.convert('RGB')
                homeLogo = homeLogo.convert('RGB')

                awayLogo = awayLogo.load()
                homeLogo = homeLogo.load()

                matrix.Clear()
                for x in range(64):
                    for y in range(32):
                        self.drawPixel(canvas, x, y, [10, 10, 10])
                for x in range(24):
                    for y in range(homeHeight):
                        self.drawPixel(canvas, x, y + 8 + (int(23 - homeHeight)/2), homeLogo[x, y])

                for x in range(24):
                    for y in range(awayHeight):
                        self.drawPixel(canvas, x + 40, y + 8 + (int(23 - awayHeight)/2), awayLogo[x, y])
                # matrix.SetImage(new_img, 0, 8)
                graphics.DrawText(canvas, teamFont, 5, 7, graphics.Color(255, 255, 255), f"{home}")
                graphics.DrawText(canvas, teamFont, 44, 7, graphics.Color(255, 255, 255), f"{away}")

                if matchTime == 'notstarted':

                    month = self.monthConverter[month]
                    if hour < 10:
                        hour = "0" + str(hour)
                    if minute < 10:
                        minute = "0" + str(minute)

                    graphics.DrawText(canvas, dataFont, 22, 7, graphics.Color(255, 255, 255), f"{hour}:{minute}")
                    graphics.DrawText(canvas, dataFont, 26, 14, graphics.Color(255, 255, 255), dayString)
                    graphics.DrawText(canvas, dataFont, 26, 21, graphics.Color(255, 255, 255), month)
                    graphics.DrawText(canvas, dataFont, 28, 28, graphics.Color(255, 255, 255), str(day))

                else:

                    if finished == "FALSE" or not finished:

                        if matchTime < 10:
                            matchTime = "0" + str(minute)

                    else:
                        matchTime = "FT"
                    
                    graphics.DrawText(canvas, teamFont, 30, 7, graphics.Color(255, 255, 255), group)
                    graphics.DrawText(canvas, dataFont, 28, 16, graphics.Color(255, 255, 255), str(matchTime))
                    graphics.DrawText(canvas, dataFont, 26, 24, graphics.Color(255, 255, 255), f"{homeScore}-{awayScore}")


                canvas = matrix.SwapOnVSync(canvas)
                time.sleep(5)


    def drawPixel(self, canvas, x, y, color):
        graphics.DrawLine(canvas, x, y, x, y, graphics.Color(int(color[0]), int(color[1]), int(color[2])))


    def makeMonthConverter(self):
        m = {}
        m[1] = "Jan"
        m[2] = "Feb"
        m[3] = "Mar"
        m[4] = "Apr"
        m[5] = "May"
        m[6] = "Jun"
        m[7] = "Jul"
        m[8] = "Aug"
        m[9] = "Sep"
        m[10] = "Oct"
        m[11] = "Nov"
        m[12] = "Dec"

        return m


if __name__ == '__main__':

    while True:
        WorldCupRender().renderWorldCupMatches()

