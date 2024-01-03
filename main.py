from service.yandex_service import ConnToCloudService
import my_logger
from config.config import config
from get_info_in_cloud_disk import create_folder


def main():
    cloud_connector = ConnToCloudService(config.token.token_to_cloud)
    my_logger.logger.info(f'Запустился процесс.')
    """ Если нет OAuth токена, то запустив этот метод, получим его """
    # cloud_connector.get_oauth_token()
    """ Создаем директорию в облачном хранилище и
        с определенной периодичностью просматривает определенную директорию
     """
    create_folder(cloud_connector)


if __name__ == '__main__':
    main()
