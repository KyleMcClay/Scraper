from langdetect import detect_langs


def is_english(string):
    res = detect_langs(string)
    for item in res:
        if item.lang == "en":
            return True
    return False

"""
print(is_english("Bonjour"))
print(is_english("The quick brown fox"))
print(is_english("toriţi-vă şi o să regretaţi;nu vă căsătoriţi,şi o să"))
"""