#!/usr/bin/env python

import json
from datetime import datetime
from os import getenv
from ratelimit import limits, sleep_and_retry
import requests
from unqlite import UnQLite

ARTSY_API = "https://api.artsy.net/api"
ARTSY_HEADERS = {
    "X-Xapp-Token": getenv("ARTSY_TOKEN")
}
DB = UnQLite("./artsy.db")

@sleep_and_retry
@limits(calls=50, period=10)
def req_artsy_artworks(artworks_page):
    return requests.get(artworks_page, headers=ARTSY_HEADERS)

def main():
    artworks = DB.collection("artworks")
    artworks.create()
    moar_pages = True
    counter = 1
    json_obj = {}
    while moar_pages:
        if counter == 1:
            artworks_page = f"{ARTSY_API}/artworks"
        else:
            try:
                artworks_page = json_obj["_links"]["next"]["href"]
            except KeyError:
                moar_pages = False
                break
        try:
            print(artworks_page)
            res = req_artsy_artworks(artworks_page)
        except requests.exceptions.RequestException as err:
            print(f"[{datetime.now()}] {err}")
            break
        json_obj = json.loads(res.text)
        artworks.store(json_obj["_embedded"]["artworks"])
        counter += 1

if __name__ == "__main__":
    main()
