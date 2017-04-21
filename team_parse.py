# Code by Thomas Hagebols
# Github account: ThomasHagebols
# LinkedIn account: https://www.linkedin.com/in/thomas-hagebols/
# Date: 2017-04-21

from preamble import *
import player_parse
from pathlib import Path

import pprint
import time
import random

pp = pprint.PrettyPrinter(indent=1)
random.seed()

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
        if player['year'] == year and player['sport'] == "Football":
            urls.append(player['url'])

            # print(player['name'])
            # print(player['url'])
            # print(player['id'])
            # print(player['stars'])
            # print(player['rivals_rating'])
            # print(player['year'])

    return urls

# Get the id of a college belonging to a certain url
def get_college_id(url):
    url_list = get_players(url, 2010)
    player_info = player_parse.parse_player_page(url_list[0])

    college_info = player_info[player_info.commit == True].values.tolist()
    college_info = college_info[0]
    college_info.append(url)

    return college_info

    # TODO filter waar de regel True is

def process_players(urls, win_bet_col_id):
    matrix_operations = []

    # Add sleep to fool the firewall of the server
    n = random.random()
    time.sleep(n*2)


    for i, url in enumerate(urls):
        player_urls_with_errors = []
        print("\nParsing player", i+1, "of", len(urls), "url:", url)
        try:
            player_info = player_parse.parse_player_page(url)
            # print(player_info)

            lost_bets = player_info[player_info.college_id != win_bet_col_id]['college_id']

            for lost_bet_col_id in lost_bets:
                # print(lost_bet_col_id)
                matrix_operations.append((lost_bet_col_id,win_bet_col_id))
        except:
            print('Failed to this player. Url added to error list')
            player_urls_with_errors.append(url)

    return matrix_operations, player_urls_with_errors

def do_operations(adjacency_matrix, operations, colleges_pd):
    # Perform all operations in the operation list on the adjacency matrix
    for operation in operations:
        # Only apply operations of colleges which should in the final dataset
        if any(colleges_pd.college_id == operation[0]):
            x = colleges_pd[colleges_pd.college_id == operation[0]].index.tolist()
            y = colleges_pd[colleges_pd.college_id == operation[1]].index.tolist()
            adjacency_matrix[x,y] += 1

            # print('changing value of ',operation)
            # print('maps to:', x,y)
            # print('Has value', adjacency_matrix[x,y])

    # input("Press Enter to continue...")

    return



# To test the individual script
if __name__ == "__main__":
    data_path = 'data/'
    player_urls_with_errors = []


    # get college information
    # Check if csv with college info file exists
    if Path(data_path + 'colleges_info.csv').is_file():
        # import the data from the csv
        colleges_pd = pd.read_csv(data_path + 'colleges_info.csv')
    else:
        college_urls = pd.read_csv(data_path + 'universities.csv', names=['abbrivation', 'url'])
        # create the csv
        colleges = []
        for college_url in college_urls['url']:
            print(college_url)
            colleges.append(get_college_id(college_url))

        colleges_pd = pd.DataFrame(colleges, columns=['college_id', 'college_name', 'commit', 'url'])
        colleges_pd.to_csv(data_path + 'colleges_info.csv')

    for year in range(2003, 2014):
        print('Processing year:', year)
        adjacency_matrix = np.zeros((len(colleges_pd.index), len(colleges_pd.index)))
        matrix_operations=[]

        for index, college in colleges_pd.iterrows():
            print('Processing college', index, 'of', len(colleges_pd.index))
            url_list = get_players(college.url, year)

            op, puwe = process_players(url_list, college.college_id)

            player_urls_with_errors += puwe
            matrix_operations += op
            print(matrix_operations)
            print(player_urls_with_errors)

            # matrix_operations = filter(matrix_operations, colleges_pd.college_id)

        # Apply operations to matrix
        do_operations(adjacency_matrix, matrix_operations, colleges_pd)
        pd.DataFrame(adjacency_matrix).to_csv(data_path + str(year)+'.csv')

    pd.DataFrame(player_urls_with_errors).to_csv(data_path + 'pages_with_errors.csv')