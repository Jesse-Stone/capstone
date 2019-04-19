#critic = soup.find_all('p', attrs={'class' : 'critic-names'})

# def get_reviews(url):
#     soup = make_soup(url)
#     table = soup.find_all('div', id="review-table")
#     data = []
#     for x in table:
#         z = (x.find_all('tr'))
#         for row in z:
#             cols = row.find_all('td')
#             cols = [ele.text.strip() for ele in cols]
#             data.append([ele.replace('\n', '') for ele in cols if ele])
#
#     df = pd.DataFrame(data)
#     columns = ["rating", "t_meter", "title", "review"]
#     df.columns = columns
#
#     df["year"] = df["title"].str.extract('.*\((.*)\).*')
#     df["title"] = df['title'].str.replace(r"\(.*\)", "")
#     df['title'] = df['title'].str.strip()
#     return df


def get_reviews(url):
    """for each page which contains a maximum of 50 reviews, get all of those reviews"""
    soup = make_soup(url)
    table = soup.find_all('div', id="review-table") # looks for the review table
    data = []
    for x in table:
        z = (x.find_all('tr')) #finds the rows in the table
        for row in z:

            cols = row.find_all('td')
            spans = row.find('span')
            print(spans)
            for x in cols:
                spans = x.find_all('span')
                spans = [ele for ele in spans]
                #print(spans['title'])
            # create a list of lines corresponding to element texts
            cols = [ele.text.strip() for ele in cols]
            data.append([ele.replace('\n', '') for ele in cols if ele]) # gets rid of new line white space
    return data
