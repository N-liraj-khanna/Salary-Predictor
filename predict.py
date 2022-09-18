import pickle
import numpy as np
import streamlit as st

def load_model():
  with open("./saved_steps.pkl", "rb") as file:
    data = pickle.load(file)
  return data

data=load_model()

regressor = data["model"]
le_education = data["le_education"]
le_country = data["le_country"]

def show_predict_page():
  st.title("# Software Developer Salary Prediction")

  st.write(""" #### Give us some information to predict your salary """)

  countries = (
    "India",
    "Brazil",
    "Italy",
    "Spain",
    "Poland",
    "Russian Federation",
    "France",
    "Germany",
    "United Kingdom of Great Britain and Northern Ireland",
    "United States of America",
    "Switzerland",
    "Canada",
    "Australia",
    "Sweden",
    "Netherlands",
  )

  education = (
    "Bachelor’s degree",
    "Less than a Bachelor’s",
    "Master’s degree",
    "Post Grad",      
  )

  country=st.selectbox("Country", countries)
  education=st.selectbox("Education Level", education)
  experience=st.slider("Years of experience", 0, 50, 3)

  predict=st.button("Predict")

  if predict:
    X=np.array([[country, education, experience]])
    X[:,0]=le_country.transform(X[:,0])
    X[:,1]=le_education.transform(X[:,1])
    X=X.astype(float)

    predicted_value = regressor.predict(X)
    if len(predicted_value)!=0:
      st.write(f"## Predicted Salary is ${predicted_value[0]:.02f}") 
    else:
      st.header(" Something went wrong, Please try again later!")
