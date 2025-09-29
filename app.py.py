import streamlit as st
import pandas as pd

st.set_page_config(page_title="🎬 Base de données des films", layout="wide")

# 🔗 URL vers ton Google Sheet (version CSV publique)
sheet_url = "https://docs.google.com/spreadsheets/d/TON_ID/export?format=csv"

# ⬇️ Fonction pour charger les données
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# 🔄 Bouton pour recharger (vide le cache)
if st.button("🔄 Recharger la base"):
    st.cache_data.clear()

# Chargement des données
films = load_data(sheet_url)

st.title("🎬 Base de données des films")

# 📝 Filtres
all_titles = ["Tous"] + sorted(films["Title"].unique())
selected_title = st.selectbox("🎞️ Titre :", all_titles)

all_genres = ["Tous"] + sorted({g.strip() for genre in films["Genre"].dropna() for g in genre.split(",")})
selected_genre = st.selectbox("🎭 Genre :", all_genres)

min_len, max_len = int(films["Length (min)"].min()), int(films["Length (min)"].max())
length = st.slider("⏱️ Durée (min) :", min_len, max_len, (min_len, max_len))

years = ["Tous"] + sorted(films["Year"].unique())
selected_year = st.selectbox("📅 Année :", years)

languages = ["Tous"] + sorted(films["Language"].unique())
selected_language = st.selectbox("🌍 Langue :", languages)

publics = ["Tous"] + sorted(films["Public"].unique())
selected_public = st.selectbox("👥 Public :", publics)

directors = ["Tous"] + sorted(films["Directed by"].unique())
selected_director = st.selectbox("🎬 Réalisateur :", directors)

# 🪄 Filtrage
filtered = films.copy()

if selected_title != "Tous":
    filtered = filtered[filtered["Title"] == selected_title]

if selected_genre != "Tous":
    filtered = filtered[filtered["Genre"].str.contains(selected_genre, case=False, na=False)]

filtered = filtered[
    (filtered["Length (min)"] >= length[0]) &
    (filtered["Length (min)"] <= length[1])
]

if selected_year != "Tous":
    filtered = filtered[filtered["Year"] == selected_year]

if selected_language != "Tous":
    filtered = filtered[filtered["Language"] == selected_language]

if selected_public != "Tous":
    filtered = filtered[filtered["Public"] == selected_public]

if selected_director != "Tous":
    filtered = filtered[filtered["Directed by"] == selected_director]

# 📊 Affichage
st.dataframe(filtered, use_container_width=True)
st.write(f"🎯 {len(filtered)} film(s) trouvé(s)")
