import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="Movie Recommender",
    layout="wide"
)

movies_df = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

API_KEY = "3e64bc3e"


def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data.get("Poster")

    return "https://placehold.co/300x450?text=No+Poster"


def recommend(movie_name):
    movie_index = movies_df[movies_df["title"] == movie_name].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_title = movies_df.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters


st.sidebar.title("About Project")
st.sidebar.write("""
This is a content-based movie recommendation system.

It recommends similar movies using movie tags and cosine similarity.
""")

st.title("🎬 Movie Recommendation System")
st.write("Select a movie and get similar movie recommendations.")

movie_list = movies_df["title"].values

selected_movie = st.selectbox(
    "Search or select a movie",
    movie_list
)

if st.button("Recommend"):
    try:
        names, posters = recommend(selected_movie)

        st.subheader("Recommended Movies")

        cols = st.columns(5)

        for index, col in enumerate(cols):
            with col:
                st.image(posters[index], use_container_width=True)
                st.markdown(f"**{names[index]}**")

    except Exception as e:
        st.error("Something went wrong. Try another movie.")