from credentials import *
from constants import *
import os
import time
from ftplib import FTP


def create_directory(path):
    # If the work directory doesn't existe yet...
    # ... creation of this directory
    if not os.path.isdir(path):
        os.makedirs(path)
        print("The folder " + path + " was successfully created")
    else:
        print("The folder " + path + " already exists")

    # Designation of the working directory as current directory
    os.chdir(path)


def create_timestamped_and_named_file(application_name):
    current_date = time.strftime("%Y%m%d")
    current_time = time.strftime("%H%M%S")
    format_file_name = current_date + "_" + current_time + "_" + application_name + "_log_phoenix_down.txt"
    return format_file_name


def upload_file_to_server_ftp(file, filename, application_name):
    ftp = FTP(SEEDBOX_DOMAIN_NAME)  # connect to host, default port
    ftp.login(user=SEEDBOX_USER_NAME, passwd=SEEDBOX_PASSWD)  # login with credentials
    # TODO: gérer une exception en cas de log impossible
    ftp.retrlines('LIST')  # LIST retrieves a list of files and information about those files
    ftp.cwd(SEEDBOX_ROOT_PD_SCRIPT_PATH + "/" + application_name)  # Set the current directory on the server
    ftp.storbinary('STOR ' + filename + '', file)  # uploading file to the server
    ftp.quit()

