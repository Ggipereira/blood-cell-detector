import streamlit as st

st.set_page_config(page_title="Video-Demo", page_icon="📹", layout="centered")
st.sidebar.title("📚 Navegação")
st.title("Video Demo📹")
st.write( "Click the video and see how you can use our model"
)


video_file = open("myvideo.mp4", "rb")
video_bytes = video_file.read()

st.video(video_bytes)