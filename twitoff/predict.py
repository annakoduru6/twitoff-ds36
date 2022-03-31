from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet

def predict_user(user0_username, user1_username, hypo_tweet_text):
    # Query for two users from DB
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Get word embeddings from users' tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Combine their vects into X matrix
    X = np.vstack([user0_vects, user1_vects])

    # Crate 0s and 1s
    y = np.concatenate([np.zeros(len(user0.tweets)),
                        np.ones(len(user1.tweets))])
    
    log_reg = LogisticRegression()
    log_reg.fit(X, y)

    hypo_tweet_vect = np.array([vectorize_tweet(hypo_tweet_text)])

    prediction = log_reg.predict(hypo_tweet_vect)

    return prediction[0]