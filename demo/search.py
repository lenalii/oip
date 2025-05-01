import os
from collections import defaultdict
from pymorphy2 import MorphAnalyzer
import numpy as np
from nltk import word_tokenize

# это папка в которой хранится tfidf_lemmas для каждого файла
input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework4/result")

inverted_index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework3/inverted_index.txt")

morph = MorphAnalyzer()

# читаем tf-idf
# all_terms - это сет всех лемм
# doc_vectors - в нем храним для каждого документа номер документа и tf-idf для каждой его леммы
def load_tfidf_documents(input_folder):
    doc_vectors = {}
    all_terms = set()

    for filename in os.listdir(input_folder):
        if filename.startswith("tfidf_lemmas_") and filename.endswith(".txt"):
            doc_id = filename.split("_")[-1].split(".")[0]
            vector = {}
            with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        term, idf, tfidf = parts
                        vector[term] = float(tfidf)
                        all_terms.add(term)
            doc_vectors[doc_id] = vector

    return doc_vectors, sorted(all_terms)

# читаем инвертированный индекс в нем формат: лемма: файлы
def load_inverted_index(index_path):
    inverted_index = defaultdict(set)
    with open(index_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(": ")
            if len(parts) == 2:
                lemma = parts[0]
                documents = parts[1].split(", ")
                documents = [doc.replace(".txt", "") for doc in documents]
                inverted_index[lemma].update(documents)
    return inverted_index

# нормализация вектора
def normalize_vector(vector, all_terms):
    norm_vector = np.zeros(len(all_terms))
    term_index = {term: idx for idx, term in enumerate(all_terms)}
    for term, value in vector.items():
        if term in term_index:
            norm_vector[term_index[term]] = value
    return norm_vector

# лемматизация запроса пользователя
def lemmatize_query(query):
    tokens = word_tokenize(query.lower(), language="russian")
    lemmas = []
    for token in tokens:
        parsed = morph.parse(token)[0]
        lemmas.append(parsed.normal_form)
    return lemmas

# Построение вектора запроса
def build_query_vector(query_lemmas, all_terms):
    vector = defaultdict(float)
    for lemma in query_lemmas:
        if lemma in all_terms:
            vector[lemma] += 1.0
    return vector

def load_doc_links(index_file_path):
    doc_links = {}
    with open(index_file_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                doc_id, url = parts
                doc_links[doc_id] = url
    return doc_links

doc_links = load_doc_links(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework1/index.txt"))

# поиск релевантных документов
def search(query, doc_vectors, all_terms, inverted_index, top_n=10):
    # лемматизация запроса пользователя
    query_lemmas = lemmatize_query(query)

    # строим вектор запроса
    query_vector_dict = build_query_vector(query_lemmas, all_terms)
    query_vector = normalize_vector(query_vector_dict, all_terms)

    # из инвертированного индекса достаем доки в которых есть леммы из запроса пользователя
    candidate_docs = set()
    for lemma in query_lemmas:
        candidate_docs.update(inverted_index.get(lemma, set()))

    if not candidate_docs:
        print("Нет документов, содержащих запрос.")
        return []

    # в нем хранится для каждого документа из candidate_docs, номер документа и косинусное сходство с вектором запроса
    similarities = []

    for doc_id in candidate_docs:
        doc_vector_dict = doc_vectors[doc_id]
        doc_vector = normalize_vector(doc_vector_dict, all_terms)

        # считаем косинусное сходство
        if np.linalg.norm(doc_vector) == 0 or np.linalg.norm(query_vector) == 0:
            similarity = 0
        else:
            similarity = np.dot(query_vector, doc_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(doc_vector))
        similarities.append({
            "filename": doc_id + ".txt",
            "relevance": round(similarity, 4),
            "url": doc_links.get(doc_id, "#"),
            "download_url": f"/download/{doc_id}.txt"
        })

    similarities.sort(key=lambda x: x["relevance"], reverse=True)
    return similarities[:top_n]