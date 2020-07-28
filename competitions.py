import json
import requests
import io
import datetime

from measurement import get_coords
from users import User

MONTHS = ['JAN', 'FEV', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DEC']


class Comp:
    def __init__(self, name, city, country, date, link, coords=None):
        self.name = name
        self.city = city
        self.country = country
        self.date = date
        self.link = link
        self.coords = coords

    # def create_coords(self):
    #     """Not used anymore because WCA's API already provides coordinates."""
    #     if not self.coords:
    #         self.coords = get_coords(', '.join([self.city, self.country]))

    def create_message(self):
        # s = '\n\n[' + self.name + '](https://www.worldcubeassociation.org' + self.link + ')'
        s = '\n\n[%s][%s]' % (self.name, self.link)
        s += ', at ' + self.city + ' - ' + self.country
        s += ', on ' + self.date
        return s

    def __str__(self):
        return "%s at %s" % (self.name, self.date)


def get_new_competitions(link, path):
    """Uses WCA API to get new competitions."""
    # Thanks to Alexandre Afonso at WCA for the example provided here:
    # https://github.com/campos20/wca-statistics/blob/master/src/api/wca_api.py

    competitions = []
    page = 1  # because a page only has 25 competitions
    today_string = datetime.date.today().isoformat()
    countries = get_countries_dict(path)

    while True:
        url = link + '?sort=start_date&start=' + today_string + '&page=' + str(page)
        r = requests.get(url)
        if r.status_code >= 400:
            raise Exception("BadHTMLCode")

        data = r.json()
        if len(data) == 0:  # no more pages to read
            break

        for d in data:  # reading competitions and creating objects
            if d['cancelled_at'] is not None:  # skip cancelled competitions
                continue

            link_c = d['url']
            name = d['name']
            city = d['city'].split(',')[0].upper()  # if state, gets only the city
            # country = coco.convert(d['country_iso2'], to='name_short').upper()  # converts iso2 to short_name
            country = countries[d['country_iso2']].upper()

            date = d['start_date'].split('-')
            date = "%s %s, %s" % (MONTHS[int(date[1]) - 1], date[2], date[0])

            coords = (d['latitude_degrees'], d['longitude_degrees'])
            competitions.append(Comp(name, city, country, date, link_c, coords))

        page += 1

    if not competitions:
        raise Exception("NoCompetitions")

    return competitions


def get_countries_dict(path):
    """Gets a dict that given a iso2, returns the short name of that country. 'BR' -> 'Brazil'."""
    with open(path + 'files/countries.json', 'r', encoding='utf8') as f:
        j = json.load(f)
    return j


def match_competitions_users(competitions, users, send_flag, signature, reddit):
    for u in users:
        competitions_to_send = []
        for c in competitions:
            if u.check_competition(c):
                if send_flag:
                    competitions_to_send.append(c)
                print("    Send %s to %s" % (c.name, u.name))
        u.send_competitions(competitions_to_send, signature, reddit)

    return


def compare_competitions(old, new):
    res = []

    if old != new:
        res = []
        for c in new:
            if c.name not in [a.name for a in old]:
                # c.create_coords()
                res.append(c)

    return res


def save_competitions(list_competitions, path):
    list_dict = [a.__dict__ for a in list_competitions]
    with io.open(path + 'files/competitions.json', 'w+', encoding='utf8') as f:
        json.dump(list_dict, f, indent=2, ensure_ascii=False)

    return


def load_competitions(path):
    with io.open(path + 'files/competitions.json', 'r', encoding='utf8') as f:
        list_dict = json.load(f)

    # ret = []
    # for a in list_dict:
    #     ret.append(Comp(a['name'], a['city'], a['country'], a['date'], a['link'], coords=a['coords']))
    # return ret
    return [Comp(a['name'], a['city'], a['country'], a['date'], a['link'], coords=a['coords']) for a in list_dict]


# OLD FUNCTIONS:

def get_html(link):
    """Get the html page, and check for error code."""
    url = requests.get(link)
    code = url.status_code
    if code >= 400:
        raise Exception('BadReturnHtml')
    return url


def get_new_competitions_html(link):
    """Uses beautiful to scrap wca website. DEPRECIATED"""
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
        except Exception as e:
            print("Couldn't read competition: ", e)

    if not list_competitions:
        raise Exception("NoCompetitions")

    return list_competitions
