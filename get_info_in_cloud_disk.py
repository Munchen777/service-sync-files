import requests, re, hashlib, datetime, time, pathlib
from service.yandex_service import ConnToCloudService
from my_logger import my_logger


def find_filename_in_structure(structure):
    if isinstance(structure, dict):
        for key, value in structure.items():
            yield key, value
            yield from find_filename_in_structure(value)
    elif isinstance(structure, list):
        for element in structure:
            yield from find_filename_in_structure(element)


def add_changed_files_in_cloud(file: pathlib.Path, connection: ConnToCloudService) -> None:
    """ Для измененного файла берем ссылку для загрузки и загружаем """
    link_to_add_file = requests.get(f'{connection.url}/upload?path={connection.my_dir_in_cloud}/{file.name}'
                                    f'&overwrite=True',
                                    headers=connection.headers)
    response = link_to_add_file.json()
    print(response)
    if 'href' not in link_to_add_file.json():
        error_409 = response['error']
        my_logger.error(f'Ошибка. Статус код: {link_to_add_file.status_code}\n'
                        f'Исключение: {error_409}')
        return  #
    else:
        url_to_upload_href = link_to_add_file.json()['href']
        files = {'file': open(str(file), 'rb')}
        upload_changed_file = requests.put(url_to_upload_href, files=files)
        print(upload_changed_file.status_code)



def change_file_in_cloud(file: pathlib.Path, connection: ConnToCloudService) -> None:
    """ В структуре ответа ищем название файла и последнюю дату изменения """
    try:
        get_info_for_changes = requests.get(f'{connection.url}/files?offset=4',
                                            headers=connection.headers)
    except requests.ConnectionError as conn_exc:
        my_logger.error(f'Произошла ошибка подключения при попытке загружить измененный файл: {conn_exc}')
    response = get_info_for_changes.json()
    # print(response)
    # data = ['name', 'modified']
    data = ['name', 'modified']
    data_with_values_from_cloud = {}
    for value in find_filename_in_structure(response):
        for element in data:
            if len(data_with_values_from_cloud) >= 1 and element == value[0] and not data_with_values_from_cloud.get('modified'):
                data_with_values_from_cloud[element] = value[1]
                break
            if element == value[0] and file.name == value[1] and not data_with_values_from_cloud.get(element):
                data_with_values_from_cloud[element] = value[1]

    # print(data_with_values_from_cloud)
    for element in data_with_values_from_cloud:
        my_logger.info('За последнее время изменен файл с названием {}'.format(
            data_with_values_from_cloud[element]
        ))
        print(file.absolute())
    add_changed_files_in_cloud(file, connection)
    # if not file.exists(follow_symlinks=False): ...

class DiskResourceAlreadyExistsError(Exception):
    def __str__(self):
        return f'Файл уже существует в облаке.'


def add_existing_file_in_cloud(file: pathlib.Path, connection: ConnToCloudService) -> None:
    """ Для нового файла берем ссылку для загрузки и загружаем """
    # try:
    link_to_add_file = requests.get(f'{connection.url}/upload?path={connection.my_dir_in_cloud}/{file.name}'
                                    f'&overwrite=False',
                                    headers=connection.headers)

    response = link_to_add_file.json()
    if 'href' not in link_to_add_file.json():
        error_409 = response['error']
        my_logger.error(f'Ошибка. Статус код: {link_to_add_file.status_code}\n'
                        f'Исключение: {error_409}')
        return
    else:
        url_to_upload_href = link_to_add_file.json()['href']
        files = {'file': open(str(file), 'rb')}
        upload_new_file = requests.put(url_to_upload_href, files=files)
        print(upload_new_file.status_code)


def delete_file_from_cloud(file: pathlib.Path, connection: ConnToCloudService) -> None:
    try:
        query_to_delete_from_cloud = requests.delete(f'{connection.url}?path={connection.my_dir_in_cloud}/{file}&permanently=False',
                                                     headers=connection.headers)
    except requests.ConnectionError as conn_exc:
        my_logger.error(f'Произошла ошибка подключения при попытке удалить файл из облака: {conn_exc}')
    except requests.Timeout as timeout_exc:
        my_logger.error(f'Исключение timeout: {timeout_exc}')

    my_logger.info(f'Удален файл из облака - {file.name}')


def checking_new_file_with_no_changes(file: pathlib.Path, connection: ConnToCloudService) -> None:
    """ Загружаем новый, неизменный файл в облако. """
    try:
        add_nochanged_file = requests.get(f'{connection.url}/files?fields=items.name',
                                          headers=connection.headers)
        response = add_nochanged_file.json()
    except requests.ConnectionError as conn_exc:
        my_logger.error(f'Произошла ошибка подключения при попытке загрузить новый, неизменный файл: {conn_exc}')
    except requests.Timeout as timeout_exc:
        my_logger.error(f'Исключение timeout: {timeout_exc}')
    else:

        values_with_filenames_dct = response['items']
        if values_with_filenames_dct: # если какие-то названия вернул сервер
            print(values_with_filenames_dct)
            for filename in values_with_filenames_dct:
                filename_in_cloud = filename['name']
                guess_path = file.absolute().parents[0] / filename_in_cloud # есть ли у нас такой путь
                print(guess_path.name)
                print(file.name)
                if file.name != guess_path.name and file.exists():
                    my_logger.info(f'Такого файла {file.name} в облаке нет. Загружаю ...')
                    add_existing_file_in_cloud(file, connection)

                elif file.name == guess_path.name and not guess_path.exists():
                    my_logger.info(f'Из облака убираю удаленный файл {file.name}')
                    delete_file_from_cloud(filename_in_cloud, connection)

        else:
            if file.exists():
                my_logger.info(f'В облаке никаких файлов нет.')
                add_existing_file_in_cloud(file, connection)

                    # удаляю из облака
        # else:
        #     my_logger.info(f'Такого файла {file.name} в облаке нет. Загружаю ...')
        #     if file.exists():
        #         add_existing_file_in_cloud(file, connection)
            # загружаю на облако




    return  # ?


def checking_for_deleting(connection: ConnToCloudService):
    try:
        add_nochanged_file = requests.get(f'{connection.url}/files?fields=items.name',
                                          headers=connection.headers)
        response = add_nochanged_file.json()
    except requests.ConnectionError as conn_exc:
        my_logger.error(f'Произошла ошибка подключения при попытке загрузить новый, неизменный файл: {conn_exc}')
    except requests.Timeout as timeout_exc:
        my_logger.error(f'Исключение timeout: {timeout_exc}')
    else:

        values_with_filenames_dct = response['items']
        if values_with_filenames_dct:  # если какие-то названия вернул сервер
            print(values_with_filenames_dct)
            for filename in values_with_filenames_dct:
                filename_in_cloud = filename['name']
                query_for_deleting = requests.delete(f'{connection.url}?path={filename_in_cloud}?permanently=False',
                                                     headers=connection.headers)



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
                # file = file.with_suffix('.docx')

                delta_time = (date_time_utc - modified_local_file).seconds
                # Период синхронизации - 25 мин.

                if int(connection.frequency_sync_period) > delta_time / 60:
                    print(file.name)
                    print('Файл изменен')
                    change_file_in_cloud(file, connection)
                else:
                    print(file.name)
                    print('Файл не изменен')
                    checking_new_file_with_no_changes(file, connection)

        # if len(list(path.iterdir())) <= 1:
        #     my_logger.info(f'Локальная папка полностью пустая. Проверю облако.')
        #     checking_for_deleting(connection)

        print(time.sleep(60*int(connection.frequency_sync_period)))
