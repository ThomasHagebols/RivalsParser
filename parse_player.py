# Code by Thomas Hagebols
# Github account: ThomasHagebols
# LinkedIn account: https://www.linkedin.com/in/thomas-hagebols-032676a8/
# Date: 2017-04-21

from lxml import html
import requests
import pandas as pd
from bs4 import BeautifulSoup


# Check if the total number of bids checks out with the number of rows
# Check it the number of accepted bids is exactly 1
def check_offer_errors(tr):
    nr_of_rows = len(tr.xpath('//*[@id="college_choices"]/tbody/tr'))
    nr_schools = len(tr.xpath('//a[@class="school"]/text()'))-1
    nr_accepted_bids = len(tr.xpath('//div[@class="checkmark-yellow"]'))
    nr_declined_bids = len(tr.xpath('//div[@class="checkmark-gray"]'))
    if nr_accepted_bids != 1 or (nr_accepted_bids + nr_declined_bids != nr_of_rows) or nr_of_rows!=nr_schools:
        print("We got the following values")
        print("accepted:", nr_accepted_bids, "declined:", nr_declined_bids, "rows:", nr_of_rows, "schools:", nr_schools)
        raise ValueError("The number of accepted, declined and total bids doesn't checkout")


# Parse the page of a single player
def parse_player_page(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Check of the number of offers check out
    try:
        check_offer_errors(tree)
    except ValueError:
        print("Something doesn't checkout in the number of offers (declined or accepted) at url: ", url)
        # raise ValueError("The number of accepted, declined and total bids doesn't checkout")

    schools = tree.xpath('//a[@class="school"]/text()')
    nr_of_bids = len(schools) - 1

    # Make list with a single 1 at the first element and the rest 0
    offer_status = [0] * nr_of_bids
    offer_status[0] = 1

    data = {'school': schools[1:], 'offer_accepted': offer_status}

    return pd.DataFrame(data, columns=['school', 'offer_accepted'])


# To test the individual script
if __name__ == "__main__":
    # This page gives a problem!!
    # Bowling Green is not included since it is not an <a>, but a <div>
    # Idea to fix dynamic page problem
    # //rv-commitments/@prospects
    data = parse_player_page('https://n.rivals.com/content/prospects/19949')
    print(data)