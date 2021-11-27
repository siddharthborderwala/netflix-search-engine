import time
import csv
import contractions
import pandas as pd
from util import remove_puncts


def get_rows(file_path):
    """
    Read documents from csv file and return a list of dictionaries containing show information.
    Fixes contractions and makes all words lowercase.

    :param file_path: path to csv file
    :return: list of documents
    """
    rows = []
    with open(file_path, "r", encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append({
                "id": row["show_id"][1:],
                "title": remove_puncts(row["title"].lower()),
                "type": remove_puncts(row["type"].lower()),
                "directors": ",".join(list(map(lambda x: remove_puncts(x.strip().lower()), row["director"].split(",")))),
                "actors": ",".join(list(map(lambda x: remove_puncts(x.strip().lower()), row["cast"].split(",")))),
                "release_year": row["release_year"],
                "duration": row["duration"].lower(),
                "categories": ",".join(list(map(lambda x: remove_puncts(x.strip().lower()), row["listed_in"].split(",")))),
                "plot": remove_puncts(contractions.fix(row["plot"].lower())),
            })
    return rows


def store_rows(rows, file_path):
    """
    Store documents in csv file.

    :param rows: list of documents
    :param file_path: path to csv file
    """
    df = pd.DataFrame(rows)
    df.fillna('', inplace=True)
    df.drop_duplicates(inplace=True)
    rows = df.to_dict('records')
    with open(file_path, "w", encoding="UTF-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=df.columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    print("Cleaning raw csv data")
    start_time = time.time()
    store_rows(get_rows("data/raw/netflix.csv"), "data/processed/clean.csv")
    print('Data cleaned in {:.2f}s.'.format(time.time() - start_time))
