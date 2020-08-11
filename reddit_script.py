# -*- coding: utf-8 -*-
# !/usr/bin/env python

from utilities import *
from credentials import *
from constants import *
import requests
import requests.auth

# Oath2 Reddit quick start : https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
# Oath2 Reddit documentation : https://github.com/reddit-archive/reddit/wiki/OAuth2


class RedditScript:
    def __init__(self):
        self.application_name = "reddit"

    def reddit_request_token(self):
        client_auth = requests.auth.HTTPBasicAuth(REDDIT_APP_CLIENT_KEY, REDDIT_API_SECRET_KEY)
        post_data = {"grant_type": "password", "username": REDDIT_USERNAME, "password": REDDIT_PASSWORD}
        headers = {"User-Agent": "phoenix-down/0.1 by IAmTerror"}
        response = requests.post("https://www.reddit.com/api/v1/access_token",
                             auth=client_auth, data=post_data, headers=headers)
        datas = response.json()
        token = datas['access_token']
        return token

    def get_username(self):
        my_token = self.reddit_request_token()
        url = "https://oauth.reddit.com/api/v1/me"
        headers = {"Authorization": "bearer " + my_token, "User-Agent": "phoenix-down/0.1 by IAmTerror"}
        response = requests.get(url, headers=headers)
        datas = response.json()
        username = datas['name']
        return username

    def get_saved_posts(self, after_pagination=None, saved_posts_count=0,  all_datas=None):
        if all_datas is None:
            all_datas = []
        my_token = self.reddit_request_token()
        if after_pagination is None:
            url = "https://oauth.reddit.com/user/" + REDDIT_USERNAME.lower() + "/saved?limit=100"
        else:
            url = "https://oauth.reddit.com/user/" + REDDIT_USERNAME.lower() \
                  + "/saved?limit=100&after=" + after_pagination
        headers = {"Authorization": "bearer " + my_token, "User-Agent": "phoenix-down/0.1 by IAmTerror"}
        response = requests.get(url, headers=headers)
        current_datas = response.json()
        all_datas.append(current_datas)
        after_pagination = current_datas['data']['after']
        saved_posts_current_dist = current_datas['data']['dist']
        saved_posts_count += saved_posts_current_dist
        if after_pagination is not None:
            return self.get_saved_posts(after_pagination, saved_posts_count, all_datas)
        else:
            return all_datas, saved_posts_count

    def get_subscribed_subreddits(self, after_pagination=None, subreddits_count=0, all_datas=None):
        if all_datas is None:
            all_datas = []
        my_token = self.reddit_request_token()
        if after_pagination is None:
            url = "https://oauth.reddit.com/subreddits/mine/subscriber?limit=100"
        else:
            url = "https://oauth.reddit.com/subreddits/mine/subscriber?limit=100&after=" + after_pagination
        headers = {"Authorization": "bearer " + my_token, "User-Agent": "phoenix-down/0.1 by IAmTerror"}
        response = requests.get(url, headers=headers)
        current_datas = response.json()
        all_datas.append(current_datas)
        after_pagination = current_datas['data']['after']
        subreddits_current_dist = current_datas['data']['dist']
        subreddits_count += subreddits_current_dist
        if after_pagination is not None:
            return self.get_subscribed_subreddits(after_pagination, subreddits_count, all_datas)
        else:
            return all_datas, subreddits_count

    def run_script(self):
        logging.info('reddit script is running...')

        create_directory(PD_SCRIPT_ROOT_PATH + "/" + self.application_name)

        username = self.get_username()

        saved_posts = self.get_saved_posts()

        suscribed_subreddits = self.get_subscribed_subreddits()

        logging.info('creating reddit log file')
        file_name = create_timestamped_and_named_file_name(self.application_name)
        file = open(file_name, "w", encoding="utf-8")

        logging.info('writing in reddit log file...')
        # processing of saved posts
        file.write("##### Saved posts of " + username + " reddit user (JSON) :")
        file.write("\n\n")
        file.write(username + " reddit user have " + str(saved_posts[1]) + " saved posts")
        file.write("\n\n")
        for json in saved_posts[0]:
            file.write(str(json))
            file.write("\n\n\n\n")
        # processing of subreddits
        file.write("##### Suscribed subreddits of " + username + " reddit user (list) :")
        file.write("\n\n")
        file.write(username + " reddit user have " + str(suscribed_subreddits[1]) + " suscribed subreddits")
        file.write("\n\n")
        for json in suscribed_subreddits[0]:
            children = json['data']['children']
            for subreddit in children:
                file.write(subreddit['data']['display_name_prefixed'])
                file.write("\n")
        file.write("\n\n")
        file.write("##### Suscribed subreddits of " + username + " reddit user (JSON) :")
        file.write("\n\n")
        for json in suscribed_subreddits[0]:
            file.write(str(json))
            file.write("\n\n\n\n")

        logging.info('writing in reddit log file done')
        file.close()

        # opens the file for reading only in binary format in order to upload
        file = open(file_name, "rb")

        upload_file_to_server_ftp(file, file_name, self.application_name)

        file.close()

        logging.info('reddit script is terminated')



