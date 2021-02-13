#!/usr/bin/env python

import json
import sqlite3
from datetime import datetime
from time import sleep
from ratelimit import limits, sleep_and_retry
import requests

MET_API_V1 = "https://collectionapi.metmuseum.org/public/collection/v1"
CONNECTION = sqlite3.connect("the_met.db")
CURSOR = CONNECTION.cursor()

def object_insert(vals):
    f = ["id", "title", "artist", "date", "classification", "medium", "country",
         "culture", "region", "subregion", "primary_image", "addtl_images"]
    o = "object_"
    fields = [f"{o}{i}" for i in f]
    sql = ("INSERT INTO objects("+", ".join(fields)+") "
           "VALUES("+(len(f)*"?, ")[:-2]+")")
    CURSOR.execute(sql, (vals))
    CONNECTION.commit()

def del_obj_id(obj_id, json_fpath):
    with open(json_fpath, "r+") as json_file:
        tmp_objects = json.load(json_file)
        tmp_objects.remove(obj_id)
        json_file.seek(0)
        json.dump(tmp_objects, json_file)
        json_file.truncate()

@sleep_and_retry
@limits(calls=795, period=10)
def req_met_object(obj_id):
    return requests.get(f"{MET_API_V1}/objects/{obj_id}")

def main():
    json_fpath = "./object_ids.json"
    try:
        with open(json_fpath, "r") as json_file:
            all_objects = json.load(json_file)
        all_objects.sort()
    except FileNotFoundError:
        all_objects = json.loads(
            requests.get(f"{MET_API_V1}/objects?departmentIds=9|11|15|16|19|21").text)["objectIDs"]
        all_objects.sort()
        with open(json_fpath, "w") as json_file:
            json.dump(all_objects, json_file)
    vals = []
    for obj_id in all_objects:
        try:
            res = req_met_object(obj_id)
        except requests.exceptions.RequestException as err:
            print(f"[{datetime.now()}] {err}")
            sleep(25)
            continue
        json_obj = json.loads(res.text)
        # who cares if there isn't an image to look at
        if not json_obj["primaryImage"]:
            del_obj_id(obj_id, json_fpath)
            continue
        vals = [
            str(json_obj["objectID"]),
            json_obj["title"],
            json_obj["artistDisplayName"],
            json_obj["objectDate"],
            json_obj["classification"],
            json_obj["medium"],
            json_obj["country"],
            json_obj["culture"],
            json_obj["region"],
            json_obj["subregion"],
            json_obj["primaryImage"],
            ",".join(json_obj["additionalImages"]),
        ]
        object_insert(vals)
        del_obj_id(obj_id, json_fpath)

if __name__ == "__main__":
    main()
