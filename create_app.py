from flask import Flask

def create_app():
    """
    a function to create the flask app

    Returns:
        flsak app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hghghghg'

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app