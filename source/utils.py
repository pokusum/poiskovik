import faiss
import numpy as np
import pandas as pd

def get_rows_from_sql(indexes, connection, useStemming):
    cursor = connection.cursor()
    subqueries = []
    processed_articles_column = 'stem_article' if useStemming else 'proc_article'

    # # Вариант для обработки нескольких запросов обновременно
    for index in indexes:
        subqueries.append(f"SELECT url, {processed_articles_column}, article FROM documents WHERE \"index\" = {index}")
    queries = [' UNION ALL '.join(subqueries[i:i + 400]) for i in range(0, len(subqueries), 400)]

    resultDataFrames = []
    for query in queries:
        cursor.execute(query)
        resultDataFrames.append(pd.DataFrame(cursor.fetchall()))
    return pd.concat(resultDataFrames)


def getVectorDB(path):
    return faiss.read_index(path)


def findVectorsIndexes(query, encoder, kDocuments, index):
    queryEmbd = encoder.encode(query, normalize_embeddings=True)
    D, I = index.search(np.array(queryEmbd), kDocuments)
    return I[:len(query)]

def get_rows_from_csv(filename, indices):
    df = pd.read_csv(
        filename,
        header=None,
        skiprows=lambda x: x not in indices
    )
    return df