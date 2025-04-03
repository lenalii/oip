import os
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
nltk.download('punkt_tab')

stop_words = set(stopwords.words("russian"))

input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework1/files")
output_folder = "result"
os.makedirs(output_folder, exist_ok=True)

morph = MorphAnalyzer()

#убираем html разметку, и все лишние символы, оставляем только буквы
def clean_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ")

    text = re.sub(r"[^а-яёА-ЯЁ\s]", "", text)
    text = text.lower()
    return text.strip()

#токенезация
def tokenize_text(text):
    tokens = word_tokenize(text, language="russian")
    filtered_tokens = set()
    for token in tokens:
        if token not in stop_words:
            filtered_tokens.add(token)
    return list(filtered_tokens)

#лемматизация
def lemmatize_tokens(tokens):
    lemmas = {}
    for token in tokens:
        parsed = morph.parse(token)[0]
        lemma = parsed.normal_form
        if lemma not in lemmas:
            lemmas[lemma] = []
        lemmas[lemma].append(token)
    return lemmas


for file_name in os.listdir(input_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_folder, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        clean_content = clean_text(html_content)

        tokens = tokenize_text(clean_content)
        lemmas = lemmatize_tokens(tokens)

        tokens_file_name = f"tokens_{file_name}"
        tokens_file_path = os.path.join(output_folder, tokens_file_name)
        with open(tokens_file_path, "w", encoding="utf-8") as tokens_file:
            for token in tokens:
                tokens_file.write(f"{token}\n")

        lemmas_file_name = f"lemmas_{file_name}"
        lemmas_file_path = os.path.join(output_folder, lemmas_file_name)
        with open(lemmas_file_path, "a", encoding="utf-8") as lemmas_file:
            for lemma, tokens_list in lemmas.items():
                tokens_str = " ".join(tokens_list)
                lemmas_file.write(f"{lemma} {tokens_str}\n")

        print(f"Обработан файл: {file_name}")

print("Обработка завершена.")