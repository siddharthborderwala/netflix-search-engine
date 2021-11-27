import csv
import time
import gensim
import pandas as pd

model = gensim.models.doc2vec.Doc2Vec(vector_size=100, min_count=1, epochs=50)


if __name__ == '__main__':
    print("Training model using doc2vec model")
    start = time.time()
    rows = pd.read_csv("data/processed/clean.csv", encoding="UTF-8")
    corpus = []
    for row in rows.itertuples():
        tokens = gensim.utils.simple_preprocess(row.plot)
        corpus.append(gensim.models.doc2vec.TaggedDocument(tokens, [row.id]))
    print(len(corpus))
    model.build_vocab(corpus)
    model.save("models/doc2vec.model")
    print(len(model.dv))
    print("Created model in {:.2f}s.".format(time.time() - start))
