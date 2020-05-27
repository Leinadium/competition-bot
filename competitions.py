import json
import requests
import io
from bs4 import BeautifulSoup

from measurement import get_coords
from users import User


class Comp:
    def __init__(self, name, city, country, date, link, coords=None):
        self.name = name
        self.city = city
        self.country = country
        self.date = date
        self.link = link
        self.coords = coords

    def create_coords(self):
        if not self.coords:
            self.coords = get_coords(', '.join([self.city, self.country]))

    def create_message(self):
        s = '\n\n[' + self.name + '](https://www.worldcubeassociation.org' + self.link + ')'
        s += ', at ' + self.city + ' - ' + self.country
        s += ', on ' + self.date
        return s


def get_html(link):
    """Get the html page, and check for error code"""
    url = requests.get(link)
    code = url.status_code
    if code != 200:
        raise Exception('BadReturnHtml')
    return url


def get_new_competitions(link):
    # print("loading html")
    html = get_html(link)

    # print('loading competitions list')
    soup = BeautifulSoup(html.content, 'html.parser')
    competition_html = soup.find_all('li', class_="list-group-item not-past")

    list_competitions = list()
    # print("creating competitions")
    for c in competition_html:
        try:
            date = list(c.find(class_='date').stripped_strings)[0]
            link = c.find(class_='competition-info').a['href']
            name = c.find(class_='competition-info').a.string
            location = list(c.find(class_='location').stripped_strings)
            country = location[0]
            city = location[1][1:].strip()
            if "," in city:
                city = city[:city.find(',')]  # if state

            list_competitions.append(Comp(name, city.upper(), country.upper(), date, link))
            # print('.', end='')
        except Exception as e:
            print("Couldn't read competition: ", e)

    # print('.')

    if not list_competitions:
        raise Exception("NoCompetitions")

    return list_competitions


def match_competitions_users(competitions, users, send_flag, signature):
    for u in users:
        competitions_to_send = []
        for c in competitions:
            if u.check_competition(c):
                if send_flag:
                    competitions_to_send.append(c)
                print("    Send %s to %s" % (c.name, u.name))
        u.send_competitions(competitions_to_send, signature)

    return


def compare_competitions(old, new):
    res = []

    if old != new:
        res = []
        for c in new:
            if c.name not in [a.name for a in old]:
                c.create_coords()
                res.append(c)

    return res


def save_competitions(list_competitions, path):
    list_dict = [a.__dict__ for a in list_competitions]
    with io.open(path + 'files/competitions.json', 'w+', encoding='utf8') as f:
        json.dump(list_dict, f)

    return


def load_competitions(path):
    with io.open(path + 'files/competitions.json', 'r', encoding='utf8') as f:
        list_dict = json.load(f)

    return [Comp(a['name'], a['city'], a['country'], a['date'], a['link'], coords=a['coords']) for a in list_dict]
