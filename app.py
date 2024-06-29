import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    api_key = "9cdc0aef12fbcdb8b8dc0d3cff04c7b8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
   movie_index = movies_df[movies_df['title'] == movie].index[0]
   distances = similarity[movie_index]
   movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
   recommended_movies = []
   recommended_movies_poster = []
   for i in movies_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies_df.iloc[i[0]].id))
   return recommended_movies,recommended_movies_poster

movies_df = pickle.load(open('movies.pkl','rb'))
similarity =  pickle.load(open('similarity.pkl','rb'))
movies_list = movies_df['title'].values

st.title("Movie Recommender System")
selected_movie_name = st.selectbox('''Which Movie Reommendation you want to see?
                                   ''',
                       movies_list)

st.markdown("""
    <style>
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        color: #2C3E50;
        margin-top: 10px;
    }
    .movie-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        transition: transform 0.2s;
        margin: 0 10px; /* Add horizontal margin for spacing */
    }
    .movie-container:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .movie-poster {
        border-radius: 10px;
        width: 150px;
    }
    </style>
    """, unsafe_allow_html=True)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5,gap='large')  # Add gap between columns

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f'''
                <div class="movie-container">
                    <img src="{poster}" class="movie-poster">
                    <div class="movie-title">{name}</div>
                </div>
                ''', unsafe_allow_html=True)
