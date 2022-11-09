from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import json
from enum import Enum
from PIL import Image, ImageDraw
from io import BytesIO
import requests
from apikeyPRIVATE import api_key
import urllib.request


class PremierLeagueRender:
    def __init__(self): 
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = 'adafruit-hat'
        self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False

        self.path = "/home/pi/Documents/Scoreboard/"
        self.font_path = "/home/pi/Documents/rpi-rgb-led-matrix/fonts/"

        self.colors = self.plColors()


    def renderPremierLeagueStandings(self, printer=False):

        with open(self.path + 'eplStandings.json', 'r') as file:
            standings = json.load(file)
        
        matrix = RGBMatrix(options=self.options)
        canvas = matrix.CreateFrameCanvas()

        State = Enum('State', ['FIRST', 'SECOND'])

        state = State.FIRST

        teamFont = graphics.Font()
        teamFont.LoadFont(self.font_path + "7x13.bdf")

        titleFont = graphics.Font()
        titleFont.LoadFont(self.font_path + "5x8.bdf")

        # Loop over first to 20th place
        for place in range(1, 21):

            pos1 = canvas.width
            pos2 = canvas.width

            while True:
                canvas.Clear()
                # Draw the "EPL Standings" header with a line underneath
                len1 = graphics.DrawText(canvas, titleFont, 0, 6, graphics.Color(255, 255, 255), "EPL Standings")
                graphics.DrawLine(canvas, 0, 7, 64, 7, graphics.Color(255, 255, 255))

                team = standings[str(place)]['team']
                points = standings[str(place)]['points']
                won = standings[str(place)]['won']
                draw = standings[str(place)]['draw']
                lost = standings[str(place)]['lost']

                teamString = f"{place}. {team}"
                dataString = f"{points} points {won}-{draw}-{lost}"

                color = self.colors[team]

                # Draw the team name with their table position
                len2 = graphics.DrawText(canvas, teamFont, pos1, 18, color, teamString)
                
                # Draw the point total and record for the team
                len3 = graphics.DrawText(canvas, teamFont, pos2, 28, color, dataString)

                if (pos1 != canvas.width - len2 - 1 and state == State.FIRST):
                    pos1 -= 1
                elif (pos2 != canvas.width - len3 - 1 and state == State.SECOND):
                    pos2 -= 1
            
                if (pos1 == canvas.width - len2 - 1 and state == state.FIRST):
                    state = State.SECOND
                    pos1 = 0
                    time.sleep(0.5)
                    pos2 = canvas.width
                    continue
                elif (pos2 == canvas.width - len3 - 1 and state == state.SECOND):
                    state = State.FIRST
                    pos2 = 0
                    time.sleep(0.5)
                    pos1 = canvas.width
                    break

                time.sleep(0.05)
                canvas = matrix.SwapOnVSync(canvas)

    
    def renderPremierLeagueGames(self):

        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        }
        
        with open(self.path + 'eplMatches.json', 'r') as file:
            matches = json.load(file)
        with open(self.path + 'eplLogos.json', 'r') as file:
            logos = json.load(file)
        
        matrix = RGBMatrix(options=self.options)
        canvas = matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont(self.font_path + "5x8.bdf")

        for match in sorted(matches):

            awayTeam = matches[match]['awayTeam']
            homeTeam = matches[match]['homeTeam']

            urllib.request.urlretrieve(logos[awayTeam], 'away.png')
            urllib.request.urlretrieve(logos[homeTeam], 'home.png')
            awayLogo = Image.open('away.png')
            homeLogo = Image.open('home.png')

            awayLogo.thumbnail((24, 24), Image.ANTIALIAS)
            homeLogo.thumbnail((24, 24), Image.ANTIALIAS)

            awayLogo = awayLogo.convert('RGB')
            homeLogo = homeLogo.convert('RGB')

            print(f"{homeTeam} vs {awayTeam}")

            new_img = Image.new('RGB', (64, 24))
            new_img.paste(homeLogo, (0,0))
            new_img.paste(awayLogo, (39,0))

            matrix.Clear()
            matrix.SetImage(new_img, 0, 8)
            graphics.drawText(canvas, font, 9, 4, graphics.Color(255, 255, 255), f"{self.getAbbreviation(homeTeam)}")
            graphics.drawText(canvas, font, 31, 4, graphics.Color(255, 255, 255), "vs.")
            graphics.drawText(canvas, font, 49, 4, graphics.Color(255, 255, 255), f"{self.getAbbreviation(awayTeam)}")
            time.sleep(5)



    def getAbbreviation(self, team):

        if team == "Arsenal":
            return "ARS"
        elif team == "Aston Villa":
            return "AVL"
        elif team == "Bournemouth":
            return "BOU"
        elif team == "Brentford":
            return "BRE"
        elif team == "Brighton":
            return "BHA"
        elif team == "Chelsea":
            return "CHE"
        elif team == "Crystal Palace":
            return "CRY"   
        elif team == "Everton":
            return "EVE"
        elif team == "Fulham":
            return "FUL"
        elif team == "Leeds":
            return "LEE"
        elif team == "Leicester":
            return "LEI"
        elif team == "Liverpool":
            return "LIV"
        elif team == "Manchester City":
            return "MCI"
        elif team == "Manchester United":
            return "MUN"
        elif team == "Newcastle":
            return "NEW"
        elif team == "Nottingham Forest":
            return "NFO"
        elif team == "Southampton":
            return "SOU"
        elif team == "Tottenham":
            return "TOT"
        elif team == "West Ham":
            return "WHU"
        elif team == "Wolves":
            return "WOL"

        


    
    def plColors(self):
        colors = {}
        colors['Arsenal'] = graphics.Color(239, 1, 7)
        colors['Aston Villa'] = graphics.Color(149, 191, 229)
        colors['Bournemouth'] = graphics.Color(218, 41, 28)
        colors['Brentford'] = graphics.Color(227, 6, 19)
        colors['Brighton'] = graphics.Color(0, 87, 184)
        colors['Chelsea'] = graphics.Color(3, 70, 148)
        colors['Crystal Palace'] = graphics.Color(27, 69, 143)
        colors['Everton'] = graphics.Color(39, 68, 136)
        colors['Fulham'] = graphics.Color(255, 255, 255)
        colors['Leeds'] = graphics.Color(255, 205, 0)
        colors['Leicester'] = graphics.Color(0, 83, 160)
        colors['Liverpool'] = graphics.Color(200, 16, 46)
        colors['Manchester City'] = graphics.Color(108, 171, 221)
        colors['Manchester United'] = graphics.Color(218, 41, 28)
        colors['Newcastle'] = graphics.Color(255, 255, 255)
        colors['Nottingham Forest'] = graphics.Color(229, 50, 51)
        colors['Southampton'] = graphics.Color(215, 25, 32)
        colors['Tottenham'] = graphics.Color(255, 255, 255)
        colors['West Ham'] = graphics.Color(122, 38, 58)
        colors['Wolves'] = graphics.Color(253, 185, 19)

        return colors


if __name__=='__main__':

    while True:
        #PremierLeagueRender().renderPremierLeagueStandings()
        PremierLeagueRender().renderPremierLeagueGames()

