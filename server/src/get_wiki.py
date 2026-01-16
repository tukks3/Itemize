# Utility file
import json
import re
import requests
from slpp import slpp as lua

class GetWiki:
    def __init__(self, all_champs_title, all_champs_sec):
        self.all_champs_title = all_champs_title
        self.all_champs_sec = all_champs_sec
        

    # Template for LoL wiki pages
    def query_template(self, title, sec):
        url = "https://wiki.leagueoflegends.com/api.php"
        params = {
            "action": "query",
            "titles": title,
            "format": "json",
            "prop": "revisions",
            "rvprop": "content",
            "rvslots": "main",
            "rvsection": sec,
        }

        try:
            response = requests.get(url, params=params)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to query '{title}' (1): {e}")
        return response.text


    def get_champs(self, title, section, case):
        all_champs = []
        for section in section:
            data = self.query_template(title, section)
            match case:
                case 0:
                    names = list(
                        set(
                            re.findall(
                                    r"\*\s\{\{(?:cai|cais)\|[A-Za-z\s\.'!]+\|(?P<name>[A-Za-z\s\.']+)\}\}",
                                    data,
                                    re.MULTILINE,
                                )
                            )
                        )
                case 1:
                    names = list(
                        set(
                            re.findall(
                                r"\*\s\{\{(?:ci)+\|(?P<name>[A-Za-z\s\.']+)\}\}",
                                data,
                                re.MULTILINE,
                            )
                        )
                    )


            names = [
                name.replace(" ", "").replace("'", "").replace(".", "").lower()
                for name in names
                ]
            all_champs.extend(names)
        return all_champs

    def get_champ_data(self):
        data = self.query_template(self.all_champs_title, self.all_champs_sec)
        j = json.loads(data)
        return self.convert_lua(j)

    def convert_lua(self, data):
        # Isolate lua
        try:
            page = next(iter(data["query"]["pages"].values()))
            lua_str = page["revisions"][0]["slots"]["main"]["*"]
            lua_str = lua_str.replace("-- <pre>\nreturn ", "").replace(
                "-- </pre>\n-- [[Category:Lua]]", ""
            )
        except KeyError as e:
            raise KeyError(
                f"Failed to access keys in 'convert_lua': {self.all_champs_title}: {e}"
            )

        # Convert lua to dicts
        try:
            wiki_data = lua.decode(lua_str)
        except ValueError as e:
            raise ValueError(f"Lua error in 'convert_lua': {e}")

        return(iter(wiki_data.values()))


