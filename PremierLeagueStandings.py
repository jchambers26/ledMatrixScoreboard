import requests
import json
from apikeyPRIVATE import api_key

class PremierLeagueStandings():

    def __init__(self):
        self.path = "/home/pi/Documents/Scoreboard/eplStandings.json"
        self.key = api_key

    def getStandings(self):
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        }

        request = requests.get("http://v3.football.api-sports.io/standings?league=39&season=2022", headers=headers).json()

        with open(self.path, 'w') as file:
            json.dump(request, file)

if __name__ == '__main__':
    PremierLeagueStandings().getStandings()
