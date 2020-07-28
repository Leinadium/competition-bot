from users import *
from log import Log
from os import path, sep

# This script is executed via crontab, so it needs the script's directory to find the modules and files
PATH = path.dirname(path.abspath(__file__)) + sep

SEND_FLAG = True  # False if testing
SIGNATURE = "\n\n^(WCACompetitionsBot - v2.4)"


def main():
    # Starting Log object to save at files/ later
    log = Log(PATH, 'users')
    try:
        # Starting reddit
        reddit = get_reddit_credentials(PATH)

        # Reading new messages.
        new = read_messages(SEND_FLAG, reddit)
        if not new:
            print("no new users")
            log.save("no-users")
            exit(0)

        list_users = load_users(PATH)  # get the stored users
        log.old = len(list_users)
        # if not list_users:
        #     raise Exception('LoadingUserError')

        sub, unsub = new  # new is a list with new users, and user unsubscribing
        log.actual = len(sub)
        log.new = len(unsub)
        list_users = remove_users(list_users, unsub)  # updates the list, removing
        for u in sub:
            u.send_welcome(SEND_FLAG, SIGNATURE, reddit)  # send the new users a welcome
            list_users.append(u)

        save_users(list_users, PATH)  # stores it again in the file.

        log.update_resume(new_users=len(sub), total_users=len(list_users))
        log.save('success')
        
    except Exception as e:
        print("Exception occurred: ", e)
        log.save('error')
        log.error(e)


main()
