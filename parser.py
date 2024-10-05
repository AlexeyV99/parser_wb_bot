import requests
import csv
import datetime

ITEM = 'Высокие кроссовки для девочки'
NUMBER = 5

ITEMS = []


def create_csv():
    uniq_file_name = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
    uniq_file_name = f'parse_wb_{uniq_file_name}.csv'
    with open(uniq_file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ссылка', 'название', "рейтинг", "цена"])
    return uniq_file_name


def save_csv(item, file_name):
    with open(file_name, 'a', newline='', encoding='cp1251') as file:
        writer = csv.writer(file)
        writer.writerow([item['link'],
                         item['name'],
                         item['rating'],
                         item['price'],
                         ])


def find_item(response, file_name, number):
    # time.sleep(1)
    # global NUMBER
    global ITEMS
    for index, value in enumerate(response.json()['data']['products']):
        if number <= 0:
            return True
        try:
            print(f'{number} {value['id']}: {value['name']}: рейтинг: {value['reviewRating']}: цена: '
                  f'{value['sizes'][0]['price']['total'] / 100}')
            i_value = {
                'link': f"https://www.wildberries.ru/catalog/{value['id']}/detail.aspx",
                'name': value['name'],
                'rating': value['reviewRating'],
                'price': value['sizes'][0]['price']['total'] / 100,
            }
            save_csv(i_value, file_name)
            number -= 1
        except Exception as e:
            print(f'!!! ERROR !!! {e}')


def get_page(file_name: str, item: str, number: int = 5):
    # global NUMBER = number
    page = 1
    while True:
        print(f'Страница: {page}')
        params = {
            'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'query': item,
            'resultset': 'catalog',
            'sort': 'rate',
            'spp': '30',
            'suppressSpellcheck': 'false',
            'page': str(page),
        }
        while True:
            response = requests.get('https://search.wb.ru/exactmatch/ru/common/v7/search', params=params)
            if response.status_code == 200:
                break
        # with open('json.json', 'w', encoding='utf-8') as file:
        #     json.dump(response.json(), file)

        if len(response.json()) != 0:
            result = find_item(response, file_name, number)
            if result:
                return (page - 1) * 100 + result
        else:
            return None

        page += 1
        number -= 100


def main():
    file_name = create_csv()
    get_page(file_name, ITEM)


if __name__ == '__main__':
    main()
