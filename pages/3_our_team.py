import streamlit as st

st.set_page_config(page_title="BCD — Our Team", page_icon="👥", layout="centered")
st.sidebar.title("📚 Navegação")
st.title("👥 Our Team")
st.write("Quem construiu o BCD — e o que cada um fez no projeto.")

team = [
    {"name": "Nome 1", "role": "ML / YOLO", "bio": "Treino do modelo, dataset, métricas e validação."},
    {"name": "Nome 2", "role": "App / Streamlit", "bio": "Frontend, UX, upload, outputs e deploy."},
    {"name": "Nome 3", "role": "Documentação", "bio": "README, relatório, figuras e reprodutibilidade."},
]

cols = st.columns(3)
for i, member in enumerate(team):
    with cols[i % 3]:
        st.subheader(member["name"])
        st.caption(member["role"])
        st.write(member["bio"])
