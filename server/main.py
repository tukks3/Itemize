from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_cors import CORS
import logging
import os

from src.search import validate_champ, validate_opps
from src.get_results import get_results

CHAMP_ICON_DIR = 'data/champ_icons'
ITEM_ICON_DIR = 'data/item_icons'


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


CORS(
    app,
    resources={r"/api/*": {
        "origins": [
            "https://your-frontend.vercel.app",
            "https://yourdomain.com"
        ]
    }}
)


@app.route('/api/listAllChamps')
def list_all_champs():
    files = [f for f in os.listdir(CHAMP_ICON_DIR)]
    return jsonify({
        'icons': [f'/api/champ_icons/{f}' for f in files]
    })

@app.route('/api/champ_icons/<path:filename>', methods=['GET'])
def champ_icons(filename):
    return send_from_directory(CHAMP_ICON_DIR, filename, max_age=60*60*24*30)



@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        champ = data['champName']
        result = validate_champ(champ)
        return jsonify({'champId': result}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/validTeam', methods=['POST'])
def valid_team():

    try:
        data = request.get_json()

        champ_name = data['champId']

    # To return to homepage if invalid input in URL
    except ValueError as e:
        return jsonify({'error': str(e), 'route': 'true'}), 404


    try:

        opp_team = [opp for opp in data['oppTeam'] if opp is not None]
        opp_name = data['oppName']

        if opp_name is None:
            raise ValueError('Select a champion')

        result = validate_opps(champ_name, opp_team, opp_name)

        return jsonify({'oppId': result}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/getResults', methods=['POST'])
def results():

    data = request.get_json()
    champ = data['champId']
    opp_team = data['oppTeam']


    item_counters = get_results(champ, opp_team)

    for item in item_counters:
        item['item_icon_url'] = f'/api/item_icons/{item['item_id']}.png'

    print(item_counters)

    return jsonify(item_counters)


@app.route('/api/item_icons/<path:filename>', methods=['GET'])
def item_icons(filename):
    return send_from_directory(ITEM_ICON_DIR, filename, max_age=60*60*24*30)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
