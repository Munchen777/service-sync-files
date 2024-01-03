from service.yandex_service import ConnToCloudService
import my_logger
from config.config import config
from get_info_in_cloud_disk import create_folder


def main():
    cloud_connector = ConnToCloudService(config.token.token_to_cloud)
    my_logger.logger.info(f'Запустился процесс.')
    """ Если нет OAuth токена, то может его получить, 
    используя Client secret и ClientID """
    # cloud_connector.get_token()
    """ Создаем директорию в облачном хранилище, если она не существует и
     в бесконечном цикле просматриваем файлы в локальной директории с
     периодичностью """
    create_folder(cloud_connector)


if __name__ == '__main__':
    main()
