from flask import Flask, jsonify, request, render_template
from flask_jsonpify import jsonpify
import json, requests, pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
from ingredient_parser import ingredient_parser
import config, rec_sys

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello():
    return HELLO_HTML

HELLO_HTML = """
     <html><body>
         <h1>PoC Demostrador</h1>
         <p>
         
         </p>
         <p>Indique algunos ingredientes a la consulta para recibir recomendaciones de recetas.
         <br>Clic <a href="/recipe?ingredients= pasta tomato onion">aquí</a> para visualizar un ejemplo.
     </body></html>
     """

@app.route('/recipe', methods=["GET"])
def recommend_recipe():
    ingredients = request.args.get('ingredients')   
    recipe = rec_sys.RecSys(ingredients)
    
    response = {}
    count = 0
    for index, row in recipe.iterrows():
        response[count] = {
            'recipe': str(row['recipe']),
            'score': str(row['score']),
            'ingredients': str(row['ingredients']),
            'url': str(row['url'])
        }
        count += 1
    return jsonify(response)
   

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)



# http://127.0.0.1:5000/recipe?ingredients=pasta

# use ipconfig getifaddr en0 in terminal (ipconfig if you are on windows, ip a if on linux) 
# to find intenal (LAN) IP address. Then on any devide on network you can use server.