from flask import Flask
from config import Config

def make_app():
    app =  Flask(__name__)
    app.config.from_object(Config)


    #Blueprints
    from .routes import main
    app.register_blueprint(main)
    return app