#!/usr/bin/env python

import json

from tqdm import tqdm

import db


def update_entry(entry: dict) -> dict:
    return entry


def parse_json(filepath: str = None) -> None:
    if not filepath:
        with open("config.json", "r") as readfile:
            filepath = json.load(readfile)["data_dir"] + "/" + "FrequentFlyerForum-Profiles.json"

    with open(filepath, "r") as readfile:
        data = json.load(readfile)

    for client in tqdm(data["Forum Profiles"]):
        client = update_entry(client)

        db.frequent_flyers.insert_one(client)


if __name__ == "__main__":
    parse_json()
