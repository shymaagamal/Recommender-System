# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Import Important package

# %%
import pandas as pd
import numpy as np
from sklearn.utils import shuffle


# %%
movies=pd.read_csv("movies.csv")
movies.head(2)


# %%
rating=pd.read_csv("ratings.csv")
rating.head(2)


# %%
movies=movies.drop(['genres'],axis=1)
rating=rating.drop(['timestamp'],axis=1)
rating=shuffle(rating)
movies=shuffle(movies)

rating.head(2)

# %% [markdown]
# # Merge Data

# %%
movie_data = pd.merge(rating, movies, on='movieId')
movie_data.head()

# %% [markdown]
# # Explor Data

# %%
# Calculate mean rating of all movies
movie_data.groupby('title')['rating'].mean().sort_values(ascending=False).head()


# %%
movie_data.groupby('title')['rating'].count().sort_values(ascending=False).head()


# %%
ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
ratings_mean_count.dropna(inplace=True)
ratings_mean_count.sort_values("rating_counts",ascending=False).head(10)

# %% [markdown]
# # Generate data matrix between users and movies and value is rating

# %%
user_movie_rating = movie_data.pivot_table(index='userId', columns='title', values='rating')[:200]
print(user_movie_rating.shape)
user_movie_rating.head(3)

# %% [markdown]
# # Replace NAN Value with zero

# %%
user_movie_rating.replace(np.nan, 0,inplace=True)
user_movie_rating.head(2)

# %% [markdown]
# # Cosin similarit Function

# %%
def Cosin_Similarity(data_Matrix,film_name):
    similarty_df = pd.DataFrame(columns=['userId', 'Cosin_similarty'])
    film=data_Matrix[film_name]
    for i in data_Matrix:
        dot_product = np.dot(film, data_Matrix[i])
        norm_a = np.linalg.norm(film)
        norm_b = np.linalg.norm(data_Matrix[i])
        similarity=dot_product / (norm_a * norm_b)
        similarty_df=similarty_df.append({'userId': i, 'Cosin_similarty': similarity},ignore_index=True)
    return similarty_df  


# %%
# def Similarities(data_Matrix,film_name,Mode="Item based"):
#     film=data_Matrix[film_name]
#     if Mode== "Item based":
#         similarty_df = pd.DataFrame(columns=['title', 'Cosin_similarty'])
#         for i in data_Matrix:
#             similarty_Factor=Cosin_Similarity(film,data_Matrix[i])
#             similarty_df=similarty_df.append({'title': i, 'Cosin_similarty': similarty_Factor},ignore_index=True)

#     elif Mode=="User based":
#         similarty_df = pd.DataFrame(columns=['ID', 'Cosin_similarty'])
#         for i in data_Matrix:
#             similarty_Factor=Cosin_Similarity(film,data_Matrix[i])
#             similarty_df=similarty_df.append({'ID': i, 'Cosin_similarty': similarty_Factor},ignore_index=True)

#     return similarty_df  

# %% [markdown]
# # Use Data matrix to match Toy Story (1995)

# %%
Toy_story_ratings = user_movie_rating['Toy Story (1995)']
Toy_story_ratings


# %%
movies_like_Toy_story=Cosin_Similarity(user_movie_rating,'Toy Story (1995)').sort_values('Cosin_similarty', ascending=False)
movies_like_Toy_story.dropna(inplace=True)
movies_like_Toy_story.sort_values('Cosin_similarty', ascending=False).head(10)


# %%
cos_Toy_Story = movies_like_Toy_story.join(ratings_mean_count['rating_counts'],on='userId')
cos_Toy_Story.head()


# %%
cos_Toy_Story[cos_Toy_Story ['rating_counts']>100].sort_values('Cosin_similarty', ascending=False).head(10)

# %% [markdown]
# # Use Data matrix to match Waiting to Exhale (1995)

# %%
Toy_story_ratings = user_movie_rating['Waiting to Exhale (1995)']
movies_like_Waiting_to_exhale=Cosin_Similarity(user_movie_rating,'Waiting to Exhale (1995)').sort_values('Cosin_similarty', ascending=False)
movies_like_Waiting_to_exhale.dropna(inplace=True)
movies_like_Waiting_to_exhale.sort_values('Cosin_similarty', ascending=False).head(10)


# %%
cos_Waiting_to_exhale = movies_like_Waiting_to_exhale.join(ratings_mean_count['rating_counts'],on='userId')
cos_Waiting_to_exhale.head()


# %%
cos_Waiting_to_exhale[cos_Waiting_to_exhale ['rating_counts']>20].sort_values('Cosin_similarty', ascending=False).head(10)

# %% [markdown]
# # Part Three

# %%
Movies_User_Ratings=user_movie_rating.T # Transpose Movie user table 
Movies_User_Ratings.head(10)


# %%
User_200_Ratings=Movies_User_Ratings[200]
User_200_Ratings.head(10)

# %% [markdown]
# # Users like USer200

# %%
Users_like_userID200=Cosin_Similarity(Movies_User_Ratings,200).sort_values('Cosin_similarty', ascending=False)
Users_like_userID200.dropna(inplace=True)
Top_ten_similar_users=Users_like_userID200.sort_values('Cosin_similarty', ascending=False).head(10)
Top_ten_similar_users

# %% [markdown]
# # Intersection between original merging data with Top ten similar users on userId

# %%
intersection_df = pd.merge(movie_data, Top_ten_similar_users, how ='inner', on ='userId') 
#generate new dataFrame groupby title on mean of ratings for ten similar users
ratings_mean_for_ten_users = pd.DataFrame(intersection_df.groupby('title')['rating'].mean())
# dropes Movies that isn't rated by ten similar users
ratings_mean_for_ten_users.dropna(inplace=True) 
#sort mean of rating asending to recommend the higher three movies to user of id 200
ratings_mean_for_ten_users.sort_values("rating",ascending=False).head(3)


