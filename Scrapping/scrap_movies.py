from scrap_a_movie import scrap_a_movie
import requests
from bs4 import BeautifulSoup
import os

urls = []

current_folder = os.path.dirname(__file__)
list_url = os.path.join(current_folder, "top.html")
with open(list_url, 'r', encoding='utf-8') as file:
    content = file.read()
soup = BeautifulSoup(content, "html.parser")
links = soup.find_all('a', class_='ipc-title-link-wrapper')
urls = [link['href'] for link in links if 'href' in link.attrs]

for url in urls:
    print(scrap_a_movie(url))