#            )                              (                                                   )
#         ( /(         (        (      )    )\ )      (  (                    (   (          ( /(
#  `  )   )\())  (    ))\  (    )\  ( /(   (()/(  (   )\))(    (      (    (  )(  )\  `  )   )\())
#  /(/(  ((_)\   )\  /((_) )\ )((_) )\())   ((_)) )\ ((_)()\   )\ )   )\   )\(()\((_) /(/(  (_))/
# ((_)_\ | |(_) ((_)(_))  _(_/( (_)((_)\    _| | ((_)_(()((_) _(_/(  ((_) ((_)((_)(_)((_)_\ | |_
# | '_ \)| ' \ / _ \/ -_)| ' \))| |\ \ /  / _` |/ _ \\ V  V /| ' \)) (_-</ _|| '_|| || '_ \)|  _|
# | .__/ |_||_|\___/\___||_||_| |_|/_\_\  \__,_|\___/ \_/\_/ |_||_|  /__/\__||_|  |_|| .__/  \__|
# |_|


# Author :
# +-+-+-+-+-+-+-+-+-+
# |I|A|m|T|e|r|r|o|r|
# +-+-+-+-+-+-+-+-+-+

# Licence :
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

# Notes :
# Python script tested on Ubuntu Linux. It can run on Windows with minor adjustements.


########################################################################################################################

########################################################################################################################

# !/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from trello_sample import *
from twitter_sample import *
from constants import *
from trello_script import *
from firefox_script import *
from jdownloader_script import *
from twitter_script import *
from steam_sample import *
from steam_script import *
from reddit_sample import *
from reddit_script import *
from setup_logger import *


# MAIN SCRIPT ----------------------------------------------------------------------------------------------------------

# TODO : gérer exceptions (erreurs)
# TODO : alertes en cas d'erreur + envoi de fichier de log (mail, trello)

logging.info('Phoenix Down Script started !')

logging.info("creating the root path directory of Phoenix Down Script...")
create_directory(PD_SCRIPT_ROOT_PATH)

# tlls = TrelloScript()
# tlls.run_script()

# fs = FirefoxScript()
# fs.run_script()

# js = JdownloaderScript()
# js.run_script()

# twts = TwitterScript()
# twts.run_script()

# stms = SteamScript()
# stms.run_script()

rs = RedditScript()
rs.run_script()

logging.info('Phoenix Down Script finished !')

logger_script()


# SAMPLE REQUESTS ------------------------------------------------------------------------------------------------------

# TRELLO SAMPLE
# get_board_by_id_sample_version(TRELLO_MBL_BOARD_ID)
# get_open_cards_by_board_id_sample_version(TRELLO_MBL_BOARD_ID)
# get_card_by_id_sample_version(TRELLO_CH_CARD_ID)
# get_boards_by_member_username_sample_version(TRELLO_MEMBER_USERNAME)

# TWITTER SAMPLE
# get_timeline()
# update_status()
# get_user_by_id(TWITTER_USER_ID)
# get_followers_id(TWITTER_USER_ID)
# get_friends_id(TWITTER_USER_ID)
# get_all_tweets_for_a_user(TWITTER_USER_ID) # WARNING : very long processing time
# get_rate_limit_status()
# WARNING : Rate limit window per 15 minutes = 15 requests x 20 followers per page = 300 followers
# get_followers(TWITTER_USER_ID)

# STEAM SAMPLE
# get_user_name(STEAM_USER_ID)
# get_game_name_by_id(546560) # Half-Life : Alyx AppId
# get_friend_list()
# get_owned_games()
# get_wishlist()

#REDDIT SAMPLE
# reddit_request_token()
# get_my_identity()
# get_saved_posts()
# get_subscribed_subreddits()


