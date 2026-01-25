import ast
import csv

from src.config import CHAMP_USAGE_FILE, COUNTER_FILE, ITEM_FILE

class Compare:
    def __init__(self, champ, opps):
        self.champ = champ
        self.opps = [opp for opp in opps if opp is not None]


    def compare(self):
        # Get all items used by user champion
        try:
            champ_items = []
            with open(CHAMP_USAGE_FILE) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if self.champ == row["champ_id"]:
                        champ_items = ast.literal_eval(row["item_ids"])
                        break

        except IOError:
            print("Could not read file", CHAMP_USAGE_FILE)

        with open(ITEM_FILE) as i, open(COUNTER_FILE) as c:
            item_reader = csv.DictReader(i)
            counter_reader = csv.DictReader(c)

            # Create lookups for item stats and opp counter stats
            items_lookup = self.item_stat_lookup(item_reader)
            counters_lookup = self.counter_lookup(counter_reader)

            # List of all item dicts
            all_counter_items = []

            for item in champ_items:
                item_stats = items_lookup.get((item))
                pop_item = {} # Populated item dict
                prio = 0
                all_opp_counters = {} # Dict of opp ids and lists of their counters

                for opp in self.opps:
                    per_opp_counter = [] # List of counters per opp
                    counters = counters_lookup.get(opp)
                    if self.ad_health(counters, item_stats):
                        prio += 1
                    if self.ap_health(counters, item_stats):
                        prio += 1

                    for stat in item_stats:
                        if self.has_shield(stat, counters, item_stats):
                            prio += 1
                            per_opp_counter.append('Shield')
                            break

                        elif stat in counters:
                            prio += 1
                            per_opp_counter.append(stat)

                    # Only count opps that item counters
                    if len(per_opp_counter) > 0:
                        all_opp_counters[opp] = per_opp_counter

                if prio > 0:
                    pop_item['item_id'] = item
                    pop_item['priority'] = prio
                    pop_item['counters'] = all_opp_counters
                    all_counter_items.append(pop_item)

            all_counter_items.sort(key=lambda x: x['priority'], reverse=True)

            return all_counter_items # Format: [{'item_id': '#', 'priority': #, 'counters': {'oppID#': [counters, counters,]}} etc etc]

    # Ensure shield isn't counted if item conflicts with damage type
    def has_shield(self, stat, counters, item_stats):
        if all ([
            stat == 'Shield',
            'Shield' in counters,
            self.check_shield(counters, item_stats) is True
        ]):
            return True

    def check_shield(self, counters, item_stats):
        if all([
                'Armor' in counters,
                'SpellBlock' not in counters,
                'SpellBlock' in item_stats,
        ]):
            return False

        if all([
                'SpellBlock' in counters,
                'Armor' not in counters,
                'Armor' in item_stats,
        ]):
            return False
        else:
            return True

    # Ensure health only counts against AD champs when item also has armor
    def ad_health(self, counters, item_stats):
        if all([
            'Armor-Health' in counters,
            'Armor' in item_stats,
            'Health' in item_stats,
        ]):
            return True

    # Ensure health only counts against AP champs when item also has spellblock
    def ap_health(self, counters, item_stats):
        if all([
            'SpellBlock-Health' in counters,
            'SpellBlock' in item_stats,
            'Health' in item_stats,
        ]):
            return True


    def item_stat_lookup(self, reader):
        stat_lookup = {}
        for row in reader:
            stat_lookup[(row['id'])] = [stat for stat in ast.literal_eval(row['stats'])]
        return stat_lookup

    def counter_lookup(self, reader):
        stat_lookup = {}
        for row in reader:
            stat_lookup[(row['id'])] = [counter for counter in ast.literal_eval(row['counters'])]
        return stat_lookup


# Need to use literal eval because row['counters'] is a string 