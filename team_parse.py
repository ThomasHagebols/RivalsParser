# Code by Thomas Hagebols
# Github account: ThomasHagebols
# LinkedIn account: https://www.linkedin.com/in/thomas-hagebols-032676a8/
# Date: 2017-04-21

from lxml import html
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import parse_player

# Parse the list of url's of all players
def get_players(url, year):
    # Load page
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Retreive JSON
    json_data = tree.xpath('//rv-commitments/@prospects')
    parsed_json = json.loads(json_data[0])

    # Get list of url's
    urls = []
    for player in parsed_json:
        if player['year'] == year:
            urls.append(player['url'])
            # print(player['name'])
            # print(player['url'])
            # print(player['id'])
            # print(player['stars'])
            # print(player['rivals_rating'])
            # print(player['year'])

    return urls


# To test the individual script
if __name__ == "__main__":
    for year in range(2005, 2014):
        print("\n\n year:", year)
        url_list = get_players('https://bostoncollege.rivals.com/commitments/football/', year)

        for i, url in enumerate(url_list):
            print("Parsing url", i+1, "of", len(url_list), url)
            parse_player.parse_player_page(url)