import csv
import sys

import compare
import validate

from config import CHAMP_FILE
from config import FULL_TEAM

def main():
    champ = validate_champ()
    opps = validate_opps(champ)

    champ_id = ids(champ)
    opp_ids = ids(opps)

    comp = compare.Compare(champ_id, opp_ids)
    item_counters = comp.compare()

    print(item_counters)

def validate_champ():
    champ = input('Enter champion: ').strip().lower()
    try:
        validate.Validate(champ)
        return champ
    except ValueError as e:
        print(e)
    except EOFError:
        sys.exit('No valid champion name')

def validate_opps(champ):
    valid = validate.Validate(champ)
    while True:
        try:
            opp = input('Enter enemy: ').strip().lower()

            valid.add_opps(opp)

            if len(valid.opps) == FULL_TEAM:
                return valid.opps
        except ValueError as e:
            print(e)
        except EOFError:
            if not valid.opps:
                sys.exit('\nNo valid enemies')
            else:
                return valid.opps

def ids(names):
    with open(CHAMP_FILE) as f:
        reader = csv.DictReader(f)

        # For list of opps
        if isinstance(names, (list, tuple, set)):
            names = set(names)
            return[row['id'] for row in reader if row['name'] in names or row['alias'] in names]

        # For single champion name
        elif isinstance(names, str):
            for row in reader:
                if names in row['name'] or names in row['alias']:
                    return row['id']
        else:
            sys.exit("Invalid Type")


if __name__ == '__main__':
    main()

