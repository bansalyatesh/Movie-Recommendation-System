import streamlit as st
import pickle


def recommend(movie):
   movie_index = movies_df[movies_df['title'] == movie].index[0]
   distances = similarity[movie_index]
   movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
   recommended_movies = []
   for i in movies_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
   return recommended_movies

movies_df = pickle.load(open('movies.pkl','rb'))
similarity =  pickle.load(open('similarity.pkl','rb'))
movies_list = movies_df['title'].values

st.title("Movie Recommender System")
selected_movie_name = st.selectbox("How would you like to be contacted",
                       movies_list)

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)