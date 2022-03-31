from os import getenv
from flask import Flask, render_template, request 
from .predict import predict_user 
from .models import DB, User, Tweet 
from .twitter import add_or_update_user

# Called a FACTORY:
def create_app():

    app = Flask(__name__)

    # Tell app where to find DB
    # Registering out DB with the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app) 

    @app.route("/")
    def home():
        users = User.query.all()
        return render_template('base.html', title = 'Home', users = users)

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title = 'Reset DB')
    
    @app.route('/populate')
    def populate():
        add_or_update_user('nasa')
        add_or_update_user('austen')
        add_or_update_user('ryanallred')
        return render_template('base.html', title = 'Populate')
    
    @app.route('/update')
    def update():
        usernames = [user.username for user in User.query.all()]
        print(usernames)
        for username in username:
            add_or_update_user(username)
        return render_template('base.html', title = 'Update')
    
    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):

        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through the
        # user submission
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} Succesfully added!".format(name)

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)

            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            # prediction returns a 0 or 1
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title="Prediction", message=message)

    return app
    
    