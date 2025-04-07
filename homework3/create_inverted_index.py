import os

input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework2/result")
inverted_index_file = "inverted_index.txt"

#проходимся по всей папке с токенами и леммами из предыдущего дз, оставляем только файлы с леммами
def get_lemma_files(directory):
    return [f for f in os.listdir(directory) if f.startswith('lemmas_') and f.endswith('.txt')]

#достаем название исходного документа(название это то что после префикса lemmas_)
def extract_doc_name(filename):
    return filename[len('lemmas_'):]


def read_lemmas_from_file(filepath):
    lemmas = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                # первая слово в файле с леммами — это лемма, дальше идут токены
                lemmas.append(parts[0])
    return lemmas

def build_inverted_index(lemma_files):
    inverted_index  = {}

    for file in lemma_files:
        doc_name = extract_doc_name(file)
        lemmas = read_lemmas_from_file(os.path.join(input_folder, file))

        for lemma in lemmas:
            if lemma not in inverted_index :
                inverted_index [lemma] = set()
            inverted_index[lemma].add(doc_name)

    return inverted_index


def save_index_to_file(index, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for lemma in sorted(index):
            f.write(f"{lemma}: {', '.join(index[lemma])}\n")



lemma_files = get_lemma_files(input_folder)
inverted_index = build_inverted_index(lemma_files)
save_index_to_file(inverted_index, inverted_index_file)
print("Создан инвертированный индекс")