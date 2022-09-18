import streamlit as st
from predict import show_predict_page
from explore import show_explore_page

current_page=st.sidebar.selectbox("Explore or Predict", ("Explore", "Predict"))

if current_page == "Explore":
  show_explore_page()
elif current_page == "Predict":
  show_predict_page()