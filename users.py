from measurement import *
import praw
import io
import json
import re


class User:
    def __init__(self, name, city, country, radius, coords=None):
        """Class to store all the info for a user"""
        self.name = name
        self.radius = radius
        self.city = city
        self.country = country
        self.coords = coords if coords else get_coords(', '.join([city, country])) if radius > 0 else None
        # sets the coords if radius is specified

    def send_competitions(self, list_c, signature, reddit):
        """Receives a list of competitions, and the final signature. Sends the messages for each comp."""
        if len(list_c) == 0:
            return
        m = "New competition(s): "
        for c in list_c:
            m += c.create_message()
        m += signature
        reddit.redditor(self.name).message("New competition(s)!", m)

    def send_welcome(self, send_flag, signature, reddit):
        """Creates the welcome message and send."""
        if not send_flag:  # send_flag == True when testing
            print("Welcome %s, at %s in %s, with a %0.2f radius" % (self.name, self.city, self.country, self.radius))
            return
        m = "Thanks for subscribing to WCACompetitionsBot: "
        if not self.city:
            m += "\n\n%s" % self.country
        else:
            m += "\n\n%s, at %s" % (self.city, self.country)
        
        if self.radius >= 0:
            m += ", radius = %0.2f." % self.radius
        m += signature
        reddit.redditor(self.name).message("Thank you for subscribing.", m)

    def check_competition(self, c):
        """Checks if the competitions is worth sending to the user."""
        if self.country == c.country:  # if the country is the same, maybe the city too
            if not self.city or (self.city == c.city):
                return True
        if self.coords:  # else, maybe the coordinates between the two is smaller then the radius...
            # print("Radius: %0.2f, Distance: %0.2f" % (self.radius, find_distance(self.coords, c.coords)))
            if find_distance(self.coords, c.coords) <= self.radius:
                return True

        return False


def send_invalid(message, reddit):
    """Sends a invalid message to the user."""
    m = "Sorry, I couldn't understand the location, of you gave a invalid radius. Please try again with a new message."
    reddit.redditor(message.author.name).message("Invalid subscription!", m)
    return


def read_messages(send_flag, reddit):
    """Reads new messages. Returns two list of User objects, to add and remove."""
    unsubscribe = list()
    subscribe = list()
    unread = list()

    for m in reddit.inbox.unread(limit=None):
        if isinstance(m, praw.models.Message):
            if m.subject.lower().strip() == 'subscribe':  # message to be treated
                text = m.body
                # country, city (radius)
                '''
                if "(" in text and ")" in text:
                    radius = (text[text.find('(') + 1:text.find(")")])  # gets the radius
                    try:
                        radius = float(radius)  # checks if the radius is a float.
                        text = text[:text.find('(')]
                    except ValueError:  # checks if error
                        send_invalid(m, reddit)  # tell user he is wrong
                        unread.append(m)  # reads the message
                        continue
                    print(radius)
                elif "(" in text or ")" in text:
                    send_invalid(m, reddit)  # if it passes here, the radius is wrong
                    unread.append(m)
                    continue
                else:
                    radius = -1

                if "," in text:  # city!
                    [country, city] = text.split(",")
                    city = city.strip().upper()
                else:
                    [country, city] = [text, None]
                '''
                if ')' in text and '(' in text:  # radius is defined
                    r = re.match('([a-zA-Z ]+),([a-zA-Z ]+)(\\([0-9]+\\))', text)
                    if r is None:   # invalid radius
                        if not send_flag:
                            print("invalid:", text)
                        else:
                            send_invalid(m, reddit)
                            unread.append(m)
                        continue
                    country, city = text.split(',')
                    radius = int(re.search('([0-9]+)', city).group(0))  # get the radius
                    city = city.split('(')[0]

                else:  # no radius, only city or country
                    if re.match('([a-zA-Z ]+),([a-zA-Z ]+)', text) is not None:  # COUNTRY, CITY
                        country, city = text.split(',')
                    elif re.match('([a-zA-Z ]+)', text) is not None:
                        country, city = text, None
                    else:
                        if not send_flag:
                            print("invalid:", text)
                        else:
                            send_invalid(m, reddit)
                            unread.append(m)
                        continue
                    radius = -1

                country = country.strip().upper()
                city = city.strip().upper() if city is not None else city

                u = User(m.author.name, city, country, radius)
                subscribe.append(u)
                if send_flag:
                    unread.append(m)

            elif m.subject.lower().strip() == 'unsubscribe':
                unsubscribe.append(m.author.name)

                if send_flag:  # only reads the message it not testing.
                    unread.append(m)
                else:
                    print("cleaned messages from ", m.author.name)

    reddit.inbox.mark_read(unread)

    if len(subscribe) + len(unsubscribe) > 0:
        return [subscribe, unsubscribe]
    return None


def remove_users(list_users, list_remove):
    """Removes users by the name"""
    for u in list_users:
        if u.name in list_remove:
            list_users.remove(u)

    return list_users


def save_users(list_users, path):
    """Saves the users into the file as json"""
    list_dict = [a.__dict__ for a in list_users]
    with io.open(path + 'files/users.json', 'w+', encoding='utf8') as f:
        json.dump(list_dict, f, indent=2)
    return


def load_users(path):
    """Load the users from file as json"""
    with io.open(path + 'files/users.json', 'r', encoding='utf8') as f:
        list_dict = json.load(f)

    return [User(a['name'], a['city'], a['country'], a['radius'], coords=a['coords']) for a in list_dict]


def get_reddit_credentials(path):
    with open(path + 'files/credentials.json') as f:
        credentials = json.load(f)

    r = praw.Reddit(user_agent=credentials['user_agent'],
                    client_id=credentials['client_id'],
                    client_secret=credentials['client_secret'],
                    username=credentials['username'],
                    password=credentials['password'])

    return r
