import requests
import json
from apikeyPRIVATE import api_key
import urllib

class PremierLeagueUtils():

    def __init__(self):
        self.path = "/home/pi/Documents/Scoreboard/"
        self.key = api_key
        self.ids = {}

    def getStandingsAndLogos(self):
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        }

        standings = {}

        request = requests.get("http://v3.football.api-sports.io/standings?league=39&season=2022", headers=headers).json()

        request = request['response'][0]['league']['standings'][0]

        for team in request:
            url = team['team']['logo']
            urllib.request.urlretrieve(url, f"{self.path}/eplLogos/{team['team']['name']}.png")
            standings[team['rank']] = {
                'team' : team['team']['name'],
                'points' : team['points'],
                'won' : team['all']['win'],
                'draw' : team['all']['draw'],
                'lost' : team['all']['lose'],
                'gf' : team['all']['goals']['for'],
                'ga' : team['all']['goals']['against']
            }

        with open(self.path + "eplStandings.json", 'w') as file:
            json.dump(standings, file)



if __name__ == '__main__':
    PremierLeagueUtils().getStandingsAndLogos()
