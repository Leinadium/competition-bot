from competitions import *
from users import load_users, get_reddit_credentials
from log import Log
from os import path, sep


# This script is executed via crontab, so it needs the script's directory to find the modules and files
PATH = path.dirname(path.abspath(__file__)) + sep

# LINK_HTLM = "https://www.worldcubeassociation.org/competitions"
LINK_API = 'https://www.worldcubeassociation.org/api/v0/competitions'

SEND_FLAG = True  # False if testing
SIGNATURE = "\n\n^(WCACompetitionsBot - v2.4)"


def main():
    # Starting Log object. Saves a log after execution in logs/
    print("Starting competitions module.")
    log = Log(PATH, 'competition')
    try:

        # Getting new competitions from WCA's API
        print("Reading new competitions.")
        actual = get_new_competitions(LINK_API, PATH)
        log.actual = len(actual)
        print("Found %d competitions at WCA" % len(actual))

        # Getting competitions from files/competitions.json
        print("Reading old competitions.")
        old = load_competitions(PATH)
        log.old = len(old)
        print("Found %d competitions at json" % len(old))

        # Comparing to get which competition was just announced
        print("Comparing both...")
        new = compare_competitions(old, actual)
        log.new = len(new)
        print("Found %d new competitions" % len(new))

        if len(new) != 0:
            # Loading users and starting reddit, and then sending.
            print("Loading users.")
            users = load_users(PATH)
            print("Starting reddit.")
            reddit = get_reddit_credentials(PATH)
            print("Matching competitions...")
            match_competitions_users(new, users, SEND_FLAG, SIGNATURE, reddit)

        # updating competitions on files/competitions.json
        print("Saving competitions.json file.")
        save_competitions(actual, PATH)

        # saving log
        log.update_resume(new_competitions=len(new), total_competitions=len(actual))
        log.save('success')

    except Exception as e:
        print("Exception occurred: ", e)
        log.error(e)
        log.save('error')

    print("Done!")
    return


main()
