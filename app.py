import pickle
import streamlit as st
import requests
import os




# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['id']  # Assuming 'id' is the correct column name
        recommended_movie_names.append(movies.iloc[i[0]]['title'])
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI setup
st.header('🎬 Movie Recommender System')
# Custom CSS for ambient background and styling
st.markdown(
    """
    <style>
        body {
            background-color: #2e2e2e;  /* Test color: Dark grey */
            color: #f8f8f8;
            font-family: 'Arial', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True
)








# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies = pickle.load(open(os.path.join(BASE_DIR, 'movie_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))

# Dropdown to select movie
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations when button clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

# Footer: Add text about you
st.markdown(
    """
    <style>
        /* Full-page background fix */
        html, body, [data-testid="stApp"] {
            height: 100%;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            background-attachment: fixed;
            background-size: cover;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Header styling (title) */
        h1 {
            color: #ffffff;
            text-shadow: 1px 1px 2px #00000080;
        }

        /* Button and input improvements */
        .stTextInput>div>div>input, .stButton>button {
            background-color: #1f2937;
            color: white;
            border-radius: 8px;
            border: 1px solid #4b5563;
            padding: 8px;
        }

        .stButton>button:hover {
            border: 1px solid #93c5fd;
            background-color: #2563eb;
            color: white;
        }

        /* Footer Styling */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            color: #dddddd;
            text-align: center;
            padding: 12px;
            font-size: 0.9rem;
        }

        .footer a {
            color: #60a5fa;
            text-decoration: none;
            margin: 0 10px;
        }

        .footer a:hover {
            text-decoration: underline;
        }
    </style>

    <div class="footer">
        <p>Created by <strong>God Aaditya</strong><br>
        I am Mr.nobody. A man who exists and does not exist at the same time. Feel free to connect with me!</p>
        <p>
            <a href="https://www.facebook.com/your_facebook_username" target="_blank">Facebook</a> |
            <a href="https://www.instagram.com/your_instagram_username" target="_blank">Instagram</a> |
        </p>
    </div>
    """,
    unsafe_allow_html=True
)