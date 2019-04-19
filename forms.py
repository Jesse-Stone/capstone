from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class Movie(FlaskForm):
    movie_pick = SelectField('movies', choices =[])
    rating = SelectField('rating', choices = [('Liked','Liked'),('Disliked','Disliked')])
    submit = SubmitField('submit')
    analyze = SubmitField('ANALYZE')



