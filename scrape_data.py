import re
import string
import time
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup

stat_addresses = {'defense_rb' : ('fantasy-points-against-RB.htm', 0),
                  'defense_te' : ('fantasy-points-against-TE.htm', 0),
                  'defense_qb' : ('fantasy-points-against-QB.htm', 0),
                  'defense_wr' : ('fantasy-points-against-WR.htm', 0),
                  'defense_team' : ('opp.htm', 0),
                  }

#code to scrape a single seasons data
def single(season):
    url = f'https://www.pro-football-reference.com/years/{season}/scoring.htm'
    table_html = BeautifulSoup(urlopen(url), 'html.parser').findAll('table')
    df = pd.read_html(str(table_html))[0]
    df = df.drop('Rk', 1) # drop Rk columns
    df.Player = df.Player.str.replace('*','') # remove asterisk on player's name
    df.insert(0,'Season',season) # insert season column
    df = df.apply(pd.to_numeric, errors='coerce').fillna(df) # convert non string values to numeric
    return df

##function to scrape multiple seasons of data at a time
def multiple(start_year,end_year):
    df = single(start_year)
    while start_year < end_year:
        time.sleep(4)                     ##code sleeps for 4 seconds between calls as 20 requests per minute 
        start_year = start_year + 1       ##are allowed meaning only 15 requests per minute will be made here
        df = df.append(single(start_year))
    return df

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


def main():
    letter = 'A'

    # player_df = get_player_by_letter(letter)
    # print(player_df)
    player_letter_list = []
    for letter in string.ascii_uppercase:
        player_letter_list.append(get_player_by_letter(letter))
        print(letter)
        time.sleep(5)
    
    print("goodbye world")

if __name__ == "__main__":
    main()