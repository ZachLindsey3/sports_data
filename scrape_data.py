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

def main():
    player_link_data = get_all_letters()
    player_link_data.to_csv('./data/player_name_data.csv')
    print(player_link_data)
    
    print("goodbye world")

if __name__ == "__main__":
    main()