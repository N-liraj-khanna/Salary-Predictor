import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_countries(countries, cutoff):
    shorterned_countries={}
    for i in range(len(countries)):
        if countries[countries.index[i]]>=cutoff:
            shorterned_countries[countries.index[i]]=countries.index[i]
        else:
            shorterned_countries[countries.index[i]]="Other"
    return shorterned_countries

def clean_years(x):
    if x == 'Less than 1 year':
        return float(0.5)
    else:
        return float(x)

def clean_education(x):
    if 'Master’s degree' in x:
        return 'Master’s degree'
    elif 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    elif 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post Grad'
    else:
        return 'Less than a Bachelor’s'

@st.cache
def load_data():
  df=pd.read_csv("./survey_results_public.csv")

  df=df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
  df=df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

  df=df[df["Salary"].notnull()]
  df=df.dropna()

  df=df[df["Employment"]=="Employed, full-time"]
  df=df.drop("Employment", axis=1)

  countries = shorten_countries(df.Country.value_counts(), 400)
  df["Country"]=df["Country"].map(countries)
  
  df=df[df["Salary"]<=25000]
  df=df[df["Salary"]>=10000]
  df=df[df["Country"]!="Other"]

  df["YearsCodePro"]=df.YearsCodePro.apply(clean_years)

  df["EdLevel"]=df.EdLevel.apply(clean_education)

  return df



df=load_data()

def show_explore_page():
  st.title("# Explore Software Developer Salaries")
  st.write(""" #### A Survery Made by StackOverflow of Software Developer's salaries 2022 """)
  
  data = df["Country"].value_counts()

  fig1, ax1 = plt.subplots()
  ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
  ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

  st.write("""#### Number of Data from different countries""")

  st.pyplot(fig1)

  st.write(
    """
  #### Mean Salary Based On Country
  """
  )

  data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
  st.bar_chart(data)

  st.write(
    """
  #### Mean Salary Based On Experience
  """
  )

  data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
  st.line_chart(data)