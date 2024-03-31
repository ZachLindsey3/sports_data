import re
import string
import time
import pandas as pd

import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

stat_addresses = {'defense_rb' : ('fantasy-points-against-RB.htm', 0),
                  'defense_te' : ('fantasy-points-against-TE.htm', 0),
                  'defense_qb' : ('fantasy-points-against-QB.htm', 0),
                  'defense_wr' : ('fantasy-points-against-WR.htm', 0),
                  'defense_team' : ('opp.htm', 0),
                  }

#scrape all player data of players starting with a certain letter
def get_player_by_letter(letter):
    player_index_url = f'https://www.pro-football-reference.com/players/{letter}/'

    player_html = BeautifulSoup(urlopen(player_index_url), 'html.parser').findAll('p')

    player_tuple_list = []
    for player in player_html:
        #scrape relevant info using regex
        player_name = re.findall('(?<=\"\>)(.*)(?=\<\/a)', str(player))
        player_address = re.findall('(?<=href\=\")(.*)(?=\.htm)', str(player))
        player_start_year = re.findall('(\d+)\-', str(player))
        player_end_year = re.findall('\-(\d+)', str(player))

        #dirty way to find the end of players list and finish funct
        if player_address == []:
            break

        player_tuple_list.append((str(player_name[0]), str(player_address[0]), int(player_start_year[0]), int(player_end_year[0])))

    return(pd.DataFrame(data=player_tuple_list, columns=['name', 'address', 'start_year', 'end_year']))

#scrape all player data of players starting with letters within a range "letters"
def get_all_letters(letters=string.ascii_uppercase):
    player_letter_list = []

    #loop through letters and apply get_player_by_letter function
    for letter in letters:
        player_letter_list.append(get_player_by_letter(letter))
        print(letter) #prints the letter as it is scraped (can be turned off)
        time.sleep(5)

    #concatenate all player data into a single df
    full_player_list = pd.concat(player_letter_list, ignore_index=True)
    full_player_list['player_id'] = full_player_list.index
    return(full_player_list)

# def get_all_teams():
#     team_index_url = 'https://www.pro-football-reference.com/teams/'

#     team_html = BeautifulSoup(urlopen(team_index_url), 'html.parser').findAll('table')
#     teams = team_html[0].findAll('th')
#     current_team_list = []

#     for team in teams:
#         if re.findall('(?<=href\=\")(.*)(?=\")', str(team)):
#             current_team_list.append(re.findall('(?<=href\=\")(.*)(?=\")', str(team))[0])

#     return(current_team_list)

def getLinks(link_table, regex='player_id\=(.*)\&amp'):
    link_list = []
    for link in link_table:
        link_list.append(re.findall(regex, str(link))[0])

    return(link_list)

def getPlayersByTeamSeason(team='virginia', season='2024'):
    team_index_url = f'https://www.lax.com/team?url_name={team}&year={season}'
    team_html = BeautifulSoup(urlopen(team_index_url), 'html.parser').findAll('table')

    player_table = team_html[1]
    player_df = pd.read_html(str(player_table))[0]
    player_df['Player_IDs'] = getLinks(player_table.findAll('a'), regex='player_id\=(.*)\&amp')

    goalie_table = team_html[2]
    goalie_df = pd.read_html(str(goalie_table))[0]
    goalie_df['Player_IDs'] = getLinks(goalie_table.findAll('a'), regex='player_id\=(.*)\&amp')

    print("++++++")
    print(player_df)
    print("++++++")
    print(goalie_df)


def getPlayerStatsBySeason(team='uva', season='2024'):
    team_index_url = f'https://www.lax.com/player?player_id=46&year={season}'

    team_html = BeautifulSoup(urlopen(team_index_url), 'html.parser').findAll('table')
    # print(team_html)
    teams = team_html[0].findAll('th')
    print(teams)
    print("++++++++")

    # table = BeautifulSoup.find_all('table')
    df = pd.read_html(str(team_html))[0]
    print(df)

    return(0)

def main():
    getPlayerStatsBySeason()
    getPlayersByTeamSeason()

    print("goodbye world")

if __name__ == "__main__":
    main()