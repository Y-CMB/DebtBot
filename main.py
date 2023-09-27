#### name: debtbot
#### desc: tweet national debt and percentage change
#### auth: christian barry
#### date: 26 sep 2023

import requests
import tweepy
from keys import *
from bs4 import BeautifulSoup as bs
from pathlib import Path

debt_file = Path(DEBT_PATH)

def save_debt(str_to_write):
    with open(debt_file, "w") as f:
        f.write(str_to_write)
    
    print(f"Saved {str_to_write} to file.")

def read_debt(new_debt):
    old = ""
    new = ""

    # remove $ from new_debt
    for char in new_debt:
        if char.isnumeric():
            new += char
        else:
            continue
    
    with open(debt_file, "r") as f:
        content = f.read()

        # remove $ from old_debt
        for char in content:
            if char.isnumeric():
                old += char
            else:
                continue

    perc_change = ((int(new) - int(old)) / int(old)) * 100 # n2-n1/n1 * 100
    updown = ""

    if 0 > perc_change:
        updown = "decrease"
    else:
        updown = "increase"

    return perc_change, updown

def get_debt():
    page = requests.get("https://www.pgpf.org/national-debt-clock")
    soup = bs(page.content, 'html.parser')
    debt_text = soup.find(id="ticker-text").text #<span class="ticker" id="ticker-text">$33,112,048,543,774</span>

    return debt_text

def main():
    # get the current debt
    new_debt = get_debt()

    # calc change
    perc_change, updown = read_debt(new_debt)

    # tweet
    client.create_tweet(
        text=f"""FROM THE BOT:
        Today's #nationaldebt: {new_debt}
        That's a {round(perc_change, 5)}% {updown} from yesterday.
    credit: https://www.pgpf.org/national-debt-clock
"""
        )

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API obj
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
    )

# Tweet
if __name__ == "__main__":
    # add timing
    try:
        main()
    except Exception as err:
        print(f"Something went wrong: {err}")

