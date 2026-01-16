import get_ids
import get_profiles
import get_usage
from get_icons import get_champ_icons, get_item_icons


ids = get_ids.GetIds()
#get_usage.ChampUsage(ids) # Creates 'champ_items.csv' for items used by each champ
get_profiles.ItemProfile(ids) # Creates 'item_profiles.csv' for stats of each item
#get_profiles.ChampProfile(ids) # Creates 'champ_profiles.csv' for info on all champs
#get_profiles.CounterProfiles() # Creates 'opp_counters.csv' for opponent weaknesses
#get_champ_icons()
#get_item_icons()
