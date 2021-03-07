#!/usr/bin/env python

# TODO: Build in support for updating an already-existing DB:
#       * Add new artworks
#       * Handle missing category

# NOTE: 27577 records stored as of 03/07/2021

import json
import os.path
from datetime import datetime
from os import getenv
from ratelimit import limits, sleep_and_retry
import requests
from unqlite import UnQLite

ARTSY_API = "https://api.artsy.net/api"
ARTSY_HEADERS = {
    "X-Xapp-Token": getenv("ARTSY_TOKEN")
}
DB = UnQLite(f"{os.path.dirname(os.path.realpath(__file__))}/artsy.db")

# Artsy API rate limit says 5 requests per second
# In practice, this seems to be lower
@sleep_and_retry
@limits(calls=10, period=5)
def artsy_request(url):
    return requests.get(url, headers=ARTSY_HEADERS)

def create_populate():
    artworks = DB.collection("artworks")
    if not artworks.create():
        print("Collection already exists, not proceeding with create/populate")
        return
    moar_pages = True
    counter = 1
    page_dict = {}
    while moar_pages:
        if counter == 1:
            artworks_page = f"{ARTSY_API}/artworks"
        else:
            try:
                artworks_page = page_dict["_links"]["next"]["href"]
            except KeyError:
                moar_pages = False
                break
        try:
            print(artworks_page)
            res = artsy_request(artworks_page)
        except requests.exceptions.RequestException as err:
            print(f"[{datetime.now()}] {err}")
            break
        page_dict = json.loads(res.text)
        artworks.store(page_dict["_embedded"]["artworks"])
        counter += 1

def add_artists():
    artworks = DB.collection("artworks")
    record = 0
    for artwork in artworks:
        if "artists" not in artwork:
            try:
                print(artwork["_links"]["artists"]["href"])
                res = artsy_request(artwork["_links"]["artists"]["href"])
            except requests.exceptions.RequestException as err:
                print(f"[{datetime.now()}] {err}")
                break
            try:
                artists_dict = json.loads(res.text)
            except json.decoder.JSONDecodeError:
                print(res.text)
                break
            artwork["artists"] = []
            for artist in artists_dict["_embedded"]["artists"]:
                artwork["artists"].append(artist["name"])
            artworks.update(record, artwork)
            record += 1

if __name__ == "__main__":
    create_populate()
    add_artists()
