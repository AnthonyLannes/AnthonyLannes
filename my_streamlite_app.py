import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px


st.title('Hello Wilders, welcome to my application!')

name = st.text_input("Please give me your name :")
name_length = len(name)
st.write("Your name has ",name_length,"characters")

st.write('I enjoy to discover streamlit possibilities')

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/weather2019.csv"
df_weather = pd.read_csv(link)

viz_correlation = sns.heatmap(df_weather.corr(), center=0, cmap = sns.color_palette("vlag", as_cmap=True))

st.pyplot(viz_correlation.figure)


fig = px.scatter(data_frame = df_weather, 
                 x= "DATE", 
                 y="MAX_TEMPERATURE_C", 
                 color = 'OPINION',
                 color_discrete_map = {'very bad' : 'red', 'bad' : 'orange', 'not good not bad' : 'yellow', 'good' : 'limegreen', 'very good' : 'darkgreen'},
                 title = 'Max temperatures over the year weighted by opinion',
                 labels = { 'DATE' : 'Day of the year', 'MAX_TEMPERATURE_C' : 'Max Temperature (°C)'})

fig.update_layout(title_x=0.45)
st.plotly_chart(fig)

#to save requirements.txt, go to terminal of p2 in anaconda3, and enter 'pipreqs [entire path to directory containing py script]'
