#!/usr/bin/python3
'''
app for registering blueprint and starting flask
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flask_login import LoginManager
from models.user import User
app = Flask(__name__)
CORS(app, origins="0.0.0.0")

# Register Blueprint
app.register_blueprint(app_views)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(id):
    return storage.get(User, id)

# Teardown app context to close the database connection
@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def not_found(message):
    """Handles the 404 status code
    """
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)