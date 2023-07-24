import requests
import json
import re
import time
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime


ua = UserAgent()
headers = {'User-Agent': ua.ff}

def get_dict_data(page:int=3) -> dict:
    data_dict = {}
    counter = 1
    count = 0
    while count < page:
        # time.sleep(1)
        url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={}'.format(count)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='serp-item')
        for item in data:
            salary = item.find('span', class_='bloko-header-section-3')
            if salary:
                salary = salary.text.replace('\u202f', '').replace('\u2013', '\u002d')
            else:
                salary = 'not specified'
            description = item.find('a', class_= 'serp-item__title').text
            company_name = item.find('div', class_='vacancy-serp-item__meta-info-company').text
            city_name = item.find('div', {'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'}).text
            link = item.find('a', class_='serp-item__title').get('href')
            if match_pattern(link):
                if description not in data_dict:
                    description = description
                else:
                    description = description + str(counter)
                    counter += 1
                data_dict[description] = {'link': link, 'name': company_name, 'city': city_name, 'salary': salary }

        count += 1
        
    return data_dict

def match_pattern(link:str) -> bool:
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    vacancy_description = soup.find('div', class_='vacancy-section').text
    pattern = r"(.*([Dd]jango).*([Ff]lask).*)|(.*([Ff]lask).*([Dd]jango).*)" 
    res = re.search(pattern, vacancy_description)
    if res:
        return True
    return False

def logger(*args, **kwargs):
    def __logger(old_function):
        data_dict = {}
        def new_function(*args, **kwargs):
            start = datetime.now()
            result = old_function(*args, **kwargs)
            stop = datetime.now()
            data_dict['name_func'] = '{}'.format(old_function.__name__)
            data_dict['execution_time'] = str(stop - start)
            data_dict['result'] = result
            with open('/home/andrey/net_task4_pr/main3.log', 'w') as f:
                json.dump(data_dict, f, ensure_ascii=False)
            return result
        return new_function
    return __logger


if __name__ == '__main__':
    some_logger = logger()
    get_dict_data = some_logger(get_dict_data)
    get_dict_data(page=1)







