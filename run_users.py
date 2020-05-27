from users import *
from log import Log

PATH = ''
SEND_FLAG = True
SIGNATURE = "\n\n^(WCACompetitionsBot)"


def main():
    log = Log(PATH, 'users')
    try:
        new = read_messages(SEND_FLAG)
        if not new:
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
            u.send_welcome(SEND_FLAG, SIGNATURE)  # send the new users a welcome
            list_users.append(u)

        save_users(list_users, PATH)  # stores it again in the file.

        log.save('success')
    except Exception as e:
        print("Exception occurred: ", e)
        log.save('error')
        log.error(e)


main()
