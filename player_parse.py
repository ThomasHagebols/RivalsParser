# Code by Thomas Hagebols
# Github account: ThomasHagebols
# LinkedIn account: https://www.linkedin.com/in/thomas-hagebols/
# Date: 2017-04-21

from preamble import *



# Parse the page of a single player
def parse_player_page(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Retreive JSON
    json_data = tree.xpath('//div[@id="articles"]/@ng-init')

    # Write to file. For debugging purposes
    # f = open( 'data/file.json', 'w' )
    # f.write("\"general\":" + json_data[0][5:-1])
    # f.close()

    # Parse JSON
    parsed_json = json.loads(json_data[0][5:-1])

    # Print player info
    print(parsed_json["id"], parsed_json["person"]["last_name"], parsed_json["person"]["first_name"])

    colleges = []
    committed = False
    prospect_colleges = parsed_json["prospect_colleges"]
    for index, prospect_college in enumerate(prospect_colleges):
        col_id = prospect_college["college_id"]
        col_name = prospect_college["college"]["short_name"]
        col_sign = prospect_college["sign"]
        col_commit = prospect_college["commit"]
        col_offer = prospect_college["offer"]

        if col_offer == True:
            colleges.append({"college_id": col_id, "college_name": col_name, "commit": col_commit})

            if col_commit == True:
                committed = True

        # print(colleges[index])

        # Check if the sign and commit match. If they don't give an error
        # if col_sign != col_commit:
        #     print("sign != commmit for college ", col_name)
        #     raise ValueError("sign != commmit for college ", col_name)


    # Check if the player committed to at least one team
    if committed == False:
        print("Player didn't commit to any team ", parsed_json["id"], parsed_json["person"]["last_name"])
        raise ValueError("Player didn't commit to any team ", parsed_json["id"], parsed_json["person"]["last_name"])


    # Transform to data frame
    return pd.DataFrame(colleges, columns=['college_id', 'college_name', 'commit'])


# To test the individual script
if __name__ == "__main__":
    data = parse_player_page('https://n.rivals.com/content/prospects/89774')
    print(data)