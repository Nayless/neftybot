import requests
from bs4 import BeautifulSoup
import threading


headers = {
    "accept": "*/*",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36'
}


def find_cards(): #Находит все карты

    global headers

    page_num = 1
    page_quantity = 1
    url = 'https://neftyblocks.com/drops?page=' + str(page_num)
    req = requests.get(url, headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    page_trigger = True
    all_cards = soup.find_all(class_="card card--transparent")
    sorted_cards = {}

    while page_num <= page_quantity:

        if page_trigger:
            page_quantity = number_of_pages(soup)
            page_trigger = False
        page_num += 1

        for card in all_cards:
            if card.find(class_="price price--free") and not card.find(class_="card-secure"):
                name = card.find("h3").text
                quantity = card.findAll('p')[1].text
                link = 'https://neftyblocks.com' + card.find('a').get('href')
                countdown = card.find('span', class_='countdown')
                sorted_cards[name] = link, quantity, countdown

        write_down(ascii(sorted_cards))


def number_of_pages(soup): #Ищет общее количество страниц
    num_contains = ascii(soup.find('span', attrs={'data-v-21c983b2': True}).text)
    return int(num_contains[len(num_contains)-2])


def write_down(sorted_cards): #Записывает в файл вывода карты, которые ранее не выводились
    to_write = {}

    with open('old.txt', 'w+') as file:
        old = file.read()
        for key, value in sorted_cards.items():
            if old.get(key) == 'None':
                to_write[key] = value
        file.write(old.update(to_write))
    with open('card.txt', 'w') as file:
        file.write(to_write)


def main():
    pass


if __name__ == "__main__":
    find_cards()


