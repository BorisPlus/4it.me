import json
import requests
import ipaddress

cities = [
    "Сыктывкар",
    "Норильск",
    "Кохма",
    "Мухосранск",
]

best_service = 'https://4it.me/api'


def get_city_identity(city_name, session=None):
    if session is None:
        session = requests.session()
    response = session.get(f'{best_service}/getcitylist?city={city_name}')
    return response.json()


def get_city_networks(city_id, city_name, session=None):
    if session is None:
        session = requests.session()
    response = session.get(f'{best_service}/getlistip?cityid={city_id}&base=net&city={city_name}')
    return response.json()


def get_data(city_name, session=None):
    if session is None:
        session = requests.session()
    cities_descriptions = get_city_identity(city_name, session=session)
    if not cities_descriptions:
        return [dict(
            city_name=city_name,
            city_4itme_api_description={},
            city_4itme_api_networks=[]
        )]

    result_cities_descriptions = []
    for city_description in cities_descriptions:
        city_networks = get_city_networks(city_id=city_description.get('id_net'),
                                          city_name=city_description.get('name_ru'),
                                          session=session)
        for city_network in city_networks:
            city_network['begin'] = str(ipaddress.ip_address(city_network['b']))
            city_network['end'] = str(ipaddress.ip_address(city_network['e']))
        result_cities_descriptions.append(dict(
            city_name=city_name,
            city_4itme_api_description=city_description,
            city_4itme_api_networks=city_networks
        ))
    return result_cities_descriptions


if __name__ == "__main__":
    data = []
    _session = requests.session()
    for _city in cities:
        print(_city)
        city_data = get_data(_city, session=_session)
        if city_data:
            data.append(city_data)

    with open('networks.json', 'w', encoding='utf-8') as f_out:
        json.dump(data, f_out, ensure_ascii=False, indent=3)
