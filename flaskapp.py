from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

app = Flask(__name__)

# define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# define the route for the recommendation page
@app.route('/recommendations', methods=['POST'])
def recommendations():
    # get the user input from the form
    title = request.form['movie_title']

    # implement the recommendation algorithm
    movies = pd.read_csv(r'datasets/movie_metadata.csv')
    movies = movies.fillna('')
    movies['comb'] = movies['director_name'] + ' ' + movies['actor_1_name'] + ' ' + movies['actor_2_name'] + ' ' + \
                     movies['actor_3_name'] + ' ' + movies['genres'] + ' ' + movies['movie_title'] + ' ' + movies[
                         'plot_keywords']
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(movies['comb'])
    cosine_sim = cosine_similarity(count_matrix)
    idx = movies[movies['movie_title'].apply(lambda x: x.lower()) == title.lower()].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    similar_movies = movies.loc[movie_indices, ['movie_title', 'movie_imdb_link']]

    # fetch the synopsis of each movie using OMDB API
    for i, movie_title in enumerate(similar_movies['movie_title']):
        try:
            omdb_url = 'http://www.omdbapi.com/?t=' + movie_title.replace(' ', '+') + '&apikey=8d10a43'
            response = requests.get(omdb_url)
            response_json = response.json()
            synopsis = response_json.get('Plot')
            imdb_link = response_json.get('imdbID')
            if synopsis:
                similar_movies.at[movie_indices[i], 'synopsis'] = synopsis
            if imdb_link:
                imdb_link = f'http://www.imdb.com/title/{imdb_link}/'
                similar_movies.at[movie_indices[i], 'movie_imdb_link'] = imdb_link
        except:
            pass

    posters = []
    imdb_links = []
    for imdb_id in similar_movies['movie_imdb_link'].apply(lambda x: x.split('/')[-2]):
        try:
            poster_url = f'http://img.omdbapi.com/?i={imdb_id}&h=600&apikey=8d10a43'
            imdb_link = f'http://www.imdb.com/title/{imdb_id}/'
            posters.append(poster_url)
            imdb_links.append(imdb_link)
        except:
            posters.append('https://via.placeholder.com/600x900.png?text=No+Poster+Available')
            imdb_links.append('')

    context = {'movies': similar_movies.values, 'posters': posters, 'enumerate': enumerate, "imdb_links": imdb_links}
    return render_template('recommended.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
