import csv

from src.config import CHAMP_FILE, FULL_TEAM

class Validate:
    def __init__(self, champ):
        self.user_champ = champ
        self._opponents = []
        self._new_opp = None

    @property
    def user_champ(self):
        return self._user_champ


    @user_champ.setter
    def user_champ(self, champ):
        try:
            self._user_champ = self.is_valid_champ(champ)
        except ValueError as e:
            raise ValueError(e)

    @property
    def opps(self):
        return self._opponents

    @property
    def new_opp(self):
        return self._new_opp

    def add_opps(self, opp):
        try:
            opp_id = self.is_valid_champ(opp)

            if len(self._opponents) == FULL_TEAM:
                raise ValueError('Full team')

            elif opp_id in self.opps or opp_id in self.user_champ:
                raise ValueError('Champion already selected')
            else:
                self._opponents.append(opp_id)
                self._new_opp = opp_id

        except ValueError as e:
            raise ValueError(e)


    def is_valid_champ(self, champ):
        if champ is None:
            raise ValueError("No champ selected")

        with open(CHAMP_FILE) as f:
            reader = csv.DictReader(f)


            if champ.isdigit():
                champ = str(champ)
                for row in reader:
                    if champ == str(row['id']):
                        return champ
                else:
                    raise ValueError('Invalid champion ID')

            else:
                champ = champ.strip().lower()
                for row in reader:
                    if champ == row['name'] or champ == row['alias']:
                        return str(row['id'])
                else:
                    raise ValueError('Invalid champion name')
