import pandas as pd

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)

df = pd.read_pickle('/Users/jesse/capstone/critic_data_final.pkl')

df2 = df[["name","title","critic_icon"]]
df2 = df2.replace({'critic_icon': {"fresh": 1, "rotten": 0}})

"""Ratings Cleaner"""
df["rating_checker"] = df["rating"].str.split('/')
df['scale'] = df['rating_checker'].apply(lambda x: x[-1])
df['score'] = df['rating_checker'].apply(lambda x: x[0])



def standardizer(row):
    """Used to standardize all scores to 1/10 scale. After using, maintained 98% of all of the data."""
    if row['scale'] == '5':
        return 2 * float(row['score'])
    elif row['scale'] == '10':
        return float(row['score'])
    elif row['scale'] == '4':
        if row['score'] == '4':
            return 10.0
        elif row['score'] == '3.5':
            return 9.0
        elif row['score'] == '3':
            return 8.0
        elif row['score'] == '2.5':
            return 7.0
        elif row['score'] == '2':
            return 6.0
        elif row['score'] == '1.5':
            return 5.0
        elif row['score'] == '1':
            return 4.0
        elif row['score'] == '.5':
            return 3.0
        elif row['score'] == '0.5':
            return 3.0
        elif row['score'] == '0':
            return 0
    elif row['scale'] == 'A+':
        return 10.0
    elif row['scale'] == 'A':
        return 9.5
    elif row['scale'] == 'A-':
        return 9.0
    elif row['scale'] == 'B+':
        return 8.8
    elif row['scale'] == 'B':
        return 8.5
    elif row['scale'] == 'B-':
        return 8.0
    elif row['scale'] == 'C+':
        return 7.5
    elif row['scale'] == 'C':
        return 5.5
    elif row['scale'] == 'C-':
        return 4.5
    elif row['scale'] == 'D+':
        return 4.0
    elif row['scale'] == 'D':
        return 3.5
    elif row['scale'] == 'D-':
        return 3.0
    elif row['scale'] == 'F+':
        return 2.0
    elif row['scale'] == 'F':
        return 0

'''run the below to clean if needed'''

# df['scaled_rating'] = df.apply(standardizer, axis=1)
# df = df.dropna(subset=['scaled_rating'])
# pd.to_pickle(df,'scaled_cleaned.pkl')


















#print(df3[mask].groupby("score").count().sort_values(by="review_number"))
#print(df3)



#df['new_col'] = df["rating"][0].apply(lambda x: x * 2)

#print(df["rating"][0])

# for x in df["rating"].itterows():
#     if x[0] == 5:
#         df["rating_fixed"] = x[0]*2
# print(df.columns)

#print(df.groupby("rating").agg('count').sort_values(by = "review_number"))




# mask = (df["title"] == "Isn't It Romantic") & (df["critic_icon"] == "rotten")
# # mask2 = (df["title"] == "Dumbo") & (df["critic_icon"] == "fresh")
# #
# # mask23 = (df["title"] == "Avengers: Infinity War")
# # x = df[mask]["review"].values
# #
# # mask3 = (df["title"] == "Interstellar") & (df["critic_icon"] == "fresh")
# # mask4 = (df["title"] == "Interstellar")
# #
# # ask = (df["title"] == "Ghostbusters")
# # sw = df[(df["title"] == "Star Wars: The Last Jedi") & (df["critic_icon"] == "rotten")].values
# #
# #
# # test1 = (df[mask]["name"]).values
# # test2 = (df[mask2]["name"]).values
# # gb = (df[ask]["name"]).values
# #
# # reviewer = df[df["name"] == "Rich Cline"]
# #
# #
# #
# # print([i for i in test1 if i in test2])
# #
# # mask = reviewer["title"] == "Creep"
# # print(reviewer[mask])
#rint(df2)

#df2 = df2.pivot_table(index='name', columns='title', values='critic_icon')
#
#pd.to_pickle(df2, 'matrix.pkl')





