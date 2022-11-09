import requests
import json
from dateutil import parser
from dateutil import tz
import datetime
import math


class PremierLeagueMatches():

    def __init__(self):
        self.path = "/home/pi/Documents/Scoreboard/eplMatches.json"
        self.gameweek = self.determineCurrentGameweek()
        self.teams = self.mapTeams()


    def determineCurrentGameweek(self):
        request = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()

        gameweeks = {}
        tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        now = datetime.datetime.now(tz)

        minDif = math.inf
        minGW = 0

        for gw in request['events']:
            time = parser.parse(gw['deadline_time'])
            difference = time - now
            days = abs(difference.days)
            if days < minDif:
                minDif = days
                minGW = gw['id']

        return minGW

    def mapTeams(self): 

        request = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
        teams = {}
        for team in request['teams']:
            teams[team['id']] = team['name']
        return teams



    def getMatches(self):

        localZone = tz.tzlocal()

        matches = {}

        fixtures = requests.get(f"https://fantasy.premierleague.com/api/fixtures/?event={self.gameweek}").json()
        id = 1
        for x in fixtures:
            time = parser.parse(x['kickoff_time'])
            time = time.astimezone(localZone)
            year = time.year
            month = time.month
            day = time.day
            hour = time.hour
            minute = time.minute

            matches[id] = {
                'awayTeam' : self.teams[x['team_a']],
                'homeTeam' : self.teams[x['team_h']],
                'kickoffTimeYear' : year,
                'kickoffTimeMonth' : month,
                'kickoffTimeDay' : day,
                'kickoffTimeHour' : hour,
                'kickoffTimeMinute' : minute,
                'started' : x['started'],
                'finished' : x['finished'],
                'awayTeamScore' : x['team_a_score'],
                'homeTeamScore' : x['team_h_score'],
                'minute' : x['minutes']
            }
            id += 1
        
        with open(self.path, 'w') as file:
            json.dump(matches, file)

if __name__ == '__main__':
    PremierLeagueMatches().getMatches()
            





