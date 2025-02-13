import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
API_KEY = os.getenv("API_KEY")

st.title("Movie recommendation")

movies_db = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_db)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        data = response.json()
        
        if "poster_path" in data and data["poster_path"]:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            return "No poster available"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return None  # Return None in case of failure

# Example Usage

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movies_id = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    mv = []
    mv_poster = []
    
    for i in movies_id:
        mv_id = movies.iloc[i[0]].id
        mv.append(movies.iloc[i[0]].title)
        mv_poster.append(fetch_poster(mv_id))  # Fetch correct poster

    return list(zip(mv, mv_poster))  # Return list of tuples (title, poster_url)

selected_movie = st.selectbox(
    'Which number do you like best?',
    movies['title'] )

if st.button('Recommend'):
    movies = recommend(selected_movie)  
    
    cols = st.columns(5)  # Display in 5 columns

    for i, (mv, mv_poster) in enumerate(movies):
        with cols[i % 5]:  # Arrange in columns
            st.text(mv)  
            if mv_poster:
                st.image(mv_poster, use_container_width=True)
            else: 
                st.text(mv_poster)