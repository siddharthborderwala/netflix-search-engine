from gensim.utils import simple_preprocess
from gensim.models.doc2vec import Doc2Vec
import pandas as pd
from contractions import fix
from Levenshtein import jaro

from .util import read_dict, soundex, remove_puncts as rp

df = pd.read_csv('data/processed/clean.csv')

titles_soundex = read_dict("indices/titles_soundex.txt")
actors_soundex = read_dict("indices/actors_soundex.txt")
directors_soundex = read_dict("indices/directors_soundex.txt")
categories_soundex = read_dict("indices/categories_soundex.txt")


def get_show_data(show_id):
    data = df.fillna('').loc[int(show_id) - 1].to_dict()
    return {
        'title': data['title'],
        'type': data['type'],
        'directors': list(filter(lambda x: x.strip() != '', data['directors'].split(','))),
        'actors': list(filter(lambda x: x.strip() != '', data['actors'].split(','))),
        'categories': list(filter(lambda x: x.strip() != '', data['categories'].split(','))),
        'release_year': data['release_year'],
        'duration': data['duration'],
        'plot': data['plot']
    }


def wv_ranking(query):
    """
    Generate a ranked retrieval based on a pre-trained-cum-fine-tuned word2vec model.

    :param query: query
    :param training_documents: list of training documents
    :return: list of documents relevant to the query
    """
    model: Doc2Vec = Doc2Vec.load("models/doc2vec.model")
    print(len(model.dv))

    tokens = simple_preprocess(query)
    vector = model.infer_vector(tokens)

    return model.dv.most_similar([vector], topn=len(model.dv))


def get_matches(token, d):
    s = soundex(token)
    try:
        sx_class = d[s]
        for i, w in sx_class:
            jd = jaro(token, w)
            if jd > 0.75:
                yield (i, w, jd)
    except KeyError:
        pass


def intersect_by_id(a1, a2):
    """
    Intersect two iterables of tuples of type (id, word, distance) based on their elements id.
    Return the list of tuples.

    :param a1: list 1
    :param a2: list 2
    :return: list of intersection
    """
    a1_ids = set(map(lambda x: x[0], a1))
    a2_ids = set(map(lambda x: x[0], a2))
    return list(set(filter(lambda x: x[0] in a1_ids and x[0] in a2_ids, a1 + a2)))


def get_res_element(x):
    return {
        'id': x,
        'title': df.at[x - 1 if x != 0 else 0, 'title'],
    }


def get_results(query):
    # 1. extract the tokens
    tokens = list(filter(lambda x: x != '', map(
        lambda x: rp(fix(x.lower().strip())), query.split(' '))))

    v = {
        'title': {},
        'actors': {},
        'directors': {},
        'categories': {},
    }

    # 2. get index matches
    for token in tokens:
        v['title'][token] = list(get_matches(token, titles_soundex))
        v['actors'][token] = list(get_matches(token, actors_soundex))
        v['directors'][token] = list(get_matches(token, directors_soundex))
        v['categories'][token] = list(get_matches(token, categories_soundex))

    # 3. intersect the values based on same ids

    # intersection of all items of v['title'] based on same id
    title_intersection = v['title'][tokens[0]]
    for _, value in v['title'].items():
        title_intersection = intersect_by_id(title_intersection, value)

    # intersection of all items of v['actors'] based on same id
    actors_intersection = v['actors'][tokens[0]]
    for _, value in v['actors'].items():
        actors_intersection = intersect_by_id(actors_intersection, value)

    # intersection of all items of v['directors'] based on same id
    directors_intersection = v['directors'][tokens[0]]
    for _, value in v['directors'].items():
        directors_intersection = intersect_by_id(directors_intersection, value)

    # intersection of all items of v['categories'] based on same id
    categories_intersection = v['categories'][tokens[0]]
    for _, value in v['categories'].items():
        categories_intersection = intersect_by_id(
            categories_intersection, value)

    # 4. return the results sorted by jaro_distance (descending order)
    # and with de-duplication
    title_ids = list(set(map(lambda x: x[0], sorted(
        title_intersection, key=lambda x: x[2], reverse=True))))
    actors_ids = list(set(map(lambda x: x[0], sorted(
        actors_intersection, key=lambda x: x[2], reverse=True))))
    directors_ids = list(set(map(lambda x: x[0], sorted(
        directors_intersection, key=lambda x: x[2], reverse=True))))
    categories_ids = list(set(map(lambda x: x[0], sorted(
        categories_intersection, key=lambda x: x[2], reverse=True))))

    return {
        'title': list(map(get_res_element, title_ids)),
        'actors': list(map(get_res_element, actors_ids)),
        'directors': list(map(get_res_element, directors_ids)),
        'categories': list(map(get_res_element, categories_ids)),
        'descriptions': list(map(get_res_element, map(lambda x: x[0], wv_ranking(query)))),
    }


if __name__ == '__main__':
    import json
    print(len(titles_soundex), len(actors_soundex), len(
        directors_soundex), len(categories_soundex))
    while True:
        query = input("Query:\t")
        if query == '-1':
            break
        results = get_results(query)
        print(json.dumps(results, indent=2))
