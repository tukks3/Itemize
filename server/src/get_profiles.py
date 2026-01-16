import csv

import requests

from src.get_wiki import GetWiki
from src.counter_profile_helper import CounterCheck as cph

from src.config import CHAMP_FILE
from src.config import COUNTER_FILE
from src.config import ITEM_FILE

CHAMP_DATA_TITLE = "Module:ChampionData/data"
CHAMP_DATA_SEC = None

ALLY_HEAL_TITLE = "Healing"
ALLY_HEAL_SEC = "2"
ALLY_HEAL_CASE = 0

AS_TITLE = "Attack_speed"
AS_SEC = ["23", "33"]
AS_CASE = 0

CRIT_TITLE = "Critical_strike"
CRIT_SEC = ["7", "16", "20"]
CRIT_CASE = 0

AS_OHD_TITLE = "Hybrid"
AS_OHD_SEC = "3"
AS_OHD_CASE = 1

STAT_TYPES = ["Grievous Wounds", "Shield"]

PERCENT_MP = "%\u003c/attention\u003e Magic Penetration"

ITEM_SPECS = {
    "GrievousWounds": "Grievous Wounds",
    "AttackSpeedReduction": "Reduce the \u003cattackSpeed",
    "CriticalStrikeReduction": "less damage from Critical Strikes",
    "PercentMagicPenetration": PERCENT_MP,
    "Lethality": "Lethality",
    "Shield" : "\u003Cshield\u003EShield\u003C/shield\u003E",
}


class ItemProfile:
    def __init__(self, ids): # Takes input from get_ids for item IDs
        self.profile(ids.get_items())

    def profile(self, ids):
        try:
            response = requests.get(
                "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to get item data: {e}")
        data = response.json()

        with open(ITEM_FILE, "w") as f:
            fieldnames = ["id", "name", "stats"]
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()
            for i in data:
                for id in ids:
                    id = int(id)
                    if i["id"] == id:
                        writer.writerow(
                            {
                                "id": id,
                                "name": i["name"],
                                "stats": self.get_stats(i),
                            }
                        )
                        break

    def get_stats(self, i):
        stats = i["categories"]
        for j in ITEM_SPECS:
            if ITEM_SPECS[j].lower() in str(i["description"]).lower():
                stats.append(j)
        if "MagicPenetration" in i["categories"] and PERCENT_MP not in i["description"]:
            stats.append("FlatMagicPenetration")
        return stats


class ChampProfile:
    def __init__(self, ids): # Takes input from get_ids for champion IDs
        self.profile(ids.get_champs())

    def profile(self, ids):

        # Get full wiki data of all champs
        wiki = GetWiki(CHAMP_DATA_TITLE, CHAMP_DATA_SEC)
        all_champ_data = list(wiki.get_champ_data())

        # Get create dicts of wiki data roles amd posoitions
        role_lookup = self.get_wiki_lookup('role', all_champ_data)
        pos_lookup = self.get_wiki_lookup('client_positions', all_champ_data)

        # Get specific page info using get_wiki module
        ally_heal_champs = wiki.get_champs(
            ALLY_HEAL_TITLE, ALLY_HEAL_SEC, ALLY_HEAL_CASE
        )
        as_champs = wiki.get_champs(AS_TITLE, AS_SEC, AS_CASE)
        crit_champs = wiki.get_champs(CRIT_TITLE, CRIT_SEC, CRIT_CASE)
        as_ohd_champs = wiki.get_champs(AS_OHD_TITLE, AS_OHD_SEC, AS_OHD_CASE)

        with open(CHAMP_FILE, "w") as f:
            fieldnames = [
                "id",
                "name",
                "alias",
                "positions",
                "damageType",
                "attackType",
                "championTags",
                "cdRoles",
                "wikiRoles",
                "allyHealing",
                "attackSpeed",
                "crit",
                "hybridAsOh",
            ]
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()


            for id in ids:
                try:
                    response = requests.get(
                        f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/{id}.json"
                    )
                    data = response.json()

                    alias = data["alias"].lower()  # Just for readability

                    writer.writerow(
                        {
                            "id": data["id"],
                            "name": data["name"].lower(),
                            "alias": alias,
                            "positions": pos_lookup.get(id),
                            "damageType": data["tacticalInfo"]["damageType"],
                            "attackType": data["tacticalInfo"]["attackType"].lower(),
                            "championTags": [
                                data["championTagInfo"]["championTagPrimary"].lower(),
                                data["championTagInfo"]["championTagSecondary"].lower(),
                            ],
                            "cdRoles": data["roles"],
                            "wikiRoles": role_lookup.get(id),
                            "allyHealing": self.lookup_stat(alias, ally_heal_champs),
                            "attackSpeed": self.lookup_stat(alias, as_champs),
                            "crit": self.lookup_stat(alias, crit_champs),
                            "hybridAsOh": self.lookup_stat(alias, as_ohd_champs),
                        }
                    )
                except requests.exceptions.RequestException as e:
                    raise ConnectionError(
                        f"Failed to request CDragon champ ID: {id}: {e}"
                    )
                except KeyError as e:
                    raise KeyError(f"Failed to access champion keys: {e}")

    def get_wiki_lookup(self, key, mod_data):
        lookup_dict = {}
        for i in mod_data:
            lookup_dict[int(i["id"])] = [
                i[key][j].lower() for j in range(len(i[key]))
            ]
        return lookup_dict


    def lookup_stat(self, name, champ_list):
        if name in champ_list:
            return True
        else:
            return False


class CounterProfiles:
    def __init__(self):
        self.opp_analysis()

    def opp_analysis(self):
        with open(CHAMP_FILE) as opp_f, open(COUNTER_FILE, "w") as cf:
            reader = csv.DictReader(opp_f)
            fieldnames = [
                "id",
                "name",
                "alias",
                "counters",
            ]
            writer = csv.DictWriter(cf, fieldnames)
            writer.writeheader()
            counter = cph()
            for row in reader:
                writer.writerow(
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "alias": row["alias"],
                        "counters": counter.get_counter(row),
                    }
                )
