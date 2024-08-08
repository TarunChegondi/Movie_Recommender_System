from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the preprocessed data
movies = pd.read_pickle('models/movies.pkl')
cosine_sim = pd.read_pickle('models/cosine_sim.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['title']
    recommendations = get_recommendations(movie_title)
    return render_template('index.html', recommendations=recommendations)

def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = movies.index[movies['title'].str.lower() == title.lower()].tolist()[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Get the top 10 similar movies
        movie_indices = [i[0] for i in sim_scores]
        return movies.iloc[movie_indices].to_dict('records')
    except IndexError:
        return []

if __name__ == '__main__':
    app.run(debug=True)
