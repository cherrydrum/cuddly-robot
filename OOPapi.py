import requests as r
from bs4 import BeautifulSoup as bs
from pypac import PACSession, get_pac
import configparser
import pickle
import os


class Connection():
    def __init__(self, url):
        self.authorized = False
        self.tracker_url = url
        pac = get_pac(url='https://antizapret.prostovpn.org/proxy.pac')
        self.session = PACSession(pac)

    def obtaindata(self, file='config.ini'):
        data = configparser.ConfigParser()
        data.read(file)
        self.username = data['auth']['username']
        print(self.username)
        self.password = data['auth']['password']
        self.cookiefilename = data['meta']['cookie']

    def auth(self, force=False):
        if self.username and self.password:
            headers = {'User-Agent': 'Mozilla/5.0'}
            payload = {'login_username': self.username,
                       'redirect': 'index.php',
                       'login_password': self.password,
                       'sid': '', 'login': 'Вход'}  # Невнятно.
            if os

            self.session.post(f'{self.tracker_url}/login.php',
                              headers=headers, data=payload)
            self.authorized = True
            with open(self.cookiefilename, 'wb') as f:
                pickle.dump(self.session.cookies, f)
            return self.session.cookies.get_dict()
        else:
            raise AttributeError  # FIX ME
