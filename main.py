from service.yandex_service import ConnToCloudService
import my_logger
from config.config import config
from get_info_in_cloud_disk import create_folder


def main():
    cloud_connector = ConnToCloudService(config.token.token_to_cloud)
    my_logger.logger.info(f'Запустился процесс.')
    """ Токен получил """
    # my_service.get_info_about_disk()
    """ Создаем директорию в облачном хранилище """
    create_folder(cloud_connector)


if __name__ == '__main__':
    main()
