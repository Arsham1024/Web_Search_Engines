import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request

# Stating URL
seed = "https://www.apple.com/"

# HTML Parser
parser = HTMLParser

# Max number of pages crawiling
# change this later to 3000
pages = 10

# crawler function
def crawler(MAX_Pages):
    # getting the starter HTML and turning it into plain text
    text_page = requests.get(seed).text
    # To increment with each pages successfully crawled
    pages_visited = 0
    # To store all the links to crawl
    links_tocrawl = []

    # This function takes an array to save all the links extracted and an html page in text format (not URL!)
    extract_links(links_tocrawl, text_page)

    # Need a breadth first search type of algorithm for this crawler
    # These conditions should limit the amount of pages visited to maximum we want
    while pages_visited < MAX_Pages and len(links_tocrawl) < MAX_Pages:
        break
        # End of each iteration add one to counter
        # pages_visited += 1


# This method will extract only URLs and save them to the links to crawl array.
def extract_links(links_tocrawl, text_page):
    # This will take out all the links on a page and store the in the links_tocrawl array to be crawled.
    for link in BeautifulSoup(text_page, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href') and not link['href'].startswith("/") and not link['href'].startswith("#"):
            links_tocrawl.append(link['href'])
    # Print out the result
    print("This is the array content right now: " , links_tocrawl)


if __name__ == "__main__":
    crawler(pages)
