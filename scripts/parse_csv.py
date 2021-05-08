#!/usr/bin/env python

import json

from tqdm import tqdm

import db


def update_entry(entry: dict) -> dict:
    return entry


def parse_csv(filepath: str = None) -> None:
    if not filepath:
        with open("config.json", "r") as readfile:
            filepath = json.load(readfile)["data_dir"] + "/" + "BoardingData.csv"

    with open(filepath, "r") as f:
        lines = f.readlines()

    dummy = {}

    for key in lines[0].split(";"):
        dummy[key.strip()] = ""

    for line in tqdm(lines[2:]):
        values = line.split(";")

        entry = dummy.copy()

        for k, key in enumerate(entry.keys()):
            entry[key] = values[k].strip()

        entry = update_entry(entry)

        db.boarding_data.insert_one(entry)


if __name__ == "__main__":
    parse_csv()
