import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

#Used to show more output to the terminal for Pandas
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)

def load_data():
    """Loads in all the Dataframes from the pickle files that
    have been webscraped and cleaned"""
    critics = pd.read_pickle('data/critic_ratings_fresh_rotten.pkl')
    ratings = pd.read_pickle('data/ratings_fresh_rotten.pkl')
    all_data = pd.read_pickle('data/scaled_cleaned.pkl')
    return critics,ratings,all_data

critics,ratings,all_data = load_data() #Load the Data

all_data['critic_icon'] = all_data['critic_icon'].replace(['fresh','rotten'], [1,-1]) ## Leaving out of function to easily adjust scores from 1/-1 to something else if needed for cosine similarity results


def user_reviews(): #DEPRECATED/USED FOR TERMINAL TESTING ONLY
    """Gets user input for num movies"""
    name = input("What is your name?")
    num = int(input("How many movies to review?: "))
    movies_list = []
    score_list = []
    for i in range(num):
        movie = input("Name a Movie: ")
        score = input("Score :")
        score = int(score)
        movies_list.append(movie)
        score_list.append(score)
    return movies_list, score_list


def create_review_entry(movies_list,score_list): #DEPRECATED USED FOR TERMINAL TESTING ONLY
    """Creates the Dataframe for the user's reviews, pivoted with movies on x axis"""

    new_user= {
        'title': movies_list,
        'critic_icon': score_list
    }
    return new_user


def create_critic_df(df,entry):
    """Takes the movie titles listed by the user and created by the create_movie_list() function, and returns a dataframe
    the will consist of all reviews for critics that have been invovled in at least ONE to ALL of the titles suggested by the user"""
    mask = df["title"].isin(entry['title'])
    movies_match = df[mask].loc[:,["name","critic_icon","title"]]
    df = movies_match.pivot_table(index='name', columns='title', values='critic_icon').fillna(0)
    return df


def create_user_df(dict):
    """Takes the entry and turns it into a pivoted Dataframe"""
    df = pd.DataFrame(dict)
    #df = df.set_index("name")
    df = df.pivot_table(columns='title', values='critic_icon')
    movie_list = []
    for movie in df.columns:
        movie_list.append(movie)
    return df, movie_list


def get_similarity(df1,df2,number_of_critics):
    """Computes the indices with the highest cosine similarity, returns their indexes, and searches the dataframe for
    that critic's reviews and outputs them"""
    similarities = cosine_similarity(df1, df2)
    similarities = similarities.flatten() #used so the argsort can work properly
    critics_list = similarities.argsort()[-number_of_critics:]
    flipped  = critics_list[::-1] # get the list in the right order
    sim_list = []
    scores = []
    for i in flipped:
        #print(similarities[i])
        sim_list.append(i)
    #print("\nTop {} critics with similar taste\n".format(number_of_critics))
    for critic in flipped:
        scores.append(similarities[critic]*100)
        #print("Strength Score: ",100*(similarities[critic]),"\n",df1.iloc[critic, :])
    critic_df = pd.DataFrame()
    for critic in flipped:
        x = df1.iloc[critic, :]
        critic_df = critic_df.append(x)
    critic_df["Similarity Score"] = scores
    critic_df = critic_df.replace({0:"No Review", 1: "Liked", -1: "Didn't Like"})
    return flipped, critic_df

def critic_strength_scores(flipped):
    """take the df outputted by similarities and return critics with their strength score"""
    pass


def get_top_movies(critic_indices,df):
    """Pass a list of indexes"""
    top_5_critics = df.iloc[critic_indices,:]
    critic_list = top_5_critics.reset_index()["name"]
    mask = all_data['name'].isin(critic_list)
    to_pivot = all_data[mask]
    to_pivot = to_pivot.rename(index=str, columns={"title": "Title", "name": "Critic Name"})
    pivoted_critics = to_pivot.pivot_table(index='Critic Name', columns='Title', values='scaled_rating')
    # pivoted_critics = pivoted_critics.drop(col, axis=1, inplace=1)
    return pivoted_critics

def consensus(pivoted_critics,entry):
    """n-1 thresholds to get different movie results for critics who havent seen every movie"""
    all_reviewed = pivoted_critics.dropna(axis=1)
    x = all_reviewed.T # puts movies on the X axis
    no_zeros = x[~x.eq(0.0).any(1)] #drops any movie with a 0.0 rating i.e no review
    all_reviewed = no_zeros.T #transposes back to normal
    #one_nan = pivoted_critics.dropna(thresh=len(pivoted_critics) - 1, axis=1).fillna(0) #might need code later
    #two_nan = pivoted_critics.dropna(thresh=len(pivoted_critics) - 2, axis=1).fillna(0)#might need code later
    s_consensus = all_reviewed.sum().sort_values(ascending=False, inplace=False)
    consensus_best = all_reviewed[s_consensus.index[:5]]
    consensus_worst = all_reviewed[s_consensus.index[-5:]]
    consensus_worst = consensus_worst.iloc[:,::-1]
    movies = entry[1] #gets the titles from the function return
    select_best = [x for x in consensus_best.columns if x not in movies]
    select_worst = [x for x in consensus_worst.columns if x not in movies]
    return consensus_best.loc[:, select_best],consensus_worst.loc[:, select_worst]

def four_of_five(pivoted_critics,entry):
    """n-1 thresholds to get different movie results for critics who havent seen every movie"""
    one_nan = pivoted_critics.dropna(thresh=len(pivoted_critics) - 1, axis=1).fillna(0.0)
    one_nan = one_nan.loc[:,(one_nan == 0.00).any()] #THIS WAS THE SHIT TO GET AT LEAST ONE ZERO I HOPE
    s_1 = one_nan.sum().sort_values(ascending=False, inplace=False)
    four_of_five_worst = one_nan[s_1.index[-5:]]
    four_of_five_best = one_nan[s_1.index[:5]]
    four_of_five_worst = four_of_five_worst.iloc[:,::-1]
    movies = entry[1]
    select_best = [x for x in four_of_five_best.columns if x not in movies]
    select_worst = [x for x in four_of_five_worst.columns if x not in movies]
    return four_of_five_best.loc[:,select_best],four_of_five_worst.loc[:,select_worst]


