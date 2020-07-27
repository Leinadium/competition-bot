from competitions import *
from users import load_users, get_reddit_credentials
from log import Log
from os import path, sep

PATH = path.dirname(path.abspath(__file__)) + sep
LINK = "https://www.worldcubeassociation.org/competitions"
SEND_FLAG = True
SIGNATURE = "\n\n^(WCACompetitionsBot - v2.2)"


def main():
    log = Log(PATH, 'competition')
    try:
        actual = get_new_competitions(LINK)
        log.actual = len(actual)

        old = load_competitions(PATH)
        log.old = len(old)

        new = compare_competitions(old, actual)
        log.new = len(new)

        if len(new) != 0:
            users = load_users(PATH)
            reddit = get_reddit_credentials(PATH)
            match_competitions_users(new, users, SEND_FLAG, SIGNATURE, reddit)

        save_competitions(actual, PATH)

        log.update_resume(new_competitions=len(new), total_competitions=len(actual))
        log.save('success')

    except Exception as e:
        print("Exception occurred: ", e)
        log.error(e)
        log.save('error')

    print("Done!")
    return


main()
