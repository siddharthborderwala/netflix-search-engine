import time
import pandas as pd

from util import store_dict, soundex


def create():
    """
    Create a zonal index using show titles, actor names and director names
    The titles, actor names and director names are in 'data/clean.csv' file.

    :return: None
    """
    # clean file
    clean_file = 'data/processed/clean.csv'

    # Read the clean data
    df = pd.read_csv(clean_file, encoding='UTF-8')
    # change the na to empty string
    df.fillna('', inplace=True)

    # create a soundex index
    titles_soundex = {}
    actors_soundex = {}
    directors_soundex = {}
    categories_soundex = {}

    for r in df.itertuples(index=False):
        # title
        title = r.title.split(' ')
        i = r.id
        for word in title:
            s = soundex(word)
            if s not in titles_soundex:
                titles_soundex[s] = [(i, word)]
            else:
                titles_soundex[s].append((i, word))
        # actors
        actors = map(lambda x: x.split(' '), r.actors.split(','))
        for actor_name in actors:
            for word in actor_name:
                s = soundex(word)
                if s not in actors_soundex:
                    actors_soundex[s] = [(i, word)]
                else:
                    actors_soundex[s].append((i, word))
        # directors
        directors = map(lambda x: x.split(' '), r.directors.split(','))
        for director_name in directors:
            for word in director_name:
                s = soundex(word)
                if s not in directors_soundex:
                    directors_soundex[s] = [(i, word)]
                else:
                    directors_soundex[s].append((i, word))
        # categories
        categories = map(lambda x: x.split(' '), r.categories.split(','))
        for category in categories:
            for word in category:
                s = soundex(word)
                if s not in categories_soundex:
                    categories_soundex[s] = [(i, word)]
                else:
                    categories_soundex[s].append((i, word))

    # save the soundex index

    store_dict(titles_soundex, 'indices/titles_soundex.txt')
    store_dict(actors_soundex, 'indices/actors_soundex.txt')
    store_dict(directors_soundex, 'indices/directors_soundex.txt')
    store_dict(categories_soundex, 'indices/categories_soundex.txt')


if __name__ == '__main__':
    print("Creating indices")
    start = time.time()
    create()
    print("Indices created in {:.2f}s.".format(time.time() - start))
