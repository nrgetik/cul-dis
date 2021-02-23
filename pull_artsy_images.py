#!/usr/bin/env python

import os.path
import requests
from unqlite import UnQLite

DB = UnQLite("./artsy.db")

def main():
    categories_wanted = [
        "Drawing, Collage or other Work on Paper",
        "Painting",
        "Photography",
        "Posters",
        "Print",
    ]
    bad_ids = [
        26028,
    ]
    artworks = DB.collection("artworks")
    filtered_artworks = artworks.filter(lambda piece: piece["category"] in categories_wanted and piece["__id"] not in bad_ids)
    for artwork in filtered_artworks:
        if "image_versions" in artwork:
            if int(artwork["iconicity"]) >= 35:
                art_id = artwork["__id"]
                artwork_file = os.path.normpath(f"data/{art_id}_normalized.jpg")
                if not os.path.exists(artwork_file):
                    res = requests.get(artwork["_links"]["image"]["href"].format(image_version="normalized"))
                    open(artwork_file, "wb").write(res.content)
                    print(artwork["_links"]["image"]["href"].format(image_version="normalized"))


if __name__ == "__main__":
    main()
