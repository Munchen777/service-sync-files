import requests, re, hashlib
from service.yandex_service import ConnToCloudService
from my_logger import my_logger
import pathlib, time


def calculate_hash(file_path):
    hasher = ...


def create_folder(connection: ConnToCloudService):

    info_disk_query = requests.put(f'{connection.url}?path={connection.my_dir_in_cloud}',
                                   headers=connection.headers)

    response = info_disk_query.json()
    if re.match(r'DiskPathPointsToExistent', response['error']):
        my_logger.info(f'Директория с {connection.my_dir_in_cloud} именем уже существует.')
    print(response)
    path = pathlib.Path('/Users/georgiy/Documents/docs')
    while True:
        # time.sleep(60*10) в самом конце ставим паузу на 10 мин
        for child in path.iterdir():
            if child.is_file():
                current_hash = calculate_hash(child)


