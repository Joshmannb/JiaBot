import pandas as pd
import collections

def read_csv(file_name):
    kanji_data = pd.read_csv(file_name, encoding="shift_jis_2004")
    return kanji_data

def build_db(file_name):
    kanji_data = read_csv(file_name)
    db = dict()
    for row in kanji_data.values:
        temp = row[3].split(";")
        # db[row[0]] = [x for x in temp if x != ""]
        db[row[0]] = ';'.join([x for x in temp if x != ""])
    
    return db

def main():
    db = build_db('N5_Kanji.csv')

if __name__ == "__main__":
    main()