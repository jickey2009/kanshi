# %%
import csv
import re

# %%



# %%
def search_kanji_by_radical(kanji_data: list[dict], radical: str) -> list[dict]:
    results = []
    for kanji in kanji_data:
        if radical in kanji['group']:
            results.append(kanji)
    return results


# %%
def search_kanji_by_reading(kanji_data: list[dict], reading: str) -> list[dict]:
    results = []
    hiragana_ptn = re.compile(r'^[ぁ-ん]+$')
    katakana_ptn = re.compile(r'^[ァ-ン]+$')
    if hiragana_ptn.match(reading):
        for kanji in kanji_data:
            for kun_reading in kanji['kunyomi'].split(','):
                if reading == kun_reading.strip():
                    results.append(kanji)
                    break
    elif katakana_ptn.match(reading):
        for kanji in kanji_data:
            for on_reading in kanji['onyomi'].split(','):
                if reading == on_reading.strip():
                    results.append(kanji)
                    break
    return results


# %%
def search_kanji_by_rhymes(kanji_data: list[dict], rhyme: str) -> list[dict]:
    results = []
    for kanji in kanji_data:
        if rhyme == kanji['rhyme']:
            results.append(kanji)
    return results


# %%
def lookup_kanji(kanji_data: list[dict], kanji_char: str) -> list[dict]:
    results = []
    for kanji in kanji_data:
        if kanji['kanji'] == kanji_char:
            results.append(kanji)
    return results


# %%
def filter_kanji_by_pingze(kanji_data: list[dict], pingze: bool) -> list[dict]:
    results = []
    for kanji in kanji_data:
        if pingze and kanji['rhyme'].startswith('p'):
            results.append(kanji)
        elif not pingze and not kanji['rhyme'].startswith('p'):
            results.append(kanji)
    return results


