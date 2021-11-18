import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn import preprocessing


#cleaning data
reload_df = pd.read_csv('https://raw.githubusercontent.com/AnthonyLannes/Projet2/movies/Grouped_db_category_dummied.csv')
reload_df['Title']=reload_df['Title'].str.replace('&', 'et')
reload_df.drop(columns = ['Unnamed: 0.1', 'Unnamed: 0'], inplace = True) 
reload_df = reload_df.reset_index()
reload_df['lowerTitle'] = reload_df['Title'].str.lower()
reload_df['logVotes'] = reload_df['numVotes'].apply(np.log10)
reload_df['Année/1000'] = reload_df['startYear']/1000
reload_df.rename(columns = {'tconst' : 'movie_ID'}, inplace = True)

reload_df_cat_explode = reload_df['category'].str.split(", ").explode()
cat_explode = reload_df[['movie_ID', 'Title', 'directorsName', 'actorsName', 'startYear', 'decade',
       'country', 'set_countries', 'category', 'averageRating', 'numVotes']].merge(reload_df_cat_explode, left_index=True, right_index=True)

cat_explode_2 = pd.concat([cat_explode , cat_explode['category_y'].str.get_dummies()], 
          axis = 1)

cat_explode_3 = cat_explode_2.groupby(
    ['movie_ID', 'Title', 'directorsName', 'actorsName', 'startYear', 'decade',
       'country', 'set_countries', 'category_x', 'averageRating', 'numVotes'], as_index=False).agg(
    {'Animation':sum, 'Aventure':sum, 'Comedy':sum, 'Documentary':sum, 'Drama':sum,
       'Family':sum, 'Historique':sum, 'Horror':sum, 'Musique':sum, 'Polar':sum, 'Romance':sum, 'Sf':sum,
       'Sport':sum, 'War':sum, 'Western':sum}
)
       
cat_explode_3['startYear_normalized'] = preprocessing.normalize(cat_explode_3[['startYear']].values.reshape(-1, 1), axis=0)
cat_explode_3['averageRating_normalized'] = preprocessing.normalize(cat_explode_3[['averageRating']].values.reshape(-1, 1), axis=0)
cat_explode_3['numVotes_normalized'] = preprocessing.normalize(cat_explode_3[['numVotes']].values.reshape(-1, 1), axis=0)
cat_explode_3.rename(columns={'category_x': 'category'}, inplace=True)


#Be sure that the user can find their movie in our database. Askinf for them to enter keywords of their movie, then returning them all entries with their keywords.
#then asking for them to enter the movie id.
st.write("You liked a movie you've seen and want to see something similar ?")
my_title = -1
words = st.text_input("Please enter your title keywords")

split = words.lower().split()
regex_prep =  "".join(list(f"(?=.*{i})" for i in split))
df_liked_movie_reload = reload_df[reload_df['lowerTitle'].str.contains(r"^" + regex_prep)].reset_index()

st.write(df_liked_movie_reload[['movie_ID','Title', 'startYear', 'directorsName']])

#Making the user validate their movie.
if  df_liked_movie_reload.shape[0] == 0 :
    st.write("Sorry, no matches were found for your query. Please enter new keywords to find your movie, else enter 'quit'.")

if df_liked_movie_reload.shape[0] >= 1 :
    words = st.number_input('If your movie is in the abovementionned selection, please enter the corresponding movie_ID : ', value = -1)
    my_title = words
    #my_title = st.selectbox('If your movie is in the abovementionned selection, please pick the corresponding movie_ID one', list(i for i in df_liked_movie_reload['movie_ID']))
    df_liked_movie_reload = reload_df[reload_df['movie_ID'] == my_title]
    
