import requests


from config.config import config
from requests_oauthlib import OAuth2Session


class ConnToCloudService:
    def __init__(self, token_to_cloud):
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.token_cloud = token_to_cloud
        self.my_dir_in_cloud = config.data_about_file.dirname_in_cloud
        # self.client_id = config.token.client_id
        # self.client_secret = config.token.client_secret
        # self.cloud_path = config.data_about_file.dirname_in_cloud
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token_cloud),
            # 'path': self.my_dir_in_cloud
        }

    # def get_info_about_disk(self):
    #     """ Получаем Oauth токен """
    #     client_id = config.token.client_id
    #     client_secret = config.token.client_secret
    #     auth_url = "https://oauth.yandex.ru/authorize"
    #     token_url = "https://oauth.yandex.ru/token"
    #     oauth = OAuth2Session(client_id=client_id)
    #     authorization_url, state = oauth.authorization_url(auth_url, force_confirm="true")
    #     print("Перейдите по ссылке, авторизуйтесь и скопируйте код:", authorization_url)
    #     code = input("Вставьте одноразовый код: ")
    #     token = oauth.fetch_token(token_url=token_url,
    #                               code=code,
    #                               client_secret=client_secret)
    #     access_token = token["access_token"]
    #     self.token = access_token
    #     print(access_token)

