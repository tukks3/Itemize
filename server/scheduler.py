import logging
from apscheduler.schedulers.blocking import BlockingScheduler

from src.get_ids import GetIds
from src.get_usage import ChampUsage
from src.get_profiles import ItemProfile, ChampProfile, CounterProfiles
from src.get_icons import get_champ_icons, get_item_icons


logging.basicConfig(level=logging.INFO)


def job():
    ids = GetIds()
    ChampUsage(ids) # Creates 'champ_items.csv' for items used by each champ
    ItemProfile(ids) # Creates 'item_profiles.csv' for stats of each item
    ChampProfile(ids) # Creates 'champ_profiles.csv' for info on all champs
    CounterProfiles() # Creates 'opp_counters.csv' for opponent weaknesses
    get_champ_icons()
    get_item_icons()

def main():
    scheduler = BlockingScheduler(timezone="UTC")

    scheduler.add_job(
        job,
        trigger='cron',
        id='refresh_data',
        hour=4,
        minute=0,
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=60,
    )


    scheduler.start()
    logging.info("Scheduler started.")


if __name__ == "__main__":
    main()


