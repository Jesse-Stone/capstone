from bs4 import BeautifulSoup
import requests
import re
import csv
from urllib.parse import urljoin
import numpy as np
import pandas as pd
import time

#Setting the view for pandas to see all rows/columns for testing purposes
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)

#Used to test one name
source = 'https://www.rottentomatoes.com/critics/authors'

#Use this as URL endpoints for looping letter names and URLs
end_url_letter = '?letter=y'
end_url = '/movies?page='

print(source+end_url_letter)

#Eventually use this to place dataframe into...maybe by letter first?
#csv_file = open('rotten_scrape.csv', 'x')


def make_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_links(url):
    """For a given URL last name letter, get all the critic page links where the critic's last name begins with that letter"""
    soup = make_soup(url)
    a_tags = soup.find_all('a', href=re.compile(r"^/critic/")) #used regex to find ahref tags that have critic names
    links = [urljoin(url, a['href'])for a in a_tags]  # convert relative url to absolute url
    removed_tv_people = [x for x in links if not any(c.isdigit() for c in x)] #tv people seem to have digits in thier url..will test more later
    added = [link + end_url for link in removed_tv_people]# add the page= end to all the urls to start
    return added

print(get_links(source+end_url_letter))


def critic_name(url):
    """takes in critic page, and outputs the critic name"""
    soup = make_soup(url)
    name = soup.select('h1.title')[0].text.strip()
    return name


def get_reviews(url):
    """for each page which contains a maximum of 50 reviews, get all of those reviews"""
    soup = make_soup(url)
    table = soup.find_all('div', id="review-table") # looks for the review table
    data = []
    for x in table:
        z = (x.find_all('tr')) #finds the rows in the table
        for row in z:
            cols = row.find_all('td')
            spans = row.find_all('span') #this looks for the tomato/rotten icons
            spans = [x['class'][:1:-1] for x in spans] #extracts the name of the span class which is the icon
            flat_list = [item for sublist in spans for item in sublist] #flattens the list
            arr = np.array(flat_list) #not sure if needed?
            audience_icon =(arr[1:2]) #getting the audience icon from the array
            critic_icon = (arr[:1]) #getting the critic icon from the array
            cols = [ele.text.strip() for ele in cols] #extracts the review data and puts in list
            for x in critic_icon:
                cols.append(x) #appends the critic icon to the review
            for x in audience_icon:
                cols.append(x) #appends the audience icon to the review
            data.append([ele.replace('\n', '') for ele in cols if ele]) # gets rid of new line white space
    return data


def scan_pages(url):
    """For each individual critic, go through all the review pages (max 50 reviews per page)"""
    scan = True
    num = 1
    reviews = []
    while scan == True: #this is used to keep incrementing the review page number, and it stops once the tables are empty in the next review page
        #print(num)
        page = url + str(num)
        response = requests.get(page)
        if response.url[-1] == "v": #this is to check if the reviewer only
            break
        check_if_blank = len(get_reviews(page))
        print("reviews on page:",check_if_blank)
        #print(check_if_blank)
        if check_if_blank == 1:
            scan = False
        reviews.append(get_reviews(page))
        num = num + 1
    pages = num - 1 # n - 1 pages for loop
    df = pd.DataFrame()
    for i in range(pages): # takes all the review pages and loops through them, appending to one dataframe
        dfx = pd.DataFrame(reviews[i])
        df = df.append(dfx)
    df = df.reset_index()
    df = df.drop(columns='index')
    name = critic_name(url) #from the get name / critic_name function
    df["name"] = name
    print("all pages scanned")
    return df


def review_cleaner(df):
    """Takes in all the reviews for a critic, and cleans them"""
    if len(df.columns) != 7:
        return pd.DataFrame()
    else:
        columns = ["rating", "t_meter", "title", "review","critic_icon","audience_icon","name"]
        df.columns = columns
        df["year"] = df["title"].str.extract('.*\((.*)\).*')
        df["title"] = df['title'].str.replace(r"\(.*\)", "")
        df['title'] = df['title'].str.strip()
        df = df.dropna()
        return df


def write_data(url,letter):
    f = 'rotten_scrape_y.csv'
    links = get_links(source+letter)
    for idx, name in enumerate(links):
        df = scan_pages(name)
        df_clean = review_cleaner(df)
        df_clean.to_csv(f, mode='a', header=False)
        time.sleep(2)
        print(idx)

write_data(source,end_url_letter)





