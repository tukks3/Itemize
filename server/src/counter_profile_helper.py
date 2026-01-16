import json

from src.config import CC_FILE

class CounterCheck:
    def __init__(self): ...
    def get_counter(self, champ):

        counters = []

        # Anti healing
        counters.extend(self.grievous(champ))

        # Anti burst mage
        counters.extend(self.burst_mage(champ))

        # Anti AD burst
        counters.extend(self.ad_burst(champ))

        # Anti AP poke mage
        counters.extend(self.ap_poke_mage(champ))

        # Anti AD poke mage
        counters.extend(self.ad_poke_mage(champ))

        # Anti CC
        counters.extend(self.cc(champ))

        # Anti attack-Speed champ
        counters.extend(self.attack_speed(champ))

        # Anti crit champ
        counters.extend(self.crit(champ))

        # Anti all tank
        counters.extend(self.tank(champ))

        # Anti AP tank
        counters.extend(self.ap_tank(champ))

        # Anti both AP sustained damage and damage over time
        counters.extend(self.ap_sustain_dot(champ))

        # Anti both AD sustained damage and damage over time
        counters.extend(self.ad_sustain_dot(champ))

        # Anti ADC
        counters.extend(self.squishies(champ))

        return counters

    def grievous(self, champ):
        if (
            all(
                [
                    champ['cdRoles'] == "['support', 'mage']",
                    'enchanter' in champ['wikiRoles'],
                    champ['allyHealing'] == 'True',
                ]
            )
            or all(
                [
                    champ['allyHealing'] == 'True',
                    champ['attackType'] == 'melee',
                ]
            )
            or 'self healing' in champ['championTags']
        ):
            return ['GrievousWounds']
        return []

    def burst_mage(self, champ):
        if(
            all(
            [
                any(['burst' in champ['championTags'],
                     'burst' in champ['wikiRoles'],
                     'assassin' in champ['cdRoles']]),
                champ['damageType'] == 'kMagic',
            ]
            )
            or all([
                'kMagic' in champ['damageType'],
                'mage' in champ['wikiRoles'],
                self.ap_poke_mage(champ) is not True,
            ])

        ):
            return ['SpellBlock', 'Shield']
        return []

    def ad_burst(self, champ):
        if all(
            [
                any(['burst' in champ['championTags'],
                     'burst' in champ['wikiRoles'],
                     'assassin' in champ['cdRoles']]),
                champ['damageType'] == 'kPhysical',
            ]
        ):

            return ['Armor', 'Shield']
        return []

    def ap_poke_mage(self, champ):
        if all(
            [
                'kMagic' in champ['damageType'],
                'long range' in champ['championTags'],
                'mage' in champ['cdRoles'],
                not 'burst' in champ['championTags'],
                not 'burst' in champ['wikiRoles'],
            ]
        ):
            return ['SpellBlock', 'LifeSteal', 'SpellVamp',]

        return []

    def ad_poke_mage(self, champ):
        if all(
            [
                'kPhysical' in champ['damageType'],
                'long range' in champ['championTags'],
                'mage' in champ['cdRoles'],
                not 'burst' in champ['championTags'],
                not 'burst' in champ['wikiRoles'],
            ]
        ):
            return ['Armor', 'LifeSteal', 'HealthRegen']
        return []

    def cc(self, champ):
        with open(CC_FILE) as f:
            reader = json.load(f)
            group = None
            for cc_group, names in reader.items():
                if champ['name'] in names:
                    group = cc_group
                    break
            if group is not None:
                return [{'Tenacity': group}]
            return []

    def attack_speed(self, champ):
        if 'auto-attack' in champ['championTags']:
            return ['AttackSpeedReduction']
        if all([champ['attackSpeed'] == 'True', champ['hybridAsOh'] == 'True']):
            return ['AttackSpeedReduction']
        else:
            return []

    def crit(self, champ):
        if all(
            [
                champ['crit'] == 'True',
                not 'support' in champ['cdRoles'],
            ]
        ):
            return ['CriticalStrikeReduction']
        else:
            return []

    def tank(self, champ):
        if(
            any([
                any([
                    'tank' in champ['cdRoles'],
                    'tank' in champ['wikiRoles'],
                    'juggernaut' in champ['wikiRoles'],
                ]),

                all([
                    'dive' in champ['championTags'],
                    'skirmisher' in champ['wikiRoles'],
                ])
            ])
        ):
            return ['ArmorPenetration']
        return []

    def ap_sustain_dot(self, champ):
        if (
            all([
                any([
                    'damage-over-time' in champ['championTags'],
                    'sustained damage' in champ['championTags'],
                ]),
                champ['damageType'] == 'kMagic',
            ])
        ):
            return['SpellBlock-Health']
        return[]

    def ad_sustain_dot(self, champ):
        if (
            all([
                any([
                    'damage-over-time' in champ['championTags'],
                    'sustained damage' in champ['championTags'],
                ]),
                champ['damageType'] == 'kPhysical',
            ])
        ):
            return['Armor-Health']
        return[]

    def ap_tank(self, champ):
        if(
            all([
                any([
                    champ['damageType'] == 'kMagic',
                    champ['damageType'] == 'kMixed',
                ]),
                any([
                    'tank' in champ['cdRoles'],
                    'tank' in champ['wikiRoles'],
                    'juggernaut' in champ['wikiRoles']
                ])
            ])
        ):
            return['PercentMagicPenetration']
        return[]

    def squishies(self, champ):
        if 'bottom' in champ['positions']:
            return["Lethality", "FlatMagicPenetration"]
        return []