st.write('Suggestion of movies according to the proposed title : ')
if my_title != -1 :

    #finalizing data to target with KNN

    df_tconst_film_a_trouver = pd.DataFrame(df_liked_movie_reload['movie_ID'])
    tconst_film_a_trouver = df_tconst_film_a_trouver['movie_ID'].values[0]
    film_a_comparer = cat_explode_3.loc[cat_explode_3['movie_ID'] == tconst_film_a_trouver]

    # KNN du film à comparer
    # Sélectionner les critères de comparaison
    colonnes = ['Animation', 'Aventure', 'Comedy', 'Documentary', 'Drama', 'Family',
                                'Historique', 'Horror', 'Musique', 'Polar', 'Romance', 'Sf', 'Sport',
                                'War', 'Western', 'startYear_normalized', 'averageRating_normalized',
                                'numVotes_normalized']

    # Entraîner le modèle
    nbrs = NearestNeighbors(n_neighbors=11).fit(cat_explode_3[colonnes])

    # Chercher les voisins les plus proches
    film_a_comparer = cat_explode_3.loc[cat_explode_3['movie_ID'] == tconst_film_a_trouver].reset_index()
    distance, indices = nbrs.kneighbors(film_a_comparer[colonnes])
    # df_indices = pd.DataFrame(indices)

    #Getting all recommended movies from KNN
    result = cat_explode_3.iloc[indices[0][1:]][['Title', 'directorsName', 'actorsName', 'startYear', 'country', 'category', 'averageRating', 'numVotes']]

    #Final result returned to user
    st.write("""Done ! Here are the movies we suggest you to watch based on your entry""")
    st.write(result[['Title',	'directorsName',	'actorsName',	'startYear', 'country', 'category',	'averageRating',	'numVotes']])
else :
    st.write("We cannot make suggestions. Please choose a movie.")





st.write('Movies suggestion with the same director(s) : ')
   
#Getting movie suggestion from the same director(s) than the entered movie.
#setting the df to have all the director(s) in separate rows.
if my_title != -1 :
    directors_to_explode = cat_explode_3.loc[cat_explode_3['movie_ID'] == my_title]
    directors_to_explode['directorsName'] = directors_to_explode['directorsName'].str.split(', ')
    directors_to_explode = directors_to_explode.explode('directorsName')

    #Creating a sampled dataframe for each movie directors if the number of their other movies is equal to or greater than 3. All df are stored in a dictionnary
    directors_movies = {}
    for i in directors_to_explode['directorsName'] : 
        directors_movies[i] = reload_df[(reload_df['movie_ID'] != my_title) & (reload_df['directorsName'].str.contains(i))]
        if len(directors_movies[i]) >= 3 :
          directors_movies[i] = directors_movies[i].sample(3)

    #Concatenating all the df into a single one
    final_directors_movies = pd.DataFrame()
    for directors in directors_movies :
        final_directors_movies = pd.concat([final_directors_movies, directors_movies[directors]])

    #Returning the suggestions. Inform the user if nothing is found.
    if len(final_directors_movies) == 0 :
        st.write("Our database does not have other movies from your movie director(s).")
    else : 
        final_directors_movies.drop_duplicates('movie_ID', inplace = True)
        st.write(final_directors_movies[['Title',	'directorsName',	'actorsName',	'startYear', 'country', 'category',	'averageRating', 'numVotes'	]])
else :
    st.write("We cannot make suggestions. Please choose a movie.")





st.write('Movies suggestion with the same actor(s) :')

#Getting movie suggestion with the same actor(s) than the entered movie.
#setting the df to have all the actor(s) in separate rows.
if my_title != -1 :
    actors_to_explode = cat_explode_3.loc[cat_explode_3['movie_ID'] == my_title]
    actors_to_explode['actorsName'] = actors_to_explode['actorsName'].str.split(', ')
    actor_other_movies = actors_to_explode.explode('actorsName')

    #Creating a sampled dataframe for each actors in the movies if the number of their other movies is equal to or greater than 3. All df are stored in a dictionnary
    actors_movies = {}
    for i in actor_other_movies['actorsName'] : 
        actors_movies[i]= reload_df[(reload_df['movie_ID'] != my_title) & (reload_df['actorsName'].str.contains(i))]
        if len(actors_movies[i]) >= 3 :
          actors_movies[i] = actors_movies[i].sample(3)

    #Concatenating all the df into a single one
    final_actors_movies = pd.DataFrame()
    for actors in actors_movies :
        final_actors_movies = pd.concat([final_actors_movies, actors_movies[actors]])

    #Returning the suggestions. Inform the user if nothing is found.
    if len(final_actors_movies) == 0 :
        st.write("Our database does not have other movies with your movie actor(s).")
    else : 
        final_actors_movies.drop_duplicates('movie_ID', inplace = True)
        st.write(final_actors_movies[['Title',	'directorsName',	'actorsName',	'startYear', 'country', 'category',	'averageRating', 'numVotes'	]])

else :
    st.write("We cannot make suggestions. Please choose a movie.")
