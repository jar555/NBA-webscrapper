from __future__ import print_function
import nba_py
from nba_py import game, team
# import nba_py
import json
import urllib2
import html5lib
from bs4 import BeautifulSoup
import time
from json2html import *

currentTime = time.strftime('%m/%d/%Y')
currentYear = str(time.strftime('%Y'))
currentMonth = str(time.strftime('%m'))
currentDay = int(time.strftime('%d'))
currentNba = nba_py.Scoreboard()
print(currentDay)

teamsByName = {'hawks': 1610612737, 'celtics': 1610612738, 'cavaliers': 1610612739, 'pelicans': 1610612740
    , 'bulls': 1610612741, 'mavericks': 1610612742, 'nuggets': 1610612743, 'warriors': 1610612744
    , 'rockets': 1610612745, 'clippers': 1610612746, 'lakers': 1610612747, 'heat': 1610612748
    , 'bucks': 1610612749, 'timberwolves': 1610612750, 'nets': 1610612751, 'knicks': 1610612752
    , 'magic': 1610612753, 'pacers': 1610612754, '76ers': 1610612755, 'suns': 1610612756
    , 'trail blazers': 1610612757, 'kings': 1610612758, 'spurs': 1610612759, 'thunder': 1610612760
    , 'raptors': 1610612761, 'jazz': 1610612762, 'grizzlies': 1610612763, 'wizards': 1610612764
    , 'pistons': 1610612765, 'hornets': 1610612766}

teamsById = {1610612737: 'hawks', 1610612738: 'celtics', 1610612739: 'cavaliers', 1610612740: 'pelicans',
             1610612741: 'bulls'
    , 1610612742: 'mavericks', 1610612743: 'nuggets', 1610612744: 'warriors', 1610612745: 'rockets'
    , 1610612746: 'clippers', 1610612747: 'lakers', 1610612748: 'heat', 1610612749: 'bucks', 1610612750: 'timberwolves'
    , 1610612751: 'nets', 1610612752: 'knicks', 1610612753: 'magic', 1610612754: 'pacers', 1610612755: '76ers'
    , 1610612756: 'suns', 1610612757: 'trail blazers', 1610612758: 'kings', 1610612759: 'spurs', 1610612760: 'thunder'
    , 1610612761: 'raptors', 1610612762: 'jazz', 1610612763: 'grizzlies', 1610612764: 'wizards', 1610612765: 'pistons',
             1610612766: 'hornets'}


def getCurrentGames():
    # currentGames = currentNba.available()
    listOfGames = []

    for game in currentNba.game_header():
        listOfGames.append(teamsById[game['HOME_TEAM_ID']] + ' vs ' + teamsById[game['VISITOR_TEAM_ID']])
    return listOfGames

def getGameIds():
    listIds = []
    for game in currentNba.game_header():
        listIds.append(game['GAME_ID'])
    return listIds

def getBoxscore(id):
    nbaGame = game.Boxscore(str(id))
    boxscore = nbaGame.player_stats()
    teamStats = json.dumps(nbaGame.team_stats()).split()
    #homeTeamId = int(teamStats[5][:-1])
    homeTeamId = nbaGame.json['resultSets'][0]['rowSet'][0][1]
    #awayTeamId = int(teamStats[55][:-1])
    awayTeamId = nbaGame.json['resultSets'][1]['rowSet'][0][1]
    print(nbaGame)
    # print(len(team.TeamCommonRoster(homeTeamId,'2016-17').roster()))

    for dictionary in boxscore:
        for key in dictionary.keys():
            if dictionary[key] is None:
                dictionary[key] = 0

    boxscoreJson = {'data': boxscore}
    boxscoreHTML = json2html.convert(json=boxscoreJson)

    soup = BeautifulSoup(boxscoreHTML, 'html5lib')
    [s.extract() for s in soup('th', text='data')]
    soup.findAll('table')[1]['border'] = 0

    for row in soup.find_all('table')[0].tbody.findAll('tr'):
        rows = row.contents[0].contents[0].contents[0].contents
        for col in rows:
            col.contents[27].extract()
            col.contents[26].extract()
            col.contents[25].extract()
            col.contents[24].extract()
            col.contents[21].extract()
            col.contents[9].extract()
            col.contents[4].extract()
            col.contents[2].extract()

            col.contents[5], col.contents[0] = col.contents[0], col.contents[5]
            col.contents[10], col.contents[1] = col.contents[1], col.contents[10]
            col.contents[3], col.contents[3]
            # col.contents[0], col.contents[2] = col.contents[2], col.contents[0]
            col.contents[5], col.contents[2] = col.contents[2], col.contents[5]
            col.contents[4], col.contents[12] = col.contents[12], col.contents[4]
            col.contents[5], col.contents[14] = col.contents[14], col.contents[5]
            col.contents[6], col.contents[14] = col.contents[14], col.contents[6]
            col.contents[7], col.contents[13] = col.contents[13], col.contents[7]
            col.contents[8], col.contents[13] = col.contents[13], col.contents[8]
            col.contents[9], col.contents[12] = col.contents[12], col.contents[9]
            col.contents[10], col.contents[19] = col.contents[19], col.contents[10]
            col.contents[11], col.contents[16] = col.contents[16], col.contents[11]
            col.contents[12], col.contents[14] = col.contents[14], col.contents[12]
            col.contents[13], col.contents[19] = col.contents[19], col.contents[13]
            col.contents[14], col.contents[19] = col.contents[19], col.contents[14]
            col.contents[15], col.contents[18] = col.contents[18], col.contents[15]
            col.contents[16], col.contents[18] = col.contents[18], col.contents[16]
            col.contents[17], col.contents[17]
            col.contents[18], col.contents[19] = col.contents[19], col.contents[18]
        break

    [s.extract() for s in soup('th', text=['TEAM_ID', 'PLAYER_ID', 'TEAM_ABBREVIATION', 'GAME_ID', 'TEAM_CITY'])]

    homeTag = soup.new_tag('tr')
    homeTag.contents.append(soup.new_tag('th'))
    homeTag.find('th').insert(0, teamsById[homeTeamId].upper())

    awayTag = soup.new_tag('tr')
    awayTag.contents.append(soup.new_tag('th'))
    awayTag.find('th').insert(0, teamsById[awayTeamId].upper())

    a = soup.findAll('table')[1].find('tbody').contents[0]
    soup.findAll('table')[1].contents[0].contents[0].contents[0].contents[0].replaceWith('NAME')
    soup.findAll('table')[1].contents[0].contents[0].contents[1].contents[0].replaceWith('POS')
    soup.findAll('table')[1].contents[0].contents[0].contents[5].contents[0].replaceWith('+/-')
    a.append(homeTag)

    b = soup.find('table').contents[0].find('tbody').contents
    index = 0
    bench = False
    for thead in b:
        if bench == False:
            index += 1
            if thead.contents[2].contents[0] == '0':
                bench = True
                index -= 1
        else:
            index += 1
            if thead.contents[2].contents[0] != '0':
                index -= 1
                break
        #print(thead.contents[2].contents[0])
        #print(index)
    # print(b)
    res = b[index]
    res.append(awayTag)
    #print(awayTag)

    return soup

