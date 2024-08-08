import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os

# Load datasets
movies = pd.read_csv('ml-latest-small/movies.csv')
ratings = pd.read_csv('ml-latest-small/ratings.csv')

# Create a dummy 'overview' column since the small dataset does not have one
movies['overview'] = movies['title'] + ' is a great movie.'

# Preprocess the dataset
tfidf = TfidfVectorizer(stop_words='english')
movies['overview'] = movies['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(movies['overview'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Ensure the models directory exists
os.makedirs('models', exist_ok=True)

# Save the processed data
movies.to_pickle('models/movies.pkl')
pd.to_pickle(cosine_sim, 'models/cosine_sim.pkl')

print("Data preprocessing complete and saved to disk.")
