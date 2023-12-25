import configparser
from dataclasses import dataclass
from my_logger import my_logger


@dataclass
class DataAboutFiles:
    local_path: str
    dirname_in_cloud: str
    frequency_sync_period: str


@dataclass
class Token:
    token_to_cloud: str
    client_id: str
    client_secret: str


@dataclass
class LogData:
    path_to_file_log: str


@dataclass
class Config:
    token: Token
    log_data: LogData
    data_about_file: DataAboutFiles


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    data_about_files = config['file_data']
    token_api = config['token']
    log_data_info = config['log']

    try:
        data_with_path_to_sync = data_about_files['dirname_in_cloud']
        api_token = token_api['token_to_cloud']
        if not api_token:
            raise ValueError
        if not data_with_path_to_sync:
            raise FileNotFoundError
    except ValueError:
        my_logger.error(f'Отсутствует токен API!')
    except FileNotFoundError:
        my_logger.error(f'Отсутствует путь к синхронизируемой папке!')
    else:

        return Config(
            token=Token(
                token_to_cloud=api_token,
                client_id=token_api['client_id'],
                client_secret=token_api['client_secret'],
            ),
            log_data=LogData(
                path_to_file_log=log_data_info['path_to_file_log']
            ),
            data_about_file=DataAboutFiles(
                local_path=data_about_files['local_path'],
                dirname_in_cloud=data_about_files['dirname_in_cloud'],
                frequency_sync_period=data_about_files['frequency_sync_period'],
            )
        )


config = load_config('config.ini')
