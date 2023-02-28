import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv(r'C:\Users\Kush\Desktop\Python\higher level projects\APCSP Create Task\datasets/movie_metadata.csv')
movies = movies.fillna('')
movies['comb'] = movies['director_name'] + ' ' + movies['actor_1_name'] + ' ' + movies['actor_2_name'] + ' ' + movies['actor_3_name'] + ' ' + movies['genres'] + ' ' + movies['movie_title'] + ' ' + movies['plot_keywords']

cv = CountVectorizer()
count_matrix = cv.fit_transform(movies['comb'])

cosine_sim = cosine_similarity(count_matrix)

def get_recommendations(title):
    # convert the input movie title to lowercase
    title = title.lower()

    # select relevant features to calculate similarity scores
    features = ['director_name', 'actor_1_name', 'actor_2_name', 'actor_3_name', 'genres', 'plot_keywords']

    # fill missing values with empty strings
    for feature in features:
        movies[feature] = movies[feature].fillna('')

    # create a new feature that combines the relevant features
    movies['comb'] = movies.apply(lambda row: ' '.join([row[feature] for feature in features]), axis=1)

    # calculate the cosine similarity matrix using the combined feature
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(movies['comb'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # get the index of the input movie
    idx = movies[movies['movie_title'].apply(lambda x: x.lower()) == title].index[0]

    # get the similarity scores of all movies compared to the input movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # sort the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # select the top 10 similar movies (excluding the input movie itself)
    sim_scores = sim_scores[1:11]

    # get the titles of the top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    similar_movies = movies.loc[movie_indices, 'movie_title']

    return similar_movies.tolist()


#rec = input("I want a movie to watch after: ")
print(get_recommendations(input("I want a movie to watch after: ")))
