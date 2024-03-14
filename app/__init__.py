# from authlib.integrations.flask_client import OAuth
import os
import sys
from flask import Flask, got_request_exception, abort as original_flask_abort, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_sieve import Sieve
from logging.config import dictConfig
#to get the json


# Create package object.
db = SQLAlchemy()
api = Api()
sieve = Sieve()

# Initialize the package that needed
def init_app(name, config=None):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": "storage/logs/log.log",
                    "mode": "a",
                    "maxBytes": 1048576,
                    "backupCount": 10,
                },
            },
            "root": {"level": "INFO", "handlers": ["file", "wsgi"]},
        }
    )
    app = Flask(name)
    app.config.from_object(config)
    db.init_app(app)
    api.init_app(app)
    CORS(app)
    sieve.init_app(app)
    
    #Coba Routing
    #index
    @app.route('/')
    def dasar():
        return render_template('index.html')
    
    @app.route('/pokemon')
    def index():
        return render_template('index.html')
    
    #awalnya di atas, tapi error karena circular
    #appnya belum sepenuhnya inisiasi
    #makanya error dan sekarang dipindah setelah appnya fix
    from app.apis.pokemon.resources.poke.poke_list import PokeList
    #/pokemon nampilin list pokemon
    @app.route('/pokemon/poke')
    def pokemon():
         poke_list = PokeList.get()
         return render_template('list.html', pokemons=poke_list)
    
    from app.apis.pokemon.resources.poke.poke_detail import PokeDetail
    @app.route('/pokemon/poke/<name>')
    def poke_detail(name):
         detail = PokeDetail.get(name)
        #  detail['results']
         return render_template('detail.html', pokedetails=detail)
        # return "Information page"
    
    from app.apis.pokemon.resources.poke.review import Review
    @app.route('/pokemon/poke/<name>/review', methods=['POST'])
    def add_review(name):
         poke_review = Review()
         ##review = request.json.get('review') ##sudah di review.py
         ##pokemon.review = review
         ##db.session.commit()
         return poke_review.post(name)
        #sebelumnya didetect as error di js meskipun data tersimpan
        #soalnya tadi di func langsung begini
        #poke_review= Review(name) dan returnnya string random buat test doang
    
    @app.route('/pokemon/poke/<name>/review', methods=['GET'])
    def see_reviews(name):
         review_list = Review.get(name)
         
         return render_template('review.html', review = review_list)
    #setelah di cek di html, 'review' ini menyimpan respon begini "<Response 104 bytes [200 OK]>"
    #sudah diperbaiki
    
    # ####

    # Import the models
    # must register in here not outside of init_app.
    from .models.poke_review import PokeReview

    # Register the blueprints
    # must register in here not outside of init_app. 
    
    from .apis.pokemon import pokemonApp
    
    app.register_blueprint(pokemonApp)
    return app