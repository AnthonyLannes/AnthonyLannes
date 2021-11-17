import pandas as pd
import numpy as np
from seaborn import color_palette, heatmap, scatterplot, set
import matplotlib.pyplot as plt
import streamlit as st
#getting data
cars = pd.read_csv('https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv')
st.title("Starting data")
st.write(cars)
#making buttons to filter through continent

us_button =  st.sidebar.button( 'US')
europe_button = st.sidebar.button( 'Europe')
japan_button = st.sidebar.button( 'Japan')

no_us = st.sidebar.button( 'Japan and Europe')
no_eu = st.sidebar.button( 'Japan and US')
no_jp = st.sidebar.button( 'Europe and US')
default = st.sidebar.button( 'Default')

button = [us_button, europe_button, japan_button]
no_button = [no_us, no_eu, no_jp]
continent = list(cars['continent'].drop_duplicates())

    #setting the df cars to the chosen button
if default :
    cars
                             
for i in range(len(button)) :
    if button[i] :
        cars = cars[cars['continent'] == continent[i]]

for i in range(len(button)) :
    if no_button[i] :
        cars = cars[cars['continent'] != continent[i]]

#displyaing data
st.title("Statistical description of the data")
st.write(cars.describe())


#heatmap with diag removed
    #setting diag values to 0 to remove it from heatmap
st.title("Correlation heatmap of the data")
map = cars.corr()
for column in map.columns : 
  map.loc[map[column] == 1, column] = 0
    #heatmap
set(font_scale=1.3)
plt.figure(figsize = (18,12))
palette = color_palette(palette = 'coolwarm', as_cmap = True, )
viz_heatmap = heatmap(data = map, vmin = -1, vmax = 1, center = 0, cmap = palette, annot = True)
viz_heatmap.set_xticklabels(viz_heatmap.get_xmajorticklabels(), fontsize = 16)
viz_heatmap.set_yticklabels(viz_heatmap.get_ymajorticklabels(), fontsize = 16)

st.pyplot(viz_heatmap.figure)
st.write("""Overall, data show correlations. Especially, cylinders, cubic inches, horsepower
and weights are highly correalted, which seems logic. We can see that over the year, those characteristics
have decreased, which might be an indicator to an ecologic sensitivity.
All these data are also inversely correlated to mpg and time to 60 , which once again seems logic.
""") 



#Subplot of some relevant data
st.title("Scatterplots of data")
fig, ax = plt.subplots(3,3, figsize = (40,25))

scatterplot(ax = ax[0,0], data = cars , x = 'mpg', y = 'cubicinches', s = 150)
ax[0,0].set_xlabel(xlabel = 'MPG', size = 40)
ax[0,0].set_ylabel(ylabel = 'cubicinches', size = 40)
scatterplot(ax = ax[0,1], data = cars , x = 'mpg', y = 'hp', s = 150, color = 'orange')
ax[0,1].set_xlabel(xlabel = 'MPG', size = 40)
ax[0,1].set_ylabel(ylabel = 'HP', size = 40)
scatterplot(ax = ax[0,2], data = cars , x = 'mpg', y = 'weightlbs', s = 150, color = 'red')
ax[0,2].set_xlabel(xlabel = 'MPG', size = 40)
ax[0,2].set_ylabel(ylabel = 'weightlbs', size = 40)

scatterplot(ax = ax[1,0], data = cars , x = 'cubicinches', y = 'hp', s = 150)
ax[1,0].set_xlabel(xlabel = 'Cubicinches', size = 40)
ax[1,0].set_ylabel(ylabel = 'HP', size = 40)
scatterplot(ax = ax[1,1], data = cars , x = 'cubicinches', y = 'weightlbs', s = 150, color = 'orange')
ax[1,1].set_xlabel(xlabel = 'Cubicinches', size = 40)
ax[1,1].set_ylabel(ylabel = 'weightlbs', size = 40)
scatterplot(ax = ax[1,2], data = cars , x = 'hp', y = 'weightlbs', s = 150, color = 'red')
ax[1,2].set_xlabel(xlabel = 'HP', size = 40)
ax[1,2].set_ylabel(ylabel = 'weightlbs', size = 40)

scatterplot(ax = ax[2,0], data = cars , x = 'time-to-60', y = 'cubicinches', s = 150)
ax[2,0].set_xlabel(xlabel = 'time-to-60', size = 40)
ax[2,0].set_ylabel(ylabel = 'cubicinches', size = 40)
scatterplot(ax = ax[2,1], data = cars , x = 'time-to-60', y = 'hp', s = 150, color = 'orange')
ax[2,1].set_xlabel(xlabel = 'time-to-60', size = 40)
ax[2,1].set_ylabel(ylabel = 'HP', size = 40)
scatterplot(ax = ax[2,2], data = cars , x = 'time-to-60', y = 'weightlbs', s = 150, color = 'red')
ax[2,2].set_xlabel(xlabel = 'time-to-60', size = 40)
ax[2,2].set_ylabel(ylabel = 'weightlbs', size = 40)
plt.subplots_adjust(hspace = 0.4, wspace = 0.4)

#customizing labels
plt.draw()
for i in range(3):
  for j in range(3):
    ax[i,j].set_xticklabels(ax[i,j].get_xticklabels(), size = 30)
    ax[i,j].set_yticklabels(ax[i,j].get_yticklabels(), size = 30)

st.pyplot(fig.figure)
st.write("""This just shows you scatterplots of the correlation heatmap above.""") 
