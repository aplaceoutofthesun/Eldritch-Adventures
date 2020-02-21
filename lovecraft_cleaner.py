#!/usr/bin/env python
#
"""Clean up the lovecraft files that were downloaded in lovecraft.py"""

import os
import re
import logging

from argparse import ArgumentParser

LOG_CONFIG = '%(asctime)s - %(levelno)s - %(message)s - [%(lineno)d]'
logging.basicConfig(format=LOG_CONFIG, level=3)

# Directory with small number of files to test
TEST_DIR = r".\test_clean"
TEST_DIR_PATH = os.path.realpath(r".\test_clean")
CLEAN_PATH = os.path.realpath(r'.\lovecraft_works_again')

def cmd_line_args():
    "Parse the command line arguments."
    parser = ArgumentParser()

    parser.add_argument('filename', action='store')
    parser.add_argument('-o', '--output', action='store')
    args = parser.parse_args()
    return args
###

def find_title(text):
    """Attempt to find the correct title for the story, otherwise returns a
    blank.

    The title is generally preceeded by the word 'by' (lower and upper cases),
    however in at least one case the title follows the genitive/possessive
    'Lovecraft's'.
    """
    title = ''
    for line in text:
        if re.findall(r'"\s?[bB]y', line):
            title = line
    return title

def remove_unwanted(text):
    """Split's the text and removes unwanted tokens from the text."""

    author = "HP-Lovecraft"

    if 'by' in text:
        tit, _ = text.split('by')
    elif 'By' in text:
        tit, _ = text.split('By')
    elif 'Lovecraft\'s' in text:
        _, tit = text.split('s \"')

    # Must remove ':' and '[]' from titles, or problems. (esp. Psychopompous)
    pattern = r'[\"\'\$\.\,\[\]\:\;\_\-]'
    # text = ' '.join([re.sub(pattern, '', x) for x in text])
    see = ''.join([re.sub(pattern, '', x) for x in tit])
    text = see.replace(' ', '_') + author

    return text


def clean_file(filename):
    """Opens the file for cleaning and save it when done."""

    misc_unwanted = ['His Life', 'His Writings',
                     'His Creations', 'His Study',
                     'Popular Culture', 'Internet Resources',
                     'About This Site', 'Contact Us',
                     'Site Map', 'Home',
                     ]

    dirty_file = []
    text_main = []

    with open(filename, 'r', encoding='utf-8') as open_file:
        logging.info("Reading file %s...", filename)
        dirty_file = open_file.read().split('\n')

    if len(dirty_file) < 10:
        logging.debug("%s", filename)

    # Get the titles...
    # file_title = dirty_file[2].replace('\"', '')      # Title to rename file
    file_title = remove_unwanted(dirty_file[2])     # Title to rename file
    if not re.findall(r'[\[\]\(\)]', dirty_file[2]):
        inside_title = dirty_file[2]    # Title for use at top of the book
    else:
        inside_title = remove_unwanted(dirty_file[2])

    logging.info("Title: %s", inside_title)
    logging.info("File title: %s", file_title)

    # print(remove_unwanted(file_title))

    dirty_file = dirty_file[20:-28]

    # logging.info("%s", dirty_file)
    # Add title to the top of the file plus one extra line...
    text_main.append(inside_title)
    text_main.append('\n')


    logging.info("Adding lines to clean file...")

    for line in dirty_file[:-8]:
        line = line.replace(u'\xa0', '')
        if 'H. P. Lovecraft' in line:
            continue
        if len(line) <= 2:
            continue
        if 'Return to' in line  \
                or 'Page Last' in line   \
                or 'URL:' in line:
            continue
        if line not in misc_unwanted:
            text_main.append(line+'\n')

    return text_main, file_title

# TODO: Clean up file...
def main():
    """Controls the functions, gets cmd line args, etc."""

    # Folders replicate downloaded files and website organisation.
    folders = ('fiction', 'essays', 'poetry', 'letters') # Consider a tuple...
    # folders = ('poetry', 'letters')


    for folder in folders:
        # Assumes we are in the base folder 'Lovecraft'

        save_folder = os.path.join(CLEAN_PATH, folder)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder, exist_ok=False)

        for txt in os.listdir(folder):
            # if 'p139.txt' not in txt:
            #     continue
            # logging.debug("TXT = %s", txt)

            # logging.debug(filename)
            # filename = os.path.join(TEST_DIR_PATH, txt)

            filename = os.path.join(folder, txt)

            # Get the clean text and the title.
            sparkling, title = clean_file(filename)
            # logging.info("%s", sparkling)
            # CLEAN_PATH2 = r'.\Test_directory'
            # CLEAN_PATH2 = r'.'

            # save_base = CLEAN_PATH
            # save_loc = os.path.join(CLEAN_PATH2, folder)
            save_loc = os.path.join(os.path.realpath(CLEAN_PATH), folder)

            # logging.debug("SAVE LOC = %s", save_loc)

            # save_file_name = os.path.join(save_loc, title) + '.txt'
            save_file_name = title + '.txt'

            savename = os.path.join(save_loc, save_file_name)
            # logging.debug("SAVENAME = %s", save_file_name)
            # logging.debug("LENGTH = %d", len(sparkling))

            # logging.debug("SPARKLE TYPE = %s", type(savename))
            # with open('PSYCHOFUCKER.txt', 'w', encoding='utf-8') as fucker:
            #     logging.info("%s", type(fucker))
            #     # fucker.writelines(sparkling)
            #     for line in sparkling:
            #         logging.info("%s", line)
            #         fucker.writelines(line)
            # with open(save_file_name, 'w', encoding='utf-8') as out:

            with open(savename, 'w', encoding='utf-8') as out:
                for i in sparkling:
                    # logging.info("%s", i)
                    out.write(i + '\n')

    # File details...
    # Title can be found on line '3' (dirty_file[2]) of each file...


if __name__ == "__main__":
    # pass
    main()
# pylint: disable=C0103
