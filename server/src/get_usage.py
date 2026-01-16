import csv
import json

from bs4 import BeautifulSoup
import requests

from src.config import CHAMP_USAGE_FILE

GA_ID = '3026'
GA_CHAMPS = [
    15,
    18,
    22,
    24,
    28,
    29,
    39,
    51,
    56,
    67,
    81,
    91,
    92,
    107,
    114,
    119,
    126,
    133,
    141,
    157,
    164,
    166,
    202,
    203,
    221,
    222,
    233,
    234,
    238,
    240,
    246,
    266,
    360,
    429,
    498,
    523,
    555,
    777,
    804,
    895,
]


class ChampUsage:
    def __init__(self, ids):  # Takes input from get_ids for champion and item IDs
        self.item_dict = self.build_item_dict(ids.get_items())
        self.build_champ_dict(self.item_dict, ids.get_champs())

    def build_item_dict(self, ids):
        items = {}
        for id in ids:
            try:
                response = requests.get(f"https://leagueofitems.com/items/{id}")
            except requests.exceptions.RequestException as e:
                if e.response.status_code == 404:
                    continue
                else:
                    raise ConnectionError(f"Failed to get item data (Id: {id}): {e}")
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.find(id="__NEXT_DATA__").get_text()
            data = json.loads(text)
            try:
                items[id] = [
                    champ["championId"]
                    for champ in data["props"]["pageProps"]["item"]["championStats"]
                ]
            except KeyError:
                continue

        # Manually add guardian angel since its missing from LoI
        items[GA_ID] = GA_CHAMPS
        return items

    def build_champ_dict(self, item_dict, champs):
        with open(CHAMP_USAGE_FILE, "w") as f:
            fieldnames = [
                "champ_id",
                "item_ids",
            ]
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()
            for champ in champs:
                item_ids = []
                for key, value in item_dict.items():
                    if champ in value:
                        item_ids.append(key)
                writer.writerow({"champ_id": champ, "item_ids": item_ids})
