# Code by Thomas Hagebols
# Github account: ThomasHagebols
# LinkedIn account: https://www.linkedin.com/in/thomas-hagebols/
# Date: 2017-04-21

from preamble import *
import player_parse

# import time
# import random

# random.seed()

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
        print("\n\nyear:", year)
        url_list = get_players('https://bostoncollege.rivals.com/commitments/football/', year)

        for i, url in enumerate(url_list):
            print("\nParsing url", i+1, "of", len(url_list), url)
            data = player_parse.parse_player_page(url)
            print(data)
            # n = random.random()
            # time.sleep(n*2)