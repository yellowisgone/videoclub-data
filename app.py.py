import pandas as pd
import streamlit as st

st.set_page_config(page_title="Vidéoclub", page_icon="🎬")

# 🔗 Lien vers ton Google Sheets publié en CSV
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSrBDxMN6CGh5ROmH0pXnJzbA76EqPulrda5W_WFFkKCL8ct13dSAoHpvZTtrV-2LrOhD_-ehm5XeWW/pub?output=csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

films = load_data(sheet_url)

st.title("🎬 Sélecteur de films du vidéoclub")

# --- 1️⃣ Filtres interactifs ---

# Genre : récupérer tous les genres possibles même si multiples
tous_genres = set()
for g in films['Genre'].dropna():
    for genre in str(g).split(','):
        tous_genres.add(genre.strip())
tous_genres = sorted(list(tous_genres))
choix_genres = st.multiselect("Choisir le(s) genre(s)", tous_genres)

# Title : recherche textuelle (partielle)
title_input = st.text_input("Chercher par titre (ou mots-clés)")

# Year
year_min = int(films['Year'].min())
year_max = int(films['Year'].max())
choix_year = st.slider("Année de sortie", year_min, year_max, (year_min, year_max))

# Length (min)
length_min = int(films['Length (min)'].min())
length_max = int(films['Length (min)'].max())
choix_length = st.slider("Durée (minutes)", length_min, length_max, (80, 120))

# Language
toutes_languages = sorted(films['Language'].dropna().unique())
choix_languages = st.multiselect("Choisir la/les langue(s)", toutes_languages)

# Public
tous_publics = sorted(films['Public'].dropna().unique())
choix_public = st.multiselect("Choisir le type de public", tous_publics)

# Directed by
tous_realisateurs = sorted(films['Directed by'].dropna().unique())
choix_realisateurs = st.multiselect("Choisir le(s) réalisateur(s)", tous_realisateurs)

# --- 2️⃣ Filtrage dynamique ---
resultats = films.copy()

# Filtre par genre
if choix_genres:
    mask_genre = resultats['Genre'].apply(lambda g: any(genre.strip() in str(g) for genre in choix_genres))
    resultats = resultats[mask_genre]

# Filtre par titre (texte partiel)
if title_input:
    mask_title = resultats['Title'].str.contains(title_input, case=False, na=False)
    resultats = resultats[mask_title]

# Filtre par année
resultats = resultats[(resultats['Year'] >= choix_year[0]) & (resultats['Year'] <= choix_year[1])]

# Filtre par durée
resultats = resultats[(resultats['Length (min)'] >= choix_length[0]) & (resultats['Length (min)'] <= choix_length[1])]

# Filtre par langue
if choix_languages:
    resultats = resultats[resultats['Language'].isin(choix_languages)]

# Filtre par public
if choix_public:
    resultats = resultats[resultats['Public'].isin(choix_public)]

# Filtre par réalisateur
if choix_realisateurs:
    resultats = resultats[resultats['Directed by'].isin(choix_realisateurs)]

# Tri par Note si disponible
if 'Note' in resultats.columns:
    resultats = resultats.sort_values('Note', ascending=False)

# --- 3️⃣ Affichage des résultats ---
st.subheader("🎥 Films trouvés :")
st.dataframe(resultats)

st.caption("Les données proviennent directement de ton Google Sheets publié en CSV.")



