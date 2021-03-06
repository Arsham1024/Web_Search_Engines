from bs4 import BeautifulSoup
import requests
import csv

# Most important english pages on wikipedia
# notice the en.wikipedia this shows that it is in english
def collect_links():
    ####### Global Vars
    body_links = []  # to store all the links of a certain page
    page_number = 1  # to name the output csv files
    header = ['text', 'href']  # used for the csv file later created
    base_URL = "https://en.wikipedia.org/"  # this is used to append all the pages that come after it.

    seed = requests.get(
        "https://en.wikipedia.org/w/index.php?title=Special:AllPages&from=%22Anonymous%22+anti-Scientology+protests").text  # This is the starting page
    next_page = seed  # at first this is the same as seed
    overal_num_links = 0

    ####### Main crawler
    # keep the crawler running for 10 pages which each include about 345 pages
    # a total of 3450 links/pages will be extracted
    while (page_number < 11):
        # Get it parsed through bs4
        soup = BeautifulSoup(next_page, 'lxml')
        # only choose the links in the list. not the links outside.
        all_links = soup.find('div', class_='mw-allpages-body')  # focus only on the main body of this page

        # now write out each element into a CSV file and save it as the number of the page
        # for example if we are on page 2 then the file name is 2.csv
        with open(f'Output/list.csv', 'a+') as f:
            writer = csv.DictWriter(f, fieldnames=header)

            # run through the list to get all of them
            for link in all_links.find_all('a'):
                body_links.append(link.get('href'))  # put every href in the array
                # write the header first
                writer.writerow({'text': link.text , 'href': link.get('href')})

            # incriment each page
            page_number += 1

        # focus on the navigation bar on the bottom with previous and next buttons (only 2 buttons in it)
        nav = soup.find('div', class_='mw-allpages-nav')
        # grab the one for next page to make the itterator
        next_nav = nav.find_all('a')[1].get('href')
        next_URL = base_URL + next_nav
        print(f"Moving to the page {page_number - 1} to collect links , The next pages URL is : ", next_URL)

        #     get next page into beautiful soup
        next_page = requests.get(next_URL).text
    # Output the overall number of links collected
    print("overal number of links collected: ", len(body_links))

# need a function that runs through all the pages extracted and finds their connections.
# This function also populates the

# Run the function
collect_links()