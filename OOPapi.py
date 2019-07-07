import requests as r
from bs4 import BeautifulSoup as bs
import configparser
import pickle
import os


class Connection():
    def __init__(self, url):
        self.authorized = False
        self.tracker_url = url
        self.session = r.session()
        self.cookie = None

    def obtaindata(self, file='config.ini'):
        self.configfilename = file
        self.cparser = configparser.ConfigParser()
        self.cparser.read(file)
        self.username = self.cparser['auth']['username']
        self.password = self.cparser['auth']['password']
        self.proxies = {'http': self.cparser['meta']['proxy'],
                        'https': self.cparser['meta']['proxyssl']}
        # Если ранее были логины, берем печеньку из конфига.
        if 'cookie' in self.cparser['meta'] and self.cparser['meta']['cookie']:
            self.cookie = r.cookies.create_cookie(name='bb_session',
                                                  value=self.cparser['meta']['cookie'])
            self.session.cookies.set_cookie(self.cookie)

    def auth(self, force=False):
        # Для принудительной аутентификации нужно очистить старые куки
        if force:
            self.session.cookies.clear()
            self.cookie = None
        if self.username and self.password:
            if not self.cookie:
                payload = {'login_username': self.username,
                           'redirect': 'index.php',
                           'login_password': self.password,
                           'sid': '', 'login': 'Вход'}  # Иначе не логинит.

                self.session.post(f'{self.tracker_url}/login.php',
                                  data=payload, proxies=self.proxies)
                cookies = self.session.cookies.get_dict()
                if 'bb_session' in cookies.keys():
                    self.cparser['meta']['cookie'] = cookies['bb_session']
                    with open(self.configfilename, 'w') as f:
                      self.cparser.write(f)
                else:
                    raise Exception('Login error. Failed to retrive cookies.')
            else:
                raise Exception('Cookies were found but force mode was not declared.')
        else:
            raise Exception('Userdata was not specified.')

    def query(self, req, filter='seed' ,order='asc'):
        pass

