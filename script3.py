import json

import requests
import dryscrape
from bs4 import BeautifulSoup


def parsing_links_cities():  # достаю ссылку для каждого города
    domain = "https://naturasiberica.ru"
    slug = "/our-shops/"

    response = requests.get(domain + '/' + slug)
    soup = BeautifulSoup(response.text, 'lxml')

    cities_links = []

    for link in soup.select('.our-shops .card-list .card-list__item a'):
        cities_links.append(domain + link.get('href'))

    return cities_links


def information_about_citi(cities_links):
    informations = []
    for link in cities_links:
        session = dryscrape.Session()
        session.visit(link)
        response = session.body()
        soup = BeautifulSoup(response.text, 'lxml')

        information = soup.select_one('.original-shops .original-shops__info')
        address = information.select_one('.original-shops__address').get_text()
        name = information.select_one('.original-shops__city').get_text()
        phones = [information.select_one('.original-shops__phone').get_text()]
        working_hours = []
        for working_hour in information.select('.original-shops__schedule'):
            working_hours.append(working_hour.get_text())

        informations.append({
            'address': address,
            'name': name,
            'phones': phones,
            'working_hours': working_hours
        })

    return informations

def print_json(data):
    with open('script3.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))

citi_links = parsing_links_cities()
data = information_about_citi(citi_links)
print_json(data)
