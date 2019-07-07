import requests
from bs4 import BeautifulSoup
from pypac import PACSession
from pypac.parser import PACFile
import pickle
import os

TRACKERURL = 'https://rutracker.org/forum/'


def init():
    with open('proxy.pac') as f:
        print('Reading PAC...')
        pac = PACFile(f.read())
        print('Initializing session...')
        session = PACSession(pac)


def auth(username, password):
    if os.path.isfile('cookies'):
        os.remove("cookies")
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'login_username': username, 'login_password': password,
               'redirect': 'index.php', 'sid': '', 'login': 'Вход'}
    r = session.post(TRACKERURL+'login.php',
                     headers=headers, data=payload)
    login_cookies = session.cookies.get_dict()
    with open('cookies', 'wb') as f:
        pickle.dump(session.cookies, f)

def parse(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    try:
        items_raw = soup.find(id='tor-tbl').tbody.find_all('tr')
    except AttributeError:
        return [{'title':'Ошибка парсинга. Вы точно вошли в систему?',
                'href':0, 'size':'TBODY'}]
    items = []
    for i in items_raw:
        item = {}
        try:
            item['seeders'] = i.find(class_='row4 nowrap').u.text
        except:
            continue
        approved = i.find(class_='tor-icon tor-approved')
        if approved and approved.text == '√' and int(item['seeders']) > 0:
            item['title'] = i.find(class_='med tLink hl-tags bold').text
            item['href'] = i.find(class_='small tr-dl dl-stub')['href'].split('?t=')[1]
            item['size'] = i.find(class_='small tr-dl dl-stub').text[:-2]
            items.append(item)
    return items

def seek(line, order=['desc', 'seed'], trusted_only=False):
    args = {}
    args['nm'] = str(line)
    if len(order) == 2:
        if order[0] == 'asc':
            args['s'] = 1
        elif order[0] == 'desc':
            args['s'] = 2
        if order[1] == 'size':
            args['o'] = 7
        elif order[1] == 'seed':
            args['o'] = 10
    r = session.get(TRACKERURL+'tracker.php', params=args)
    return parse(r.text)

def getmagnet(torid):
    r = session.get(TRACKERURL + 'viewtopic.php?t=' + torid)
    soup = BeautifulSoup(r.text, 'html.parser')
    magnet = soup.find("a", {"class": "med magnet-link magnet-link-16"})['href']
