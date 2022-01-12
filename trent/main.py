# System
import sys
import getpass
import logging
import json
import time


# Third Party
import configargparse
import requests
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Globals
log = None
args = None


def process_command_line():

    global log
    global args

    # Create argument parser
    parser = configargparse.ArgumentParser(description='A command line tool that snipes Sandbox lands')

    # Environment
    parser.add_argument("--environment",
                        dest="environment",
                        default="default",
                        env_var='ENVIRONMENT',
                        help="Metrics environment (eg. 'production', 'staging', 'default')")

    # Parse out the arguments
    args = parser.parse_args()

    # Prompt for secrets, if not supplied
    # if args.aws_access_key_id is None:
    #     args.aws_access_key_id = getpass.getpass("metrics-producer user AWS access key ID: ")
    # if args.aws_secret_access_key is None:
    #     args.aws_secret_access_key = getpass.getpass("metrics-producer user AWS secret access key: ")

def run_job():
    driver = webdriver.Chrome("./chromedriver")

    driver.get('http://www.yahoo.com')
    assert 'Yahoo' in driver.title

    elem = driver.find_element(By.NAME, 'p')  # Find the search box
    elem.send_keys('seleniumhq' + Keys.RETURN)
    time.sleep(5) # Let the user actually see something!

    driver.quit()

def main(argv):

    global log
    global args

    # Configure logging
    log = logging.getLogger(__name__)
    log_stream_handler = logging.StreamHandler(sys.stdout)
    log_stream_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    log_stream_handler.setLevel(logging.INFO)
    log.addHandler(log_stream_handler)
    log.setLevel(logging.INFO)

    log.info('Enter...')

    # Process arguments
    process_command_line()

    # Load list of LANDS
    lands_file_path = "lands.json"  # Get from command line, with default
    lands_file = open(lands_file_path)
    lands = json.load(lands_file)

    for land in lands:
        print(land)

    log.info("Before start threads")
    first = threading.Thread(target=run_job)
    second = threading.Thread(target=run_job)
    first.start()
    second.start()
    log.info("Threads started")
    log.info("Waiting for first thread to finish")
    first.join()
    log.info("First thread done")
    log.info("Waiting for second thread to finish")
    second.join()
    log.info("Second thread done")

    log.info('...Exit')


if __name__ == "__main__":
   main(sys.argv[1:])
