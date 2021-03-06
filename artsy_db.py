#!/usr/bin/env python

import os.path
from unqlite import UnQLite

DB = UnQLite(f"{os.path.dirname(os.path.realpath(__file__))}/artsy.db")

CATEGORIES_WANTED = [
    "Drawing, Collage or other Work on Paper",
    "Painting",
    "Photography",
    "Posters",
    "Print",
]

BAD_IDS = [
    26028,
]

MINIMUM_ICONICITY = 35

def is_good_piece(piece):
    return bool("image_versions" in piece and
        piece["category"] in CATEGORIES_WANTED and
        piece["__id"] not in BAD_IDS and
        int(piece["iconicity"]) >= MINIMUM_ICONICITY)

def get_artworks():
    artworks = DB.collection("artworks")
    return artworks.filter(is_good_piece)
