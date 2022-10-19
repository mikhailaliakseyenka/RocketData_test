import json

import requests
from bs4 import BeautifulSoup


def parsing_links_cities():  # достаю ссылку для каждого города
    domain = "https://oriencoop.cl"
    slug = "sucursales.htm"

    response = requests.get(domain + '/' + slug)
    soup = BeautifulSoup(response.text, 'lxml')

    cities_links = []

    for link in soup.select('.content .c-list .sub-menu a'):
        cities_links.append(domain + link.get('href'))

    return cities_links


def information_about_citi(cities_links):
    informations = []
    for link in cities_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')

        address = soup.select_one('.s-dato p:nth-child(2) span').get_text()
        name = soup.select_one('.s-dato h3').get_text()
        phones = [soup.select_one('.s-dato p:nth-child(3) span').get_text()]
        working_hours = []
        for working_hour in soup.select('.s-dato p:nth-child(5) span'):
            working_hours.append(working_hour.get_text())

        informations.append({
            'address': address,
            'name': name,
            'phones': phones,
            'working_hours': working_hours
        })

    return informations

def print_json(data):
    with open('script1.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))

citi_links = parsing_links_cities()
data = information_about_citi(citi_links)
print_json(data)
