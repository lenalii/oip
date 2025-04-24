import os
import math
from collections import defaultdict

input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework2/result")
output_folder = "result"
os.makedirs(output_folder, exist_ok=True)

def load_tokens(file_path):
    with open(file_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_lemmas(file_path):
    lemma_dict = defaultdict(list)
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) > 1:
                lemma, tokens = parts[0], parts[1:]
                lemma_dict[lemma].extend(tokens)
    return lemma_dict

# вычисляем tf для токенов
def compute_tf(term_list, all_tokens):
    total_terms = len(all_tokens)
    tf = defaultdict(int)
    for term in term_list:
        tf[term] = all_tokens.count(term)
    return {term: freq / total_terms for term, freq in tf.items() if total_terms > 0}

# вычисляем tf для лемм
def compute_lemma_tf(lemma_dict, all_tokens):
    total_terms = len(all_tokens)
    tf = {}
    for lemma, tokens in lemma_dict.items():
        freq = sum(all_tokens.count(tok) for tok in tokens)
        tf[lemma] = freq / total_terms if total_terms > 0 else 0
    return tf

# вычисляем idf
def compute_idf(term_documents, total_docs):
    idf = {}
    for term, docs in term_documents.items():
        idf[term] = math.log(total_docs / (1 + len(docs)))
    return idf


token_files = sorted([f for f in os.listdir(input_folder) if f.startswith("tokens_")])
lemma_files = sorted([f for f in os.listdir(input_folder) if f.startswith("lemmas_")])

term_doc_occurrences = defaultdict(set)
lemma_doc_occurrences = defaultdict(set)
all_token_data = []
all_lemma_data = []

for i, (token_file, lemma_file) in enumerate(zip(token_files, lemma_files)):
    doc_id = i + 1
    tokens = load_tokens(os.path.join(input_folder, token_file))
    lemmas = load_lemmas(os.path.join(input_folder, lemma_file))

    all_token_data.append(tokens)
    all_lemma_data.append(lemmas)

    for term in set(tokens):
        term_doc_occurrences[term].add(doc_id)

    for lemma, forms in lemmas.items():
        for token in forms:
            if token in tokens:
                lemma_doc_occurrences[lemma].add(doc_id)
                break

total_docs = len(all_token_data)
idf_terms = compute_idf(term_doc_occurrences, total_docs)
idf_lemmas = compute_idf(lemma_doc_occurrences, total_docs)

for i, (tokens, lemmas) in enumerate(zip(all_token_data, all_lemma_data)):
    doc_id = i + 1
    tf_terms = compute_tf(term_doc_occurrences.keys(), tokens)
    tf_lemmas = compute_lemma_tf(lemmas, tokens)

    with open(os.path.join(output_folder, f"tfidf_tokens_{doc_id}.txt"), "w", encoding="utf-8") as f_out:
        for term, tf in tf_terms.items():
            idf = idf_terms.get(term, 0)
            tfidf = tf * idf
            f_out.write(f"{term} {idf:.6f} {tfidf:.6f}\n")

    with open(os.path.join(output_folder, f"tfidf_lemmas_{doc_id}.txt"), "w", encoding="utf-8") as f_out:
        for lemma, tf in tf_lemmas.items():
            idf = idf_lemmas.get(lemma, 0)
            tfidf = tf * idf
            f_out.write(f"{lemma} {idf:.6f} {tfidf:.6f}\n")