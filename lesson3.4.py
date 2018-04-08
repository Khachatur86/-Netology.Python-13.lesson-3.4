import requests
from urllib.parse import urlencode


def get_url(client_id):
    url_token = "https://oauth.yandex.ru/authorize"
    params = {
        'response_type': 'token',
        'client_id': client_id
    }
    return '?'.join([url_token, urlencode(params)])


print(get_url('210a729158c74fbd9c2d0bfbe878f6d6'))

token = "AQAAAAAGLkEbAATsD9UIIuukVUwugYcDlaOKwcU"


class YaMetrikaManage:
    url = 'https://api-metrika.yandex.ru/management/v1/'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Authorization': f'OAuth{self.token}'}

    def get_counter_list(self):
        headers = self.get_headers()
        response = requests.get(
            self.url + 'counters',
            headers=headers)
        return response.json()['counters']

    def get_counter_info(self, counter_id):
        headers = self.get_headers()
        response = requests.get(
            self.url + 'counter/{}'.format(counter_id),
            headers=headers)
        return response.json()


class YaMetrikaCounter(YaMetrikaManage):
    url = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, token, counter_id, date1='today', date2='today'):
        self.counter_id = counter_id
        self.date1 = date1
        self.date2 = date2
        super().__init__(token)

    def visits(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:visits',
            'date1': self.date1,
            'date2': self.date2
        }
        response = requests.get(self.url, params, headers=headers)
        return response.json()['data'][0]['metrics'][0]

    def users(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:users',
            'date1': self.date1,
            'date2': self.date2
        }
        response = requests.get(self.url, params, headers=headers)
        return response.json()['data'][0]['metrics'][0]

    def pageviews(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:pageviews',
            'date1': self.date1,
            'date2': self.date2
        }
        response = requests.get(self.url, params, headers=headers)
        return response.json()['data'][0]['metrics'][0]


if __name__ == '__main__':

    print(f"Мой сайт - {'https://Khachatur86.github.io'}")
    metrika_manage = YaMetrikaManage("AQAAAAAGLkEbAATsD9UIIuukVUwugYcDlaOKwcU")

    for i in metrika_manage.get_counter_list():
        counter = YaMetrikaCounter(metrika_manage.token, i['id'], '2018-02-25')
        print(f'Количество визитов - {counter.visits()}')
        print(f'Количество просмотров - {counter.pageviews()}')
        print(f'Количество посетителей - {counter.users()}')
