import requests

class GetIds:
    def __init__(self):
        self.get_items()
        self.get_champs()

    def get_items(self):
        try:
            response = requests.get(
                "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to request CDragon: {e}")

        data = response.json()

        ids = []

        for d in data:
            specs = (
                d["inStore"],
                d["categories"] != "Consumable",
                not d["from"] == [],
                d["to"] == [],
            )
            if all(specs):
                ids.append(str(d["id"]))
        return ids

    def get_champs(self):
        try:
            response = requests.get(
                "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json"
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to get champ data: {e}")
        data = response.json()
        ids = [i["id"] for i in data if str(i["id"]).isdigit() and len(str(i["id"])) < 4]
        return ids


