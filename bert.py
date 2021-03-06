from sklearn.metrics import pairwise
from sentence_transformers import SentenceTransformer
import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
import glob
import re
from sklearn.metrics.pairwise import cosine_similarity
import csv
import os.path
import os
import configparser
import json
from config import FilesConfig
import sys
from config import CSVColumnConfig

sbert_model = SentenceTransformer("bert-base-nli-mean-tokens")  # Model being loaded...


def cosine_similarity_score(doc_id, similarity_matrix, matrix):
    # Finding similarity if Cosine similarity is chosen
    if matrix == "Cosine Similarity":
        similar_ix = np.argsort(similarity_matrix[doc_id])[::-1]
    for ix in similar_ix:
        if ix == doc_id:
            continue
        return similarity_matrix[doc_id][ix]


def bert(text):
    text = text
    csv_filename = "Similarity_bert.csv"
    with open(csv_filename, "a") as trail_csvFile:
        file_exists = os.path.isfile(csv_filename)
        row_dict = {}
        colum_alias_dict = eval(CSVColumnConfig.colum_alias_dict)
        column_names = CSVColumnConfig.csv_column_names
        csv_writer = csv.DictWriter(trail_csvFile, fieldnames=column_names)
        if not file_exists:
            csv_writer.writeheader()
        row_dict["Sno"] = text
        try:
            config = configparser.ConfigParser()
            config.read("listnames_as_tuple.ini")
            all_the_lists = config.items("lists")
            for list_name, list_values in all_the_lists:
                text_compared_with = list_values
                similariy_finder = [text, text_compared_with]
                documents_df = pd.DataFrame(
                    similariy_finder, columns=["similariy_finder"]
                )
                # removing stopwords and cleaning the text...
                stop_words_l = stopwords.words("english")
                documents_df["documents_cleaned"] = documents_df.similariy_finder.apply(
                    lambda x: " ".join(
                        re.sub(r"[^a-zA-Z]", " ", w).lower()
                        for w in x.split()
                        if re.sub(r"[^a-zA-Z]", " ", w).lower() not in stop_words_l
                    )
                )
                # creating vector using the loaded model...
                document_embeddings = sbert_model.encode(
                    documents_df["documents_cleaned"]
                )
                pairwise_similarities = cosine_similarity(document_embeddings)
                score = cosine_similarity_score(
                    0, pairwise_similarities, "Cosine Similarity"
                )
                if list_name == "informationsecurity":
                    score_IS = score
                row_dict[colum_alias_dict[list_name]] = score
            csv_writer.writerow(row_dict)
        except Exception as ex:
            print(ex)
            # appending the error message along with the url to a text file
            with open(save_not_crawled, "a") as filehandle:
                filehandle.write("%s\n" % sno + "\n" + str(ex) + "\n")
                pass  # skip

    return score_IS