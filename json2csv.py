import json

if __name__ == "__main__":
    with open('networks.json', 'r', encoding='utf-8') as fr:
        data = fr.read()
        json_data = json.loads(data)
        with open('networks.csv', 'w', encoding='utf-8') as fw:
            fw.write(
                '"city";' +
                '"city_api_description_name";' +
                '"city_api_description_timezone";' +
                '"city_api_description_lat";' +
                '"city_api_description_lon";' +
                '"city_api_network_start";' +
                '"city_api_network_end";' +
                '\n'
            )
            for cities_data in json_data:
                for city_data in cities_data:
                    for network_data in city_data.get('city_4itme_api_networks'):
                        s = '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (
                            city_data.get('city_name'),
                            city_data.get('city_4itme_api_description').get('name_ru'),
                            city_data.get('city_4itme_api_description').get('timezone'),
                            city_data.get('city_4itme_api_description').get('lat'),
                            city_data.get('city_4itme_api_description').get('lon'),
                            network_data.get('begin'),
                            network_data.get('end'),
                        )
                        fw.write(s)
