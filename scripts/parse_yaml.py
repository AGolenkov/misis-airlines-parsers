#!/usr/bin/env python

import json

from tqdm import tqdm

import db


def update_entry(entry: dict) -> dict:
    return entry


def parse_yaml(filepath: str = None) -> None:
    if not filepath:
        with open("config.json", "r") as readfile:
            filepath = json.load(readfile)["data_dir"] + "/" + "SkyTeam-Exchange.json"

    with open(filepath, "r") as readfile:
        data = json.loads(readfile.read())

    for date in tqdm(data.keys()):
        for flight in data[date].keys():
            entry = {"date": date, "flight": flight, "ffs": []}

            for key in data[date][flight].keys():
                if key == "FF":
                    for ff in data[date][flight][key].keys():
                        fff = dict()

                        fff.update(data[date][flight][key][ff])

                        fff["PARTNER_CODE"] = ff.split(" ")[0]
                        fff["PARTNER_ID"] = ff.split(" ")[1]

                        entry["ffs"].append(fff)
                else:
                    entry[key] = data[date][flight][key]

            entry = update_entry(entry)

            db.exchange.insert_one(entry)


if __name__ == "__main__":
    parse_yaml()
