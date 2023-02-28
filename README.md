## What to watch next?
This project is a movie recommendation system built using machine learning techniques. The system takes in a user's movie preferences and recommends similar movies that the user may enjoy.

The recommendation engine is built using the collaborative filtering technique, which is a commonly used method in recommender systems. Collaborative filtering is a type of recommendation system that uses the past behavior of users to predict what they may like in the future. In the case of movies, the system looks at the user's movie ratings and compares them with other users who have similar tastes. It then recommends movies that those similar users have rated highly but the user has not yet seen.

To build the system, a dataset of movie ratings was used. The dataset contains information on user movie ratings and movie metadata such as title, genre, and release year. The dataset was preprocessed to remove duplicates, missing values, and noisy data.

When a user inputs a movie title, the system retrieves the metadata for that movie and calculates its cosine similarity to every other movie in the database. The cosine similarity algorithm measures the similarity between two vectors (in this case, the movie plot summaries), and returns a value between 0 and 1, where 1 means the vectors are identical.

The system then returns a list of the top N movies (where N is a specified number) with the highest cosine similarity scores to the input movie. These recommended movies are displayed to the user along with their poster images and some basic information such as title and synopsis.

The user interface for the recommendation system was built using the Flask web framework. The user enters their movie preferences on the front-end, which sends a request to the Flask server. The server then uses the recommendation engine to generate movie recommendations, which are returned to the front-end for display.

Overall, this project demonstrates the use of machine learning and collaborative filtering techniques in building a movie recommendation system, which can provide users with personalized movie recommendations based on their past movie ratings.

![image](https://user-images.githubusercontent.com/120294776/221744691-75d4eb82-31ad-4883-be8a-df0f10c90c12.png)
