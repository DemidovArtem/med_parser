from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import time

class Address:
    def __init__(self, city, address, worktime, phone, metro):
        self.city = city
        self.address = address
        self.worktime = worktime
        self.phone = phone
        self.metro = metro

class Service:
    def __init__(self, category, title, price):
        self.category = category
        self.title = title
        self.price = price

def address_data():
    resp = req.get("https://spb.klinikabudzdorov.ru/kliniki/klinika-v-sankt-peterburge/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"})
    addresses = []
    soup = BeautifulSoup(resp.text, 'lxml')
    for address_item, worktime_item, phone_item in zip(soup.find_all('div', 'contacts-information-content'), soup.find_all('div', 'contacts-work-time'), soup.find_all('div', 'contacts-phone')):
        address = address_item.get_text(separator=";", strip=True)
        address, metro = address.split(";")
        worktime = worktime_item.get_text(strip=True)[13:]
        phone = phone_item.get_text(strip=True)[6:]
        addresses.append(Address("г. Санкт-Петербург", address, worktime, phone, metro))
    data = [[addresses[i].city, addresses[i].address, addresses[i].worktime, addresses[i].phone, addresses[i].metro]
            for i in range(len(addresses))]
    df = pd.DataFrame(data=data, columns=['Город', 'Адрес', 'Часы работы', 'Контактный телефон', 'Станция метро'])
    df.to_csv('Адреса.csv', encoding='utf-8-sig')

def analysis_data():
    resp = req.get("https://spb.klinikabudzdorov.ru/uslugi/analizy/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"})
    urls = []

    soup = BeautifulSoup(resp.text, 'lxml')
    for item in soup.find_all('a', "b-analysis-types__item"):
        url = f"https://spb.klinikabudzdorov.ru{item.get('href')}"
        urls.append(url)
    services = []
    for url in urls:
        resp = req.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"})
        soup = BeautifulSoup(resp.text, 'lxml')
        group = soup.find("h1", 'oxo-h1').get_text(strip=True)
        for title_item, price_item in zip(soup.find_all('a', 'catalog-section-item-name-wrapper intec-cl-text-hover'), soup.find_all('span', {"data-role":'item.price.discount'})):
            price = price_item.get_text()[1:-6]
            title = title_item.get_text()
            service = Service(group, title, price)
            services.append(service)

    data = [
        [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), services[i].title, services[i].category,
         '', services[i].price, 'БудьЗдоров'] for i in range(len(services))]

    df = pd.DataFrame(data,
                      columns=['Дата', 'Наименование', 'Группа', 'Код', 'Стоимость услуги', 'Наименование лаборатории'])
    df.to_csv('Анализы.csv', encoding='utf-8-sig')

if __name__ == '__main__':
    address_data()
    analysis_data()