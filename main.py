from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv('API_KEY')

# Vérifier si la clé API est définie
if not API_KEY:
    raise ValueError("API_KEY is not set. Please add it to your .env file.")

app = Flask(__name__)

# Liste prédéfinie de pays disponibles
AVAILABLE_COUNTRIES = {
    "us": "United States",
    "fr": "France",
    "jp": "Japan",
    "de": "Germany",
    "it": "Italy",
    "gb": "United Kingdom",
    "cn": "China",
    "in": "India"
}

@app.route('/news', methods=['GET'])
def get_news():
    # Récupérer le paramètre 'country' depuis l'URL, valeur par défaut : 'us'
    country = request.args.get('country', 'us')
    
    # Vérifier si le pays est valide
    if country not in AVAILABLE_COUNTRIES:
        return jsonify({"error": f"Country '{country}' is not supported. Use /pays to see available countries."}), 400
    
    # Construire l'URL pour NewsAPI
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    
    # Faire la requête à NewsAPI
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        return jsonify(response.json())  # Retourner les données sous forme de JSON
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pays', methods=['GET'])
def get_available_countries():
    # Retourner la liste des pays disponibles
    return jsonify(AVAILABLE_COUNTRIES)

if __name__ == '__main__':
    # Exécuter l'application sur host=0.0.0.0 et port=5000
    app.run(host='0.0.0.0', port=5000)
           
