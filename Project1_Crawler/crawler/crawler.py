import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import re
import random
import time
import csv
from langdetect import detect

# Stating URLs
from urllib3.exceptions import InsecureRequestWarning, NewConnectionError, MaxRetryError

all_seeds = ["https://en.wikipedia.org/wiki/General-purpose_programming_language",
             "https://fa.wikipedia.org/wiki/%D9%88%DB%8C%DA%A9%DB%8C%E2%80%8C%D9%BE%D8%AF%DB%8C%D8%A7%DB%8C_%D9%81%D8%A7%D8%B1%D8%B3%DB%8C",
             "https://www.esmadrid.com/"]

# Max number of pages crawling
# change this later to 3000
MAX_Pages = 200
#PAGE_LIMIT = 500 # set for extracting pages
# This is a global variable indicating the current language that is being checked.
# default is english
all_langs = ["English", "Farsi", "Spanish"]
current_language = all_langs[1]
# This will give the correct seed for the current language and set it to current seed
current_seed = all_seeds[0]

# Creating report.csv file for links and number outlinks
with open('report.csv', 'w', encoding='UTF8', newline='') as report:
    writer = csv.writer(report)
    report.close()


# crawler function
def crawler():
    # To store all the links intended to crawl
    links_tocrawl = []
    global current_language
    # current seed correlates to the language being crawled
    global current_seed

    for i in range(len(all_langs)):
        current_lang = all_langs[i]
        print("The current languages under search is : ", current_lang)
        pages_visited = 0
        # To store all the links to crawl
        # initially only has the seed at index 0
        links_tocrawl = [all_seeds[i]]
        # This method is the engine of the crawler and while loop is located here
        # By the end of each crawl cycle a language is fully crawled.
        crawl(MAX_Pages, links_tocrawl, pages_visited)

        # extract and store html content into repository
        extract_pages(MAX_Pages, links_tocrawl, current_lang)

        # Extracts all outlinks in links_tocrawl
        report_links(MAX_Pages, links_tocrawl, pages_visited, current_lang)


# While loop of the crawler, This is separated because
# the crawler needs to run multiple times and with different specifications
def crawl(MAX_Pages, links_tocrawl, pages_visited):
    # Temporary while loop timer for debugging
    start1 = time.time()
    global current_language
    # These conditions should limit the amount of pages visited to maximum we want
    while pages_visited < MAX_Pages and len(links_tocrawl) < MAX_Pages:
        # Starting timer for politeness time-out
        start_time = time.time()
        text_page = requests.get(links_tocrawl[pages_visited]).text
        crawl_delay = time.time() - start_time

        # Extract all the links in the page to be searched over later.
        extract_links(links_tocrawl, text_page, pages_visited)

        # End of each iteration add one to counter
        pages_visited += 1

        # Time-out based on time it takes to load the page and randomly multiplied by 1 or 2
        time.sleep(random.uniform(1, 2) * crawl_delay)

    # Outputting how many links have been recorded.
    print("The number of pages visited for above language : ", len(links_tocrawl))
    # Prints runtime of while loop
    end = time.time()
    print("Runtime : ", end - start1, "\n")


# This method requests html content for each url
def extract_pages(max_pages, links_tocrawl, language_):
    for i, link in enumerate(links_tocrawl):
        try:
            text_page = requests.get(links_tocrawl[i]).text
            print("Extract Link:", "#", i, links_tocrawl[i])
            # call to store content in repository
            store_pages(text_page, i + 1, language_)
        except Exception:
            pass
        time.sleep(2)
        # stop iteration after maximum page limit
        if i + 1 >= max_pages:
            break


# This method saves extracted html pages into repository
def store_pages(text_page, page, language_):
    soup = BeautifulSoup(text_page, 'html.parser')
    # store new data every times the program runs
    folderName = str(language_).title()
    fileName = str(language_).lower()
    if page == 1:
        file_ = open(f'../repository/{folderName}/{fileName}.txt', 'w', encoding='utf-8')
    # append html content to existing file
    else:
        file_ = open(f'../repository/{folderName}/{fileName}.txt', 'a', encoding='utf-8')
    # add each page to the file in repository and close the file
    file_.write(soup.prettify())
    file_.write("\n{}\n".format("=" * 100))
    file_.close()


# This method will extract only URLs and save them to the links to crawl array.
def extract_links(links_tocrawl, text_page, pages_visited):
    # Counter for number of outlinks found in a link
    outlinks = 0

    # This will take out all the links on a page and store the in the links_tocrawl array to be crawled.
    for link in BeautifulSoup(text_page, parse_only=SoupStrainer('a'), features="html.parser"):
        # This will do 3 checks
        #  1. checks if the link has href attribute (because these are links)
        #  2. checks to see if these hrefs start with http so that we know these are URLs and not relative links
        if link.has_attr('href') \
                and link['href'].startswith("http"):
            links_tocrawl.append(link['href'])
            outlinks += 1
        # else should skip this iteration of the loop and continue
        else:
            continue

    # Print out result of outlinks
    print("Current Link:", links_tocrawl[pages_visited], "Number of Outlinks:", outlinks)
    # Print out the result
    print("This is the array content : ", links_tocrawl)
    print("")


# Writes appended links and its number of outlinks to report.csv
def report_links(MAX_Pages, links_tocrawl, pages_visited, current_lang):
    # Prints header for language and outlinks in report
    header_row = (current_lang + ' Links:', "Outlinks:")
    with open('report.csv', 'a', encoding='UTF8', newline='') as report:
        writer = csv.writer(report)
        writer.writerow(header_row)

    # Loop which finds total outlinks in all links in links_tocrawl array up to MAX_Pages
    for i in range(MAX_Pages):
        outlinks = []
        text_page = requests.get(links_tocrawl[i]).text
        for link in BeautifulSoup(text_page, parse_only=SoupStrainer('a'), features="html.parser"):
            if link.has_attr('href') and link['href'].startswith("http"):
                outlinks.append(link['href'])
            else:
                continue

        # Writes links and its number of outlinks to report.csv
        print("Current Link:", "#", i, links_tocrawl[i], "Number of Outlinks:", len(outlinks))
        report_row = [links_tocrawl[i], len(outlinks)]
        with open('report.csv', 'a', encoding='UTF8', newline='') as report:
            writer = csv.writer(report)
            writer.writerow(report_row)

if __name__ == "__main__":
    crawler()
