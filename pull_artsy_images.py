#!/usr/bin/env python

import os.path
import requests
import artsy_db

def main():
    for artwork in artsy_db.get_artworks():
        art_id = artwork["__id"]
        artwork_file = os.path.normpath(f"data/{art_id}_normalized.jpg")
        if not os.path.exists(artwork_file):
            res = requests.get(artwork["_links"]["image"]["href"].format(image_version="normalized"))
            open(artwork_file, "wb").write(res.content)
            print(artwork["_links"]["image"]["href"].format(image_version="normalized"))

if __name__ == "__main__":
    main()
