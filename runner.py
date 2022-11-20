from premierLeagueRender import PremierLeagueRender
from worldCupRender import WorldCupRender
from nflRender import NFLRender


if __name__ == '__main__':
    while True:
        #PremierLeagueRender().renderPremierLeagueStandings()
        #PremierLeagueRender().renderPremierLeagueGames()
        WorldCupRender().renderWorldCupMatches()
        NFLRender().renderNFLGames()