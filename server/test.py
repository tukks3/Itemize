from src.get_ids import GetIds
from src.get_usage import ChampUsage
from src.get_profiles import ItemProfile, ChampProfile, CounterProfiles
from src.get_icons import get_champ_icons, get_item_icons

ids = GetIds()
ChampUsage(ids) # Creates 'champ_items.csv' for items used by each champ
ItemProfile(ids) # Creates 'item_profiles.csv' for stats of each item
ChampProfile(ids) # Creates 'champ_profiles.csv' for info on all champs
CounterProfiles() # Creates 'opp_counters.csv' for opponent weaknesses
get_champ_icons()
get_item_icons()
