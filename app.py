from flask import Flask, jsonify, request, g
from flask_cors import CORS
import models
from flask_login import LoginManager
from resources.dogs import dog
from resources.user import user
import os

DEBUG = True
PORT = 8000

login_manager = LoginManager()

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


CORS(dog, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(dog, url_prefix='/api/v1/dogs')
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

if 'ON_HEROKU' in os.environ:
    print('\non heroku!')
    models.initialize()


# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
