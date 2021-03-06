#!/usr/bin/env python

import json

from tqdm import tqdm
from transliterate import translit

import db

from transliteration import transliterate

import fuzzy


soundex = fuzzy.Soundex(4)


def update_entry(entry: dict) -> dict:
    name = entry["PaxName"].split()

    # Get name.
    entry["PassengerLastName"] = name[0] if len(name) >= 1 else ""
    entry["PassengerFirstName"] = name[1] if len(name) >= 2 else ""
    entry["PassengerSecondName"] = name[2] if len(name) >= 3 else ""
    entry['PassengerFirstName_en'] = transliterate(entry['PassengerFirstName']).replace("'",'').upper()
    entry['PassengerSecondName_en'] = transliterate(entry['PassengerSecondName']).replace("'",'').upper()
    entry['PassengerLastName_en'] = transliterate(entry['PassengerLastName']).replace("'",'').upper()
    entry['PassengerFirstName_sx'] = soundex(entry['PassengerFirstName_en'])
    entry['PassengerSecondName_sx'] = soundex(entry['PassengerSecondName_en'])
    entry['PassengerLastName_sx'] = soundex(entry['PassengerLastName_en'])

    # Transliterate name.
    entry["PassengerFirstName_en"] = translit(entry["PassengerFirstName"], "ru", reversed=True).replace("'", "").upper()
    entry["PassengerSecondName_en"] = (
        translit(entry["PassengerSecondName"], "ru", reversed=True).replace("'", "").upper()
    )
    entry["PassengerLastName_en"] = translit(entry["PassengerLastName"], "ru", reversed=True).replace("'", "").upper()

    return entry


def parse_line(line: str, lengths: list, use_magic: bool = False) -> list:
    if use_magic:
        magic = 0

    s = []

    for length in lengths:
        val = line[0:length].strip()

        if val == "":
            if use_magic:
                val = f"magic{magic}"
                magic += 1

        s.append(val)
        line = line[length:]

    return s


def parse_tab(filepath: str = None) -> None:
    if not filepath:
        with open("scripts/config.json", "r") as readfile:
            filepath = json.load(readfile)["data_dir"] + "/" + "Sirena-export-fixed.tab"

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lengths = []
    sum_lengths = 0

    for i in range(0, len(lines[0]) - 1, 6):
        if lines[0][i - 1] == " " and lines[0][i] != " ":
            lengths.append(i - sum_lengths)
            sum_lengths = i
        elif lines[1][i - 1] == " " and lines[1][i] != " ":
            lengths.append(i - sum_lengths)
            sum_lengths = i

    # Fix last line.
    lengths.append(i - sum_lengths)

    keys = parse_line(lines[0], lengths, use_magic=True)

    for line in tqdm(lines[1:]):
        entry = {}
        vals = parse_line(line, lengths)

        for i in range(len(vals)):
            entry[keys[i]] = vals[i]

        new_entry = update_entry(entry)

        db.sirena.insert_one(new_entry)


if __name__ == "__main__":
    parse_tab()
