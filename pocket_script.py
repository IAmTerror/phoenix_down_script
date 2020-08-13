from utilities import *
from constants import *
from credentials import *
import requests
import requests.auth
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
import sys


class PocketScript:
    def __init__(self):
        self.application_name = "pocket"

    def pocket_request_token(self):
        url = "https://getpocket.com/v3/oauth/request"
        payload = {"consumer_key": POCKET_CONSUMER_KEY, "redirect_uri": "pocketapp1234:authorizationFinished"}
        response = requests.request("POST", url, params=payload)
        datas = response.text
        split_datas = datas.split("=")
        request_token = split_datas[1]
        return request_token

    def authorize_app_and_get_access_token(self):
        code = self.pocket_request_token()
        redirect_uri = "pocketapp1234:authorizationFinished"

        # For Firefox we need to set a headless flag to inform browser not to use gui.
        firefox_bin = '/usr/bin/geckodriver'
        os.environ['MOZ_HEADLESS'] = '1'

        # We are using Selenium to send login form with obtained in previous step request token. Keep in mind that
        # different providers will have different login form. You need to check field ids you will be populating with
        # data.
        binary = FirefoxBinary(firefox_bin, log_file=sys.stdout)

        driver = webdriver.Firefox()
        driver.get('https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}'.format(code, redirect_uri))
        driver.find_element_by_id('feed_id').send_keys(POCKET_USERNAME)
        driver.find_element_by_id('login_password').send_keys(POCKET_PASSWORD)
        driver.find_element_by_class_name('btn-authorize').click()
        driver.close()

        url = "https://getpocket.com/v3/oauth/authorize"
        payload = {"consumer_key": POCKET_CONSUMER_KEY, "code": code}
        response = requests.request("POST", url, params=payload)
        datas = response.text
        split_datas = datas.replace('=', ' ').replace('&', ' ').split()
        access_token = split_datas[1]
        return access_token

    def get_user_datas(self):
        access_token = self.authorize_app_and_get_access_token()
        url = "https://getpocket.com/v3/get"
        payload = {"consumer_key": POCKET_CONSUMER_KEY, "access token": access_token}
        response = requests.request("POST", url, params=payload)
        datas = response.text
        return datas

    def run_script(self):
        logging.info('pocket script is running...')

        create_directory(PD_SCRIPT_ROOT_PATH + "/" + self.application_name)