from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import json
from PIL import Image, ImageColor

class NFLRender():

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

    def renderNFLGames(self):

        with open(self.path + 'nflGames.json', 'r') as file:
            games = json.load(file)

        matrix = RGBMatrix(options=self.options)
        canvas = matrix.CreateFrameCanvas()

        teamFont = graphics.Font()
        teamFont.LoadFont(self.font_path + "5x7.bdf")

        dataFont = graphics.Font()
        dataFont.LoadFont(self.font_path + "4x6.bdf")


        for g in games:
            game = games[g]
            homeTeam = game['homeTeam']
            awayTeam = game['awayTeam']
            year = game['year']
            month = self.monthConverter[game['month']]
            day = game['day']
            dayString = game['dayString']
            hour = game['hour']
            minute = game['minute']
            homeColor = ImageColor.getcolor('#' + game['homeColor'].upper(), "RGB")
            awayColor = ImageColor.getcolor('#' + game['awayColor'].upper(), "RGB")
            homeScore = game['homeScore']
            awayScore = game['awayScore']
            timeRemaining = game['timeRemaining']
            possession = game['possession']
            homeID = game['homeID']
            awayID = game['awayID']
            if len(timeRemaining) == 4:
                timeRemaining = "0" + timeRemaining
            quarter = game['quarter']
            status = game['status']

            awayLogo = Image.open(f"./nflLogos/{awayTeam}.png")
            homeLogo = Image.open(f"./nflLogos/{homeTeam}.png")


            awayLogo.thumbnail((23, 23), Image.ANTIALIAS)
            homeLogo.thumbnail((23, 23), Image.ANTIALIAS)

            awayLogo = awayLogo.convert('RGB')
            homeLogo = homeLogo.convert('RGB')

            awayLogo = awayLogo.load()
            homeLogo = homeLogo.load()

            matrix.Clear()

            for x in range(23):
                for y in range(23):
                    self.drawPixel(canvas, x, y + 8, homeLogo[x, y])

            for x in range(23):
                for y in range(23):
                    self.drawPixel(canvas, x + 40, y + 8, awayLogo[x, y])

            homeCoord = 6 if len(homeTeam) == 2 else 4
            awayCoord = 48 if len(awayTeam) == 2 else 46
            graphics.DrawText(canvas, teamFont, homeCoord, 7, graphics.Color(homeColor[0], homeColor[1], homeColor[2]), f"{homeTeam}")
            graphics.DrawText(canvas, teamFont, awayCoord, 7, graphics.Color(awayColor[0], awayColor[1], awayColor[2]), f"{awayTeam}")


            if status == 'pre':
                if minute < 10:
                    minute = "0" + str(minute)

                timeCoord = 22 if hour >= 10 else 24

                graphics.DrawText(canvas, dataFont, timeCoord, 7, graphics.Color(255, 255, 255), f"{hour}:{minute}")
                graphics.DrawText(canvas, dataFont, 26, 14, graphics.Color(255, 255, 255), dayString)
                graphics.DrawText(canvas, dataFont, 26, 21, graphics.Color(255, 255, 255), month)
                graphics.DrawText(canvas, dataFont, 28, 28, graphics.Color(255, 255, 255), str(day))

            elif status == 'in':
                timeCoord = 22 if hour >= 10 else 24

                
                homeScoreCoord = 30 if int(homeScore) < 10 else 28
                awayScoreCoord = 30 if int(awayScore) < 10 else 28

                graphics.DrawText(canvas, dataFont, timeCoord, 7, graphics.Color(255, 255, 255), timeRemaining)
                graphics.DrawText(canvas, dataFont, 28, 21, graphics.Color(255, 255, 255), f"Q{quarter}")
                graphics.DrawText(canvas, dataFont, homeScoreCoord, 14, graphics.Color(homeColor[0], homeColor[1], homeColor[2]), homeScore)
                graphics.DrawText(canvas, dataFont, awayScoreCoord, 28, graphics.Color(awayColor[0], awayColor[1], awayColor[2]), awayScore)        

                # Possession Arrow
                if possession == homeID:
                    graphics.DrawText(canvas, dataFont, homeScoreCoord - 5, 14, graphics.Color(255, 255, 255), "<")
                else:
                    padding = 5 if int(awayScore) < 10 else 10
                    graphics.DrawText(canvas, dataFont, awayScoreCoord + padding, 28, graphics.Color(255, 255, 255), ">")


            elif status == 'post':

                homeScoreCoord = 30 if int(homeScore) < 10 else 28
                awayScoreCoord = 30 if int(awayScore) < 10 else 28

                graphics.DrawText(canvas, dataFont, 22, 7, graphics.Color(255, 255, 255), "FINAL") 
                graphics.DrawText(canvas, dataFont, homeScoreCoord, 14, graphics.Color(homeColor[0], homeColor[1], homeColor[2]), homeScore)
                graphics.DrawText(canvas, dataFont, 28, 21, graphics.Color(255, 255, 255), "--") 
                graphics.DrawText(canvas, dataFont, awayScoreCoord, 28, graphics.Color(awayColor[0], awayColor[1], awayColor[2]), awayScore)        

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
    NFLRender().renderNFLGames()