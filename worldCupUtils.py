import requests
import json
import datetime
import urllib
import os
from dateutil import tz, parser
from apikeyPRIVATE import world_cup_email, world_cup_pw

class WorldCupUtils():

    def __init__(self):
        self.path = "/home/pi/Documents/Scoreboard/"
        self.email = world_cup_email
        self.pw = world_cup_pw
        self.token = None

    
    def apiLogin(self):
        headers = {
            'Content-Type': 'application/json',
        }

        data_raw = '{"email": "' + self.email + '", "password": "' + self.pw + '"}'

        url = "http://api.cup2022.ir/api/v1/user/login"

        response = requests.post(url, headers=headers, data=data_raw).json()

        return response['data']['token']

    def worldCupMatches(self):

        self.token = self.apiLogin()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }

        matches = {}

        response = requests.get("http://api.cup2022.ir/api/v1/match", headers=headers).json()['data']

        for match in response:

            qatarTime = match['local_date'] + " +0300"

            qatarTime = datetime.datetime.strptime(qatarTime, '%m/%d/%Y %H:%M %z')

            localTz = datetime.datetime.now().astimezone().tzinfo

            localTime = qatarTime.astimezone(localTz)

            now = datetime.datetime.now(localTz)

            dif = localTime - now

            days = abs(dif.days)

            if days < 4:

                id = match['id']

                home = self.convertName(match['home_team_en'])
                away = self.convertName(match['away_team_en'])

                # Only download flags once
                if not os.path.exists(self.path + f"worldCupFlags/{home}.png"):
                    urllib.request.urlretrieve(match['home_flag'], self.path + f"worldCupFlags/{home}.png")     
                if not os.path.exists(self.path + f"worldCupFlags/{away}.png"):
                    urllib.request.urlretrieve(match['away_flag'], self.path + f"worldCupFlags/{away}.png")

                data = {
                    "home" : home,
                    "away" : away,
                    "year" : localTime.year,
                    "month" : localTime.month,
                    "day" : localTime.day,
                    "dayString" : localTime.strftime("%A")[0:3],
                    "hour" : localTime.hour,
                    "minute" : localTime.minute,
                    "time" : match['time_elapsed'],
                    "finished" : match['finished'],
                    "group" : match['group'],
                    "homeScore" : match['home_score'],
                    "awayScore" : match['away_score'],
                }
                
                if localTime in matches:
                    matches[str(localTime)].append(data)
                else:
                    matches[str(localTime)] = [data]


        with open(self.path + "worldCupMatches.json", 'w') as file:
            json.dump(matches, file)

    def worldCupMatchesESPN(self):
        response = requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard").json()

        games = {}

        localZone = tz.tzlocal()

        for game in response['events']:

            date = game['date']

            utctime = parser.parse(date)
            time = utctime.astimezone(localZone)

            dayString = time.strftime('%A')[0:3]
            year = time.year
            month = time.month
            day = time.day
            hour = time.hour
            minute = time.minute

            home = game['competitions'][0]['competitors'][0]['team']['abbreviation']
            away = game['competitions'][0]['competitors'][1]['team']['abbreviation']


            data = {
                    "home" : home,
                    "away" : away,
                    "year" : year,
                    "month" : month,
                    "day" : day,
                    "dayString" : dayString,
                    "hour" : hour,
                    "minute" : minute,
                    "time" : game['competitions'][0]['status']['displayClock'][0:2],
                    "finished" : game['competitions'][0]['status']['type']['completed'],
                    "group" : "n/a",
                    "homeScore" : game['competitions'][0]['competitors'][0]['score'],
                    "awayScore" : game['competitions'][0]['competitors'][1]['score'],
                }

            games[f"{home} vs {away}"] = [data]

        with open(self.path + "worldCupMatchesESPN.json", 'w') as file:
            json.dump(games, file)



    def convertName(self, name):

        if name == "Ecuador":
            return "ECU"
        elif name == "Nederlands":
            return "NED"
        elif name == "Qatar":
            return "QAT"
        elif name == "Senegal":
            return "SEN"
        elif name == "England":
            return "ENG"
        elif name == "United States":
            return "USA"
        elif name == "Iran":
            return "IRN"
        elif name == "Wales":
            return "WAL"
        elif name == "Argentina":
            return "ARG"
        elif name == "Mexico":
            return "MEX"
        elif name == "Poland":
            return "POL"
        elif name == "Saudi Arabia":
            return "KSA"
        elif name == "Australia":
            return "AUS"
        elif name == "Denmark":
            return "DEN"
        elif name == "France":
            return "FRA"
        elif name == "Tunisia":
            return "TUN"
        elif name == "Costa Rica":
            return "CRC"
        elif name == "Germany":
            return "GER"
        elif name == "Japan":
            return "JPN"
        elif name == "Spain":
            return "ESP"
        elif name == "Belgium":
            return "BEL"
        elif name == "Canada":
            return "CAN"
        elif name == "Croatia":
            return "CRO"
        elif name == "Morocco":
            return "MAR"
        elif name == 'Brazil':
            return "BRA"
        elif name == "Cameroon":
            return "CMR"
        elif name == "Serbia":
            return "SRB"
        elif name == "Switzerland":
            return "SUI"
        elif name == "Ghana":
            return "GHA"
        elif name == "Portugal":
            return "POR"
        elif name == "South Korea":
            return "KOR"
        elif name == "Uruguay":
            return "URU"
        
        
        
        
        
        
        


if __name__ == '__main__':
    WorldCupUtils().worldCupMatches() 
    WorldCupUtils().worldCupMatchesESPN()     

