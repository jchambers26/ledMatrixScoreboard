import requests
import json
from dateutil import parser
from dateutil import tz
import os
import urllib

class NFLUtils():

    def __init__(self):
        self.logoPath = "/home/pi/Documents/Scoreboard/nflLogos/"
        self.path = "/home/pi/Documents/Scoreboard/nflGames.json"


    def getGames(self):

        localZone = tz.tzlocal()

        games = {}

        localZone = tz.tzlocal()

        response = requests.get("http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard").json()

        for game in response['events']:
            date = game['date']
            utctime = parser.parse(date)
            time = utctime.astimezone(localZone)

            dayString = time.strftime('%A')[0:3]
            year = time.year
            month = time.month
            day = time.day
            hour = time.hour - 12 if time.hour > 12 else time.hour
            minute = time.minute

            homeTeam = game['competitions'][0]['competitors'][0]['team']['abbreviation']
            homeID = game['competitions'][0]['competitors'][0]['id']
            homeColor = game['competitions'][0]['competitors'][0]['team']['color']
            if homeTeam in ['LV', 'PIT', 'PHI', 'BAL', 'HOU', 'DEN', 'MIN', 'DAL', 'LAC', 'LAR', 'NE', 'NYJ']:
                homeColor = game['competitions'][0]['competitors'][0]['team']['alternateColor']
            elif homeTeam == 'ATL':
                homeColor = 'A71930'
            elif homeTeam == 'NO':
                homeColor = 'D3BC8D'
            elif homeTeam == 'CHI':
                homeColor = 'C83803'
            elif awayTeam == 'WSH':
                awayColor = 'FFB612'
            elif awayTeam == 'CLE':
                awayColor = 'FF3C00'

            awayTeam = game['competitions'][0]['competitors'][1]['team']['abbreviation']
            awayID = game['competitions'][0]['competitors'][1]['id']
            awayColor = game['competitions'][0]['competitors'][1]['team']['color']
            if awayTeam in ['LV', 'PIT', 'PHI', 'BAL', 'HOU', 'DEN', 'MIN', 'DAL', 'LAC', 'LAR', 'NE', 'NYJ']:
                awayColor = game['competitions'][0]['competitors'][1]['team']['alternateColor']
            elif awayTeam == 'ATL':
                awayColor = 'A71930'
            elif awayTeam == 'NO':
                awayColor = 'D3BC8D'
            elif awayTeam == 'CHI':
                awayColor = 'C83803'
            elif awayTeam == 'WSH':
                awayColor = 'FFB612'
            elif awayTeam == 'CLE':
                awayColor = 'FF3C00'


            try:
                possession = game['competitions'][0]['situation']['possession']
            except:
                possession = None


            # Only download logos once
            if not os.path.exists(self.logoPath + f"{homeTeam}.png"):
                logo = game['competitions'][0]['competitors'][0]['team']['logo']
                urllib.request.urlretrieve(logo, self.logoPath + f"{homeTeam}.png")     
            if not os.path.exists(self.logoPath + f"{awayTeam}.png"):
                logo = game['competitions'][0]['competitors'][1]['team']['logo']
                urllib.request.urlretrieve(logo, self.logoPath + f"{awayTeam}.png")

            homeScore = game['competitions'][0]['competitors'][0]['score']
            awayScore = game['competitions'][0]['competitors'][1]['score']

            timeRemaining = game['competitions'][0]['status']['displayClock']
            quarter = game['competitions'][0]['status']['period']
            status = game['competitions'][0]['status']['type']['state']

            data = {
                "homeTeam" : homeTeam,
                "homeID" : homeID,
                "awayTeam" : awayTeam,
                "awayID" : awayID,
                "possession" : possession,
                "year" : year,
                "month" : month,
                "day" : day,
                "dayString" : dayString,
                "hour" : hour,
                "minute" : minute,
                "homeColor" : homeColor,
                "awayColor" : awayColor,
                "homeScore" : homeScore,
                "awayScore" : awayScore,
                "timeRemaining" : timeRemaining,
                "quarter" : quarter,
                "status" : status
            }

            keyString = f"{homeTeam} vs {awayTeam}"

            games[keyString] = data

        with open(self.path, 'w') as file:
            json.dump(games, file)

if __name__ == '__main__':
    NFLUtils().getGames()
            