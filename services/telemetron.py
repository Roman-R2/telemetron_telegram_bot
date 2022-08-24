"""
https://api.telemetron.net/docs/

"""
import logging
import math
from pprint import pprint

import requests

from services import status
from settings import settings

from requests.exceptions import ConnectionError

import logging_config

# Инициализация логирования сервера.
LOGGER = logging.getLogger('server_logger')


def check_request(func):
    def worker(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            LOGGER.error(
                f'Нет соединения с сервером телеметрон. Проверьте соединение.'
                f'requests.exceptions.ConnectionError.'
            )
            exit(777)
            return None

    return worker


class TelemetronRequests:
    """ Класс служит для отправки запросов и получения ответов Telemetron
    API. """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Content-Type": "application/json",
    }

    authorization_url = 'https://api.telemetron.net/auth/'

    def __init__(self):
        self.expires_in = None
        self.access_token = None
        self.refresh_token = None
        self.vending_machines = None
        self.components = None
        # Авторизуемся
        self.__get_authorization()
        # Спарсим полученные ингредиенты
        self.__component_parser()
        # Спарсим полученный список автоматов
        self.__vending_machines_parser()
        # print('vending_machines')
        # pprint(self.vending_machines)
        # print('components')
        # pprint(self.components)
        # pprint(self.__get_planogram())
        # self.__get_vending_machine_components_capacity()
        self.union_of_capacity_and_loading = self.__get_union_of_capacity_and_loading()

    def __get_authorization(self):
        data = {
            "client_id": settings.TELEMETRON_CLIENT_ID,
            "client_secret": settings.TELEMETRON_CLIENT_SECRET,
            "grant_type": settings.TELEMETRON_GRANT_TYPE,
            "password": settings.TELEMETRON_PASSWORD,
            "scope": settings.TELEMETRON_SCOPE,
            "username": settings.TELEMETRON_LOGIN
        }

        response = self.__send_post_request(self.authorization_url, data)

        if response is not None:
            if response.status_code != status.HTTP_200_OK:
                LOGGER.error(
                    f'Запрос авторизации вернул статус не 200'
                    f'{response.status_code=}. {response.headers=} '
                    f'{response.text=}'
                )
            else:
                response_dict = response.json()
                self.expires_in = response_dict['expires_in']
                self.access_token = response_dict['access_token']
                self.refresh_token = response_dict['refresh_token']
                self.headers.update(
                    {"Authorization": f"Bearer {self.access_token}"})
                LOGGER.debug(
                    f'{__name__}: Запрос авторизации вернул ответ {response.status_code}'
                )

    def __component_parser(self):
        """ Преобразует ответ от сервера по ингредиентам в удобную
        структуру дынных для дальнейшего использования. """
        raw_components = self.__get_components()
        component_dict = {}
        for item in raw_components:
            component_dict.update({
                item['id']: (item['name'], item['units'])
            })
        # pprint(component_dict)
        self.components = component_dict
        LOGGER.debug(
            f'{__name__}: Преобразовали данные от сервера: {component_dict}'
        )

    def __vending_machines_parser(self):
        """ Преобразует ответ от сервера по автоматам в удобную
        структуру дынных для дальнейшего использования. """
        raw_vending_machines = self.__get_vending_machines()
        vending_machines = {}
        for item in raw_vending_machines:
            vending_machines.update({
                item['id']: (item['name'], item['planogram_id'], item['state'])
            })
        self.vending_machines = vending_machines
        LOGGER.debug(
            f'{__name__}: Преобразовали данные от сервера: {vending_machines}'
        )

    @check_request
    def __send_post_request(self, url, data) -> requests:
        response = requests.post(url, data=data)
        LOGGER.debug(
            f'Получили ответ {response.status_code} по url {url}'
        )
        return response

    @check_request
    def __send_get_request(self, url) -> requests:
        response = requests.get(
            url,
            headers=self.headers)
        return response

    def get_info(self):
        """
        Получит информацию о пользователе, залогиненом в Telemetron API.
        """
        url = 'https://api.telemetron.net/v2/me'
        response = self.__send_get_request(url)
        return response

    def __get_vending_machines(self):
        url = 'https://api.telemetron.net/v2/vending_machines'
        response = self.__send_get_request(url)
        return response.json()

    def __get_vending_machine_loading(self, vending_machine_id=24689):
        """ Текущий уровень загрузки торгового автомата ингредиентами. """
        url = f'https://api.telemetron.net/v2/vending_machines/{vending_machine_id}/loading'
        response = self.__send_get_request(url)
        # print(f'Загрузка автомата id {vending_machine_id}:')
        # for item in response.json():
        #     print(
        #         f'\t{self.components[item["component_id"]][0]} загружен {item["value"]} {self.components[item["component_id"]][1]}'
        #     )
        return response.json()

    def __get_components(self):
        """ Получит ингредиенты для автоматов (идентификаторы и их
        описания). """
        url = "https://api.telemetron.net/v2/components"
        response = self.__send_get_request(url)
        return response.json()

    def __get_planogram_capacity(self, planogram_id=177970):
        """ Получит планограмму загрузки ингредиентов для автомата. """
        url = f"https://api.telemetron.net/v2/planograms/{planogram_id}"
        response = self.__send_get_request(url)
        return response.json()['capacity']

    # def __get_vending_machine_components_capacity(self,
    #                                               vending_machine_id=24689):
    #     """ Получит и вернет максимальную вместимость ингредиентов
    #     в планограме по выбранному автомату. """
    #
    #     # print(
    #     #     f'{__name__}Для автомата {self.vending_machines[vending_machine_id][0]}')
    #     # pprint(self.__get_planogram_capacity(
    #     #     planogram_id=self.vending_machines[vending_machine_id][1]
    #     # ))
    #     return self.__get_planogram_capacity(
    #         planogram_id=self.vending_machines[vending_machine_id][1]
    #     )

    def __get_union_of_capacity_and_loading(self):
        """ Объедини данные по вместимости ингредиентов и текущей загрузки """
        union_ingredients_data = []
        for vending_machine_id in self.vending_machines.keys():
            # print(
            #     f'{__name__}Для автомата {self.vending_machines[vending_machine_id][0]}'
            # )
            planogram_capacity = self.__get_planogram_capacity(
                planogram_id=self.vending_machines[vending_machine_id][1]
            )
            # print('planogram_capacity=')
            # pprint(planogram_capacity)
            vending_machine_loading = self.__get_vending_machine_loading(
                vending_machine_id=vending_machine_id
            )
            # print('vending_machine_loading=')
            # pprint(vending_machine_loading)
            # print('-'*70)
            capacity_data = []
            for capacity in planogram_capacity:
                for loading in vending_machine_loading:
                    if capacity['component_id'] == loading['component_id']:
                        capacity_data.append(
                            {
                                'component_id': loading['component_id'],
                                'component_name':
                                    self.components[capacity["component_id"]][
                                        0],
                                'component_sizing':
                                    self.components[capacity["component_id"]][
                                        1],
                                'loading_value': loading['value'],
                                'capacity_value': capacity['capacity'],
                                'capacity_critical_level': capacity[
                                    'critical'],
                            }
                        )
            union_ingredients_data.append(
                {
                    'name': self.vending_machines[vending_machine_id][0],
                    'data': capacity_data
                }
            )
        return union_ingredients_data

    def how_ingredients_must_have(self):
        """ Отобразит данные о том, какие ингредиенты нужны в данный момент. """

        for item in self.union_of_capacity_and_loading:
            print('---> ', item['name'])
            for ingredient in item['data']:
                component_name = ingredient["component_name"]
                loading_value = ingredient["loading_value"]
                capacity_value = ingredient["capacity_value"]
                component_sizing = ingredient["component_sizing"]
                diff_component = (capacity_value - loading_value)
                how_many_need = 0

                if component_sizing == 'гр':
                    how_many_need = diff_component // 700
                    component_sizing = 'шт'
                if component_sizing == 'шт':
                    how_many_need = diff_component // 80
                if component_sizing == 'мл':
                    how_many_need = diff_component // 5000
                    component_sizing = 'шт'

                print(
                    f'\t{component_name}: {how_many_need} {component_sizing}'
                )

            print('-' * 70)

    def show_ingredients(self):
        """ Отобразит данные о загрузке ингредиентов. """
        for item in self.union_of_capacity_and_loading:
            print('---> ', item['name'])
            for ingredient in item['data']:
                print(
                    f'{ingredient["component_name"]}: {ingredient["loading_value"]}/{ingredient["capacity_value"]} {ingredient["component_sizing"]}'
                )
            print('-' * 70)


if __name__ == "__main__":
    telemetron = TelemetronRequests()
    # telemetron.show_ingredients()
    telemetron.how_ingredients_must_have()
