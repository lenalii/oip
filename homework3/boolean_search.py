import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def load_inverted_index(filepath):
    inverted_index = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                term, docs = line.strip().split(':', 1)
                inverted_index[term.strip()] = set(doc.strip() for doc in docs.split(',') if doc.strip())
    return inverted_index

def lemmatize_token(token):
    return morph.parse(token)[0].normal_form

def query_to_eval_string(query, index, all_docs):
    tokens = query.replace('(', ' ( ').replace(')', ' ) ').split()
    result = '('

    for token in tokens:
        upper = token.upper()
        if upper == 'AND':
            result += ').intersection('
        elif upper == 'OR':
            result += ').union('
        elif upper == 'NOT':
            result += ').difference('
        elif token == '(':
            result += '('
        elif token == ')':
            result += ')'
        else:
            lemma = lemmatize_token(token)
            result += str(index.get(lemma, set()))

    result += ')'
    return result

def boolean_search(query, index):
    all_docs = set()
    for docs in index.values():
        all_docs.update(docs)

    expr = query_to_eval_string(query, index, all_docs)
    return eval(expr)


index = load_inverted_index('inverted_index.txt')
print("Загружен инвертированный индекс.")

while True:
    query = input()
    if query.lower() == 'exit':
        break
    try:
        result = boolean_search(query, index)
        print("Найдено в документах:", ", ".join(sorted(result)) if result else "Ничего не найдено.")
    except Exception as e:
        print("Ошибка в запросе:", e)