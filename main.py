#### name: debtbot
#### desc: tweet national debt and percentage change
#### auth: christian barry
#### date: 26 sep 2023

import requests
from bs4 import BeautifulSoup as bs
from keys import *
import tweepy

def save_debt(str_to_write):
    with open("debt_file.txt", "w") as f:
        f.write(str_to_write)
    
    print(f"Saved {str_to_write} to file.")

def read_debt(file):
    pass

def get_debt():
    page = requests.get("https://www.pgpf.org/national-debt-clock")
    soup = bs(page.content, 'html.parser')
    debt_text = soup.find(id="ticker-text").text #<span class="ticker" id="ticker-text">$33,112,048,543,774</span>

    return debt_text

def main():
    client.create_tweet(text=f"Today's #nationaldebt: {get_debt()}")

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

# testing 2