import pandas as pd
import numpy as np
import scipy.spatial as sp

from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)

critics = pd.read_pickle('critic_ratings_fresh_rotten.pkl')
ratings = pd.read_pickle('ratings_fresh_rotten.pkl')
all_data = pd.read_pickle('scaled_cleaned.pkl')

all_data['critic_icon'] = all_data['critic_icon'].replace(['fresh','rotten'], [2,1])

#Create the matrix

df2 = all_data.pivot_table(index='name', columns='title', values='critic_icon').fillna(0)

critic_matrix = csr_matrix(df2.values)

a = np.zeros(shape=(1,len(df2.columns)))
new_user = pd.DataFrame(a,columns=df2.columns,index = np.arange(1,2))
new_user.index.name = "name"
new_user["A Quiet Place"] = 2
new_user["Halloween"] = 1
new_user["The Drop"] = 2
new_user["Eden"] = 1

new_user = new_user.astype(float)

test_matrix = csr_matrix(new_user.values)

x = cosine_similarity(test_matrix, critic_matrix)

print(np.argmax(x))

print(critic_matrix[1263])
print(critics.iloc[1263,:])
