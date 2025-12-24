import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Page config
st.set_page_config(page_title="Book Recommender", layout="wide")

# Horizontal navbar
selected = option_menu(
    menu_title=None,
    options=["Top 50 Books", "Recommend"],
    icons=["book", "search"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#00a65a"},
        "nav-link": {"color": "white", "font-weight": "bold", "font-size": "18px"},
        "nav-link-selected": {"background-color": "#007144"},
    }
)

if selected == "Top 50 Books":
    st.markdown("### 🎯 Top 50 Books")
    cols = st.columns(4)
    for i in range(len(popular_df)):
        with cols[i % 4]:
            st.image(popular_df['Image-URL-M'].iloc[i], width=150)
            st.markdown(f"**{popular_df['Book-Title'].iloc[i]}**")
            st.caption(f"Author: {popular_df['Book-Author'].iloc[i]}")
            st.caption(f"Votes: {popular_df['num_ratings'].iloc[i]}")
            st.caption(f"Rating: {popular_df['avg_rating'].iloc[i]:.2f}")

elif selected == "Recommend":
    st.markdown("### 🔍 Recommend Books Based on a Title")

    # Dropdown of all book titles
    book_list = pt.index.values
    selected_book = st.selectbox("Select a Book Title:", book_list)

    if st.button("Recommend"):
        index = np.where(pt.index == selected_book)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        st.markdown("### ✅ Recommendations:")
        cols = st.columns(4)

        for idx, i in enumerate(similar_items):
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            book_title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            img_url = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

            with cols[idx % 4]:
                st.image(img_url, width=150)
                st.markdown(f"**{book_title}**")
                st.caption(f"Author: {author}")
