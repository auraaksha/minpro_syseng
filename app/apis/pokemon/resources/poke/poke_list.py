import json
import requests
import traceback
from flask import make_response, jsonify, current_app, request
from flask_restful import Resource, reqparse
from flask_sieve import Validator

class PokeList(Resource):
    @classmethod
    #limit getnya maks 20 pokemon aja (default)
    def get(cls):
        r = requests.get('https://pokeapi.co/api/v2/pokemon')
        data = r.json() #nyoba

        pokemon_list = []

        for result in data['results']:
            pokemon_info = {
                'name' : result['name'],
                'types' : [],
                'url' : result['url']
            }
            pokemon_list.append(pokemon_info)

        #perlu requests lagi karena info type ada di page beda
        for pokemon_info in pokemon_list:
            pokemon_data = requests.get(pokemon_info['url']).json()
            pokemon_info['types'] = [type_data['type']['name'] for type_data in pokemon_data['types']]

        return pokemon_list

   