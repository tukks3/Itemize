import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src.config import CHAMP_ICON_FOLDER
from src.config import ITEM_ICON_FOLDER

CHAMP_LEN = 4
ITEM_NUMBER_LEN = 4

def get_champ_icons():
     url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/"
     try:
          response = requests.get(url)
          response.raise_for_status
          soup = BeautifulSoup(response.text, "html.parser")


     except requests.RequestException as e:
          print(f"Error downloading the file: {e}")

     links = set()

     for a in soup.select("a[href]"):
          href = a["href"]
          num = href.removesuffix(".png")



          if (
               all([
                    href.lower().endswith(".png"),
                    len(num) < CHAMP_LEN,
                    num.isdigit(),
               ])
          ):
               links.add(href)

     for link in links:
          file_path = f"{CHAMP_ICON_FOLDER}/{link}"
          icon_url = urljoin(url, link)

          r = requests.get(icon_url)

          with open(file_path, "wb") as f:
               f.write(r.content)


def get_item_icons():

    url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/items/icons2d/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as e:
            print(f"Error downloading the file: {e}")


    links = set()

    for a in soup.select("a[href]"):
        href = a["href"]

        if (
             len(href) > ITEM_NUMBER_LEN
             and all([
                  href.lower().endswith(".png"),
                  href[:ITEM_NUMBER_LEN].isdigit(),
                  not href[ITEM_NUMBER_LEN].isdigit(),
             ])
        ):
             links.add(href)

    for link in links:
        file_path = f"{ITEM_ICON_FOLDER}/{link[:ITEM_NUMBER_LEN]}.png"
        icon_url = urljoin(url, link)

        r = requests.get(icon_url)

        with open(file_path, "wb") as f:
            f.write(r.content)

