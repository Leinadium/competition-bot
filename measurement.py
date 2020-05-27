import geopy
from geopy import distance


def get_coords(location):  # TODO
    """Get coordinates from location using geopy. Return list or None if error."""
    g = geopy.geocoders.Nominatim(user_agent="WCACompetitionsBot")
    try:
        loc = g.geocode(location)
        lat = loc.latitude
        lon = loc.longitude
        r = [lat, lon]

    except Exception as e:
        print("Error getting coords: ", e)
        return None

    return r


def find_distance(l1, l2):
    """Get distance between two distances using geopy. Return int or -1 if error."""
    try:
        return distance.distance(l1, l2).km

    except Exception as e:
        print("Error getting distance between 2 points", e)
        return -1
