import requests, re, hashlib, datetime
from service.yandex_service import ConnToCloudService
from my_logger import my_logger
import pathlib


def find_filename_in_structure(structure):
    if isinstance(structure, dict):
        for key, value in structure.items():
            yield key, value
            yield from find_filename_in_structure(value)
    elif isinstance(structure, list):
        for element in structure:
            yield from find_filename_in_structure(element)


def add_changed_files_in_cloud(file: pathlib.Path, connection: ConnToCloudService) -> None:
    link_to_add_file = requests.get(f'{connection.url}/upload?path={file.absolute()}&overwrite=True',
                                    headers=connection.headers)


def change_file_in_cloud(file: pathlib.Path, connection: ConnToCloudService) -> None:
    """ В структуре ответа ищем название файла и последнюю дату изменения """
    get_info_for_changes = requests.get(f'{connection.url}/files?offset=4',
                                        headers=connection.headers)
    response = get_info_for_changes.json()
    # print(response)
    # data = ['name', 'modified']
    data = ['name']
    data_with_values_from_cloud = {}
    for value in find_filename_in_structure(response):
        for element in data:
            if element == value[0] and file.name == value[1] and not data_with_values_from_cloud.get(element):
                data_with_values_from_cloud[element] = value[1]
            # elif len(data_with_values_from_cloud) == 1 and data_with_values_from_cloud.get('name'):
            #     data_with_values_from_cloud[element] = value[1]
            #     break
    for element in data_with_values_from_cloud:
        my_logger.info('За последнее время изменен файл с названием {}'.format(
            data_with_values_from_cloud[element]
        ))
        print(file.absolute())
    # add_changed_files_in_cloud(file, connection)
    # if not file.exists(follow_symlinks=False): ...


def create_folder(connection: ConnToCloudService):

    """ Создаем облачную директорию. Если она существует, то логгер уведомит. """

    info_disk_query = requests.put(f'{connection.url}?path={connection.my_dir_in_cloud}',
                                   headers=connection.headers)

    response = info_disk_query.json()
    if re.match(r'DiskPathPointsToExistent', response['error']):
        my_logger.info(f'Директория с {connection.my_dir_in_cloud} именем уже существует.')
    # print(response)
    path = pathlib.Path('/Users/georgiy/Documents/docs')
    while True:
        """ Получаем информацию о файлах на облаке. """

        get_info_about_cloud_dir = requests.get(f'{connection.url}?path={connection.my_dir_in_cloud}',
                                                headers=connection.headers)
        response = get_info_about_cloud_dir.json()
        # print(response)
        last_modified_time_in_cloud = response['modified']
        # print(last_modified_time_in_cloud)
        date_time_utc = datetime.datetime.now()
        for file in path.iterdir():
            if file.is_file() and not file.match(r'.DS_Store'):
                modified_local_file = datetime.datetime.fromtimestamp(file.stat().st_mtime)

                # print(file.name)
                #
                # print(date_time_utc)
                #
                # print('*****'*70)
                #
                # print(modified_local_file)
                delta_time = (date_time_utc - modified_local_file).seconds
                # Период синхронизации - 25 мин.
                # print(int(connection.frequency_sync_period))
                # print(delta_time)
                if int(connection.frequency_sync_period) > delta_time / 60:
                    print(file.name)
                    print('Файл изменен')
                    change_file_in_cloud(file, connection)
                    pass
                else:
                    print(file.name)
                    print('Файл не изменен')




        # time.sleep(60*10) в самом конце ставим паузу на 10 мин