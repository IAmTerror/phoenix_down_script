# -*- coding: utf-8 -*-
# !/usr/bin/env python

from utilities import *
from credentials import *
from constants import *
import requests


class TrelloScript:

    def __init__(self):
        self.application_name = "trello"
        self.trello_api_key = TRELLO_API_KEY
        self.trello_server_token = TRELLO_SERVER_TOKEN
        self.trello_member_username = TRELLO_MEMBER_USERNAME

    def get_boards_shortlinks_as_keys_with_values(self, username):
        url = "https://api.trello.com/1/members/" + username + "/boards"
        querystring = {"filter": "all", "fields": "all", "lists": "none", "memberships": "none",
                       "organization": "false", "organization_fields": "name,displayName",
                       "key": self.trello_api_key, "token": self.trello_server_token}
        response = requests.request("GET", url, params=querystring)
        try:
            response.raise_for_status()
            datas = response.json()
            shortlinks_as_keys_with_values = {}
            for board in datas:
                # we get shortlinks instead ids just because the API allows this + more simple
                shortlink_board = board['shortLink']
                name_board = board['name']
                shortlinks_as_keys_with_values[shortlink_board] = [name_board]
        except requests.exceptions.HTTPError as e:
            logging.warning("Error: " + str(e))
            shortlinks_as_keys_with_values = ""
        return shortlinks_as_keys_with_values

    def get_open_cards_by_board_id(self, id):
        url = "https://api.trello.com/1/boards/" + id + "/lists"
        querystring = {"cards": "open", "card_fields": "all", "filter": "open", "fields": "all",
                       "key": self.trello_api_key, "token": self.trello_server_token}
        response = requests.request("GET", url, params=querystring)
        try:
            response.raise_for_status()
            datas = response.json()
        except requests.exceptions.HTTPError as e:
            logging.warning("Error: " + str(e))
            datas = ""
        return datas

    def get_card_by_id(self, id):
        url = "https://api.trello.com/1/cards/" + id + ""
        querystring = {"attachments": "false", "attachment_fields": "all", "members": "false", "membersVoted": "false",
                       "checkItemStates": "false", "checklists": "none", "checklist_fields": "all", "board": "false",
                       "list": "false", "pluginData": "false", "stickers": "false", "sticker_fields": "all",
                       "customFieldItems": "false", "key": self.trello_api_key, "token": self.trello_server_token}
        response = requests.request("GET", url, params=querystring)
        try:
            response.raise_for_status()
            datas = response.json()
        except requests.exceptions.HTTPError as e:
            logging.warning("Error: " + str(e))
            datas = ""
        return datas

    def run_script(self):
        logging.info('trello script is running...')

        create_directory(PD_SCRIPT_ROOT_LOGS_PATH + "/" + self.application_name)

        shortlinks_as_keys_with_values = self.get_boards_shortlinks_as_keys_with_values(
            self.trello_member_username)

        logging.info('creating trello log file')
        file_name = create_timestamped_and_named_file_name(self.application_name)
        file = open(file_name, "w", encoding="utf-8")

        logging.info('writing in trello log file...')
        # processing of boards
        for shortlink in shortlinks_as_keys_with_values:
            name_board = shortlinks_as_keys_with_values[shortlink]
            file.write("##### JSON datas of " + str(name_board) + " board : \n\n")
            datas = self.get_open_cards_by_board_id(shortlink)
            file.write(str(datas))
            file.write("\n\n\n\n")
        # processing of particulary valuable cards
        for card in TRELLO_CARDS_IDS:
            datas = self.get_card_by_id(card)
            if 'name' in datas and len(datas['name']) > 0:
                name_card = datas['name']
                file.write("##### JSON datas of " + str(name_card) + " valuable card : \n\n")
                file.write(str(datas))
                file.write("\n\n\n\n")

        logging.info('writing in trello log file done')
        file.close()

        # opens the file for reading only in binary format in order to upload
        file = open(file_name, "rb")

        upload_file_to_server_ftp(file, file_name, self.application_name)

        file.close()

        logging.info('trello script is terminated')
