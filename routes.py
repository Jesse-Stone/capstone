from flask import Flask, render_template, redirect, url_for, request, flash
from forms import Movie
from functions import critics, ratings, all_data, create_critic_df, create_user_df, get_similarity, get_top_movies, consensus, four_of_five
import pandas as pd


app = Flask(__name__) #Flask Initialize
movies_list = [] #Empty global movie list that users select
empty = pd.DataFrame() #Used to display blank dataframes on first load

@app.route('/', methods = ['GET','POST'])
def home():
    df_display = pd.DataFrame(columns =["movie_pick","rating"]) #create dataframe to display
    df = ratings.reset_index()
    top_5000 = df.sort_values(by="rating_counts", ascending=False)
    #top_5000 = top_5000[:5000].sort_values(by = "title") #create the drop down list of 5,000 movies sorted alphabetically..use this instead?
    top_5000 = top_5000[:5000]
    movie_list = []
    for title in top_5000["title"]:
        movie_list.append(title)
    form= Movie()
    form.movie_pick.choices = [(movie, movie)for movie in movie_list]
    #if request.form.post['form'] =='submit':
    #if form.validate() and form.submit.data: #SUBMITTING MOVIES SECTION
    if form.submit.data:
        print("hi")
        #print(form.data["movie_pick"])
        if form.data["movie_pick"] in [dic['movie_pick'] for dic in movies_list]:
            flash("You have already selected this movie! Please choose another.")
            df_display = df_display.append(movies_list, ignore_index=True)
        if form.data["movie_pick"] not in [dic['movie_pick'] for dic in movies_list]:
            flash("Entered")
            movies_list.append(form.data)
            df_display = df_display.append(movies_list, ignore_index= True)
        df_display.columns = ["ignore1","ignore2","Movie", "Rating","dunno"]
        #print(df_display.loc[:,["Movie","Rating"]].to_dict('list'))
        return render_template("index.html", form=form,table = df_display.loc[:,["Movie","Rating"]].to_html(classes="table text-centered", index=False))
    elif form.analyze.data: #ANALYZE SECTION
        if len(movies_list) < 1: #Check for no entries
            flash("Please choose a film before analyzing")
            return render_template("index.html", form=form,
                                   table=empty.to_html(classes="table text-centered", index=False))
        else: #Analyze and produce results here
            df_display = df_display.append(movies_list, ignore_index=True)
            df_display.columns = ["ignore1", "ignore2", "Movie", "Rating", "dunno"]
            df_display = df_display.loc[:,["Movie","Rating"]]
            df_display.columns = ['title','critic_icon'] #changing column names to match functions
            df_display['critic_icon'] = df_display['critic_icon'].map({'Liked':1, 'Disliked':-1}) #changing values to match functions

            entry = (df_display.to_dict('list')) # converting df to dict to matching prebuilt functions

            #STARTING BRINGING IN THE FUNCTIONS FOR ANALYSIS

            critic_df = create_critic_df(all_data,entry)

            user_df = create_user_df(entry)

            similarities, df = get_similarity(critic_df,user_df[0],3) #THREE IS THE NUMBER OF CRITICS TO OUTPUT
            pivoted_critics = get_top_movies(similarities,critic_df)

            best_films, worst_films = consensus(pivoted_critics,user_df[1])
            best_films_4, worst_films_4 = four_of_five(pivoted_critics,user_df[1])


            return render_template("result.html", table = best_films.to_html(classes="table text-centered"),table2 = worst_films.to_html(classes="table text-centered"),table3 = best_films_4.to_html(classes="table text-centered"),table4 = worst_films_4.to_html(classes="table text-centered"), table5 = df.to_html(classes="table text-centered"))
    return render_template("index.html",form = form, table = empty.to_html(classes="table text-centered", index=False))




