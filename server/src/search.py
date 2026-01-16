import sys

from src import validate



def validate_champ(champ):
    try:
        valid = validate.Validate(champ)
        return valid.user_champ
    except ValueError as e:
        raise ValueError(str(e))
    except EOFError:
        sys.exit('No valid champion name')


def validate_opps(champ, opp_team, opp_name):
    valid = validate.Validate(champ)

    try:
        for opp in opp_team:
            valid.add_opps(opp)

        valid.add_opps(opp_name)

        return valid.new_opp

    except ValueError as e:
        raise ValueError(str(e))

    except EOFError:
        if not valid.opps:
            sys.exit('\nNo valid enemies')
        else:
            return valid.opps
