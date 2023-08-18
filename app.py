import streamlit as st
import pickle
import pandas as pd
import requests


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[-1])[1:6]
    rec_movies = []
    rec_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        rec_movies.append(movies.iloc[i[0]].title)
        rec_poster.append(fetch_poster(movie_id))
    return rec_movies, rec_poster


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7a711fb85cd22143ae93fd5047d5b39e'.format(movie_id))
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # Return a default or placeholder image URL
        return "https://example.com/placeholder.jpg"


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title('movie recommender sytem')
selected_movie_name = st.selectbox('type your movie name:',
                                   movies['title'].values)
if st.button('recommend'):
    name, posters = recommend(selected_movie_name)
    with st.container():
        cols = st.columns(3)
        for i, j in zip(cols, range(3)):
            i.header(name[j])
            i.image(posters[j])
    with st.container():
        cols = st.columns(2)
        for i, j in zip(cols, range(3, 5)):
            i.header(name[j])
            i.image(posters[j])
