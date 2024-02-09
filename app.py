import streamlit as st
import pickle
import os
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b32c9af0cd5c6993d5f7e83a3673f92a&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + str(data['poster_path'])

# Get the absolute path to the pickle directory
pickle_dir = os.path.join(os.path.dirname(__file__), 'pickle')

# Construct the file path to movie_dict.pkl
movie_dict_path = os.path.join(pickle_dir, 'movie_dict.pkl')

# Construct the file path to movie_dict.pkl
similarity_path = os.path.join(pickle_dir, 'similarity.pkl')

movies_dict = pickle.load(open(movie_dict_path,'rb'))
df = pd.DataFrame(movies_dict)
similarity = pickle.load(open(similarity_path,'rb'))

def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = df.iloc[i[0]].movie_id
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies.append(df.iloc[i[0]].title)
    return recommend_movies , recommend_movies_poster

st.title("Movie Recommender System")
option = st.selectbox(
    "Select Movie Name",
    df['title'].values
)
if st.button('Recommend'):
    recommendations,posters = recommend(option)
    # for i in recommendations:
    #     st.write(i)
    col1 , col2 , col3 , col4 , col5 = st.columns(5)
    with col1:
        st.write(recommendations[0])
        st.image(posters[0])
    with col2:
        st.write(recommendations[1])
        st.image(posters[1])
    with col3:
        st.write(recommendations[2])
        st.image(posters[2])
    with col4:
        st.write(recommendations[3])
        st.image(posters[3])
    with col5:
        st.write(recommendations[4])
        st.image(posters[4])