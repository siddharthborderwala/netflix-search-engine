# import pandas as pd
# from spacy.pipeline import EntityRecognizer
# from spacy.training import Example
# import en_core_web_trf

# nlp = en_core_web_trf.load()


# if __name__ == '__main__':
#     docs = pd.read_csv('data/processed/clean.csv', encoding="UTF-8")

#     # train spacy ner model
#     res_list = []
#     examples = []

#     docs.fillna('', inplace=True)

#     for doc in docs.head().itertuples():
#         title = doc.title
#         actors = doc.actors.split(',')
#         directors = doc.directors.split(',')

#         t_res = nlp(title)
#         res_list.append(t_res)
#         examples.append(Example(t_res, [u'WORK_OF_ART']))

#         for actor in actors:
#             a_res = nlp(actor)
#             res_list.append(a_res)
#             examples.append(Example(a_res, [u'PERSON']))

#         for director in directors:
#             d_res = nlp(director)
#             res_list.append(d_res)
#             examples.append(Example(d_res, [u'PERSON']))

#     ner = nlp.get_pipe("ner")
#     ner.update(res_list, examples)

#     ner.to_disk("models/ner.spacy")
