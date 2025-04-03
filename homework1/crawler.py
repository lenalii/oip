import os
import requests
from bs4 import BeautifulSoup
import re
import time

base_url = "https://habr.com/ru/companies/bothub/news/"
output_folder = "homework1/files"
index_file = "homework1/index.txt"
max_pages = 150

os.makedirs(output_folder, exist_ok=True)

def download_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return None

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # убираем css js и другие ссылки
    for tag in soup.find_all(["style", "script", "link"]):
        tag.decompose()

    return str(soup)


valid_link_pattern = re.compile(r"^/ru/companies/bothub/news/\d+/$")

def extract_article_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if valid_link_pattern.match(href):
            full_url = f"https://habr.com{href}"
            links.add(full_url)
            continue
    return list(links)

def get_links(base_url):
    to_visit=[]
    for i in range (1,10):
        html = download_page(f"{base_url}page{i}/")
        article_links = extract_article_links(html)
        to_visit.extend(article_links)
        time.sleep(2)
    return to_visit


def crawl_habr_news(base_url, max_pages):
    to_visit = get_links(base_url)
    visited = set()
    page_count = 0
    with open(index_file, "w", encoding="utf-8") as index:
        while to_visit and page_count < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue

            print(f"Обработка {url}")
            html = download_page(url)
            if not html:
                continue

            cleaned_html = clean_html(html)
            file_name = f"{page_count + 1}.txt"
            file_path = os.path.join(output_folder, file_name)

            with open(file_path, "w", encoding="utf-8") as output:
                output.write(cleaned_html)

            index.write(f"{page_count + 1} {url}\n")
            visited.add(url)
            page_count += 1

crawl_habr_news(base_url, max_pages)