import pandas as pd
import numpy as np
import scipy.spatial as sp

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity

from scipy.sparse import csr_matrix

from sklearn.neighbors import KNeighborsClassifier

#Read in the scaled data
df = pd.read_pickle('scaled_cleaned.pkl')

df['critic_icon'] = df['critic_icon'].replace(['fresh','rotten'], [1,0])
print(df.head(100))




#Create the matrix

# df2 = df.pivot_table(index='name', columns='title', values='scaled_rating')
# pd.to_pickle(df2,'review_matrix.pkl')

# df = pd.read_pickle('review_matrix.pkl')
#
# forrest_gump_ratings = df['Forrest Gump']
#
# print(forrest_gump_ratings.head(400))

#print(df.groupby('title')['rating'].count().sort_values(ascending=False).head())

#Create a ratings count DF for movies

# ratings = pd.DataFrame(df.groupby('title')['scaled_rating'].mean())
#
# ratings['rating_counts'] = pd.DataFrame(df.groupby('title')['rating'].count())
#
# pd.to_pickle(ratings,'ratings.pkl')

#Create a ratings count DF for critics

critic_ratings = pd.DataFrame(df.groupby('name')['critic_icon'].mean())
#
critic_ratings['rating_counts'] = pd.DataFrame(df.groupby('name')['critic_icon'].count())

#pd.to_pickle(critic_ratings,'critic_ratings_fresh_rotten.pkl')


movie_ratings = pd.read_pickle('ratings.pkl')
#critics = pd.read_pickle('review_matrix.pkl')
#critics = critics.fillna(0) ## all movies not rated have a zero score instead of NaN
critics = pd.read_pickle('review_matrix_with_zeroes.pkl')
critic_ratings = pd.read_pickle('critic_ratings.pkl')

#print(movie_ratings)

critic_matrix = csr_matrix(critics.values)

df3 = pd.read_pickle('review_matrix_with_zeroes.pkl')
a = np.zeros(shape=(1,len(df3.columns)))
new_user = pd.DataFrame(a,columns=df3.columns,index = np.arange(1,2))
new_user.index.name = "name"
new_user["A Quiet Place"] = 1
new_user["Halloween"] = 1
new_user["The Drop"] = 5
new_user["Eden"] = 1

new_user = new_user.astype(float)

test_matrix = csr_matrix(new_user.values)

x = cosine_similarity(test_matrix, critic_matrix)

# print(x)
#
# print(np.argmax(x))
#
# print(critic_matrix[1674])
# print(critics.iloc[1674,:])


# # print(test_matrix)
# # print(critic_matrix[184])
# print(x.argsort()[-3:][::-1])


