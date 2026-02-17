import streamlit as st

st.set_page_config(page_title="BCD — Our Team", page_icon="👥", layout="centered")
st.sidebar.title("📚 Navegação")
st.title("👥 Our Team")
st.write("Quem construiu o BCD.")

team = [
    {"name": "Guilherme Pereira", "photo": "images/guilherme.jpg"},
    {"name": "Diogo Casquinha",   "photo": "images/diogo.jpg"},
    {"name": "Gabriel Afonso",    "photo": "images/gabriel.jpg"},
    {"name": "Vicente Soares",    "photo": "images/vicente.jpg"},
]

cols = st.columns(len(team))

for col, member in zip(cols, team):
    with col:
        st.image(member["photo"], width=150)
        st.subheader(member["name"])