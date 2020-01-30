from utilities import *
from credentials import *
from constants import *
import requests

application_name = "trello"


def get_boards_id_by_member_username(username):
    url = "https://api.trello.com/1/members/" + username + "/boards"
    querystring = {"filter": "all", "fields": "all", "lists": "none", "memberships": "none",
                   "organization": "false", "organization_fields": "name,displayName",
                   "key": TRELLO_API_KEY, "token": TRELLO_SERVER_TOKEN}
    response = requests.request("GET", url, params=querystring)
    datas = response.json()
    shortlinks_with_name_boards = []
    for board in datas:
        # we get shortlinks instead ids just because the API allows this + more simple
        shortlink_board = board['shortLink']
        shortlinks_with_name_boards.append(shortlink_board)
    return shortlinks_with_name_boards


def get_open_cards_by_board_id(id):
    url = "https://api.trello.com/1/boards/" + id + "/lists"
    querystring = {"cards": "open", "card_fields": "all", "filter": "open", "fields": "all",
                   "key": TRELLO_API_KEY, "token": TRELLO_SERVER_TOKEN}
    response = requests.request("GET", url, params=querystring)
    datas = response.json()
    return datas


def trello_script():
    # If the work directory "../trello" doesn't existe yet...
    # ... creation of this directory
    create_directory(PD_SCRIPT_TRELLO_DIRECTORY_PATH)

    boards = get_boards_id_by_member_username(PD_SCRIPT_TRELLO_MEMBER_USERNAME)

    file_name = create_timestamped_and_named_file(application_name)

    file = open(file_name, "w", encoding="utf-8")

    for board in boards:
        datas = get_open_cards_by_board_id(board)
        file.write(str(datas))
        file.write("\n\n################################################################################ \n\n")

