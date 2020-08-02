# -*- coding: utf-8 -*-
# !/usr/bin/env python

from utilities import *
from credentials import *
from constants import *
import requests


class SteamScript:
    def __init__(self):
        self.application_name = "steam"

    def get_user_name(self, id):
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + STEAM_API_KEY + \
              "&steamids=" + id
        response = requests.request("GET", url)
        datas = response.json()
        users = datas['response']
        user = users['players']
        # Steam API returns a list of ONE user when we call GetPlayerSummaries API method, so...
        user_name = user[0]['personaname']
        return user_name

    def get_friend_list(self):
        url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + STEAM_API_KEY + \
              "&steamid=" + STEAM_USER_ID + "&relationship=friend"
        friends_dictionnary = {}
        response = requests.request("GET", url)
        friends = response.json()
        for friend in friends['friendslist']['friends']:
            friend_id = friend['steamid']
            friend_user_name = self.get_user_name(friend_id)
            friends_dictionnary[friend_id] = friend_user_name
        return friends_dictionnary

    def get_owned_games_ids(self):
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + STEAM_API_KEY + \
              "&steamid=" + STEAM_USER_ID + "&format=json"
        my_games_ids = []
        response = requests.request("GET", url)
        datas = response.json()
        my_games = datas['response']['games']
        for game in my_games:
            game_id = game['appid']
            my_games_ids.append(game_id)
        return my_games_ids

    def run_script(self):

        logging.info('steam script is running...')

        create_directory(PD_SCRIPT_ROOT_PATH + "/" + self.application_name)

        user = self.get_user_name(STEAM_USER_ID)

        friends = self.get_friend_list()

        my_games_ids = self.get_owned_games_ids()

        logging.info('creating steam log file')
        file_name = create_timestamped_and_named_file_name(self.application_name)
        file = open(file_name, "w", encoding="utf-8")

        logging.info('writing in steam log file...')
        # processing of friends
        file.write("##### Friends list of " + user + " steam user :")
        file.write("\n\n")
        file.write(str(friends))
        file.write("\n\n")
        for key, value in friends.items():
            file.write(key + " --- " + value)
            file.write("\n")
        file.write("\n\n")
        file.write(user + " steam user have " + str(len(friends)) + " friends on steam")
        file.write("\n\n\n\n")
        # processing of owned games
        file.write("##### " + user + " owned games ids :")
        file.write("\n\n")
        file.write(str(my_games_ids))
        file.write("\n\n")
        for game_id in my_games_ids:
            file.write(str(game_id))
            file.write("\n")
        file.write("\n\n")
        file.write(user + " steam user have " + str(len(my_games_ids)) + " games on steam")

