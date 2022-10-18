import requests
from bs4 import BeautifulSoup

domain = "https://oriencoop.cl"
slug = "sucursales.htm"

response = requests.get(domain + '/' + slug)
soup = BeautifulSoup(response.text, 'lxml')

cities_links = []

for link in soup.select('.content .c-list .sub-menu a'):
    cities_links.append(domain + link.get('href'))

print(cities_links)