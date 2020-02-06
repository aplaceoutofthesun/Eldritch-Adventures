#!/usr/bin/env python3
#
"""Retrieve the collection of H.P. Lovecraft texts from the
H. P. Lovecraft Archive. http://www.hplovecraft.com/
"""

import os
import logging
import time
import requests

from bs4 import BeautifulSoup
from random import randint  # pylint: disable=wrong-import-order
from requests.exceptions import HTTPError

ADDR = 'http://www.hplovecraft.com/writings/texts/'
LOG_CONF = "[+] %(asctime)s -%(levelname)s - %(message)s"
LOVECRAFT_PATH = os.path.join(os.path.dirname(__file__), 'Lovecraft')

# Set up the logger.
logging.basicConfig(format=LOG_CONF,
                    level=logging.INFO)

def main():
    "Download the lovecraft files..."

    logging.info('Requesting links...')
    req = requests.get(ADDR)

    try:
        req.raise_for_status()
    except HTTPError as exc:
        print(exc.with_traceback)

    logging.info('Preparing soup...')
    soup = BeautifulSoup(req.text, 'lxml')

    logging.info('Parsing links...')
    links = []
    for link in soup.findAll('a'):
        lnk = link.get('href')
        if lnk is not None:
            links.append(lnk)

    parsed_links = {
        "fiction" : [x for x in links if x.startswith('fiction')],
        "poetry" : [x for x in links if x.startswith('poetry')],
        "essays" : [x for x in links if x.startswith('essays')],
        "letters" : [x for x in links if x.startswith('letters')]
        }
    logging.info('Finished link parsing...')

    # print(fiction)

# Set up the logger.
    prefixes = ["fiction", "poetry", "essays", "letters"]
    # prefixes = ["letters"]

    logging.info('Downloading files...')

    for pre in prefixes:

        # Define a path to save the files.
        save_path = os.path.join(LOVECRAFT_PATH, pre)

        if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=False)

        for link in parsed_links[pre]:
            target = ''.join((ADDR, link))
            logging.info('Getting page: %s', target)

            time.sleep(randint(1, 5))
            try:
                req = requests.get(target)
                req.raise_for_status()

                soup = BeautifulSoup(req.text, 'lxml')

                unclean_text = soup.text.split('\r\n')

                clean_name = os.path.split(link)[-1].replace('aspx', 'txt')
                filename = os.path.join(save_path, clean_name)

                logging.debug('Writing %s to disk:', filename)
                with open(filename, 'w', encoding='utf-8') as outfile:
                    for line in unclean_text:
                        outfile.write(line)
                logging.debug('Writing Completed. Continuing...')

            except HTTPError as exc:
                logging.exception('HTTPError has occurred!')

        logging.info('Link %s completed. Continuing...', pre)

    logging.info('Operation complete')


if __name__ == "__main__":
    main()
