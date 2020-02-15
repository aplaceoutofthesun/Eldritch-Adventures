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
CLEAN_PATH = os.path.realpath(r'.\lovecraft_works')

def cmd_line_args():
    "Parse the command line arguments."
    parser = ArgumentParser()

    parser.add_argument('filename',
                        action='store')

    parser.add_argument('-d', '--directory',
                        action='store_true',
                        default=False)

    parser.add_argument('-o', '--output',
                        action='store')

    args = parser.parse_args()

    return args

###

def find_title(text):
    "Attempt to find the correct title for the story."
    title = ''
    for line in text:
        if re.findall(r'"\s?[bB]y', line):
            # print(line)
            title = line
    # Refactor to just take the text as a line c.f. opening file...
    # with open(text, 'r', encoding='utf-8') as open_file:
    #     txt = open_file.read().split('\n')
    #    print(f1[20:51])
    return title

def remove_unwanted(text):
    "Function to remove unwanted tokens from text."

    author = "HP-Lovecraft"

    # text = text.split('by') if 'by' in text else text.split('By')
    if 'by' in text:
        tit, _ = text.split('by')
    elif 'By' in text:
        tit, _ = text.split('By')
    elif 'Lovecraft\'s' in text:
        _, tit = text.split('s \"')
    # text = text.split()
    pattern = r'[\"\'\$\.\,]'
    # text = ' '.join([re.sub(pattern, '', x) for x in text])
    see = ''.join([re.sub(pattern, '', x) for x in tit])
    text = see.replace(' ', '_') + author

    # text = text.replace('"\'$by', '')
    return text


def clean_file(filename):
    "Opens the file for cleaning and save it when done."

    misc_unwanted = ['His Life',
                     'His Writings',
                     'His Creations',
                     'His Study',
                     'Popular Culture',
                     'Internet Resources',
                     'About This Site',
                     'Contact Us',
                     'Site Map',
                     'Home',
                     ]

    dirty_file = []
    text_main = []

    # lengths = []

    # logging.info("Test Path: %s", TEST_DIR_PATH)

    # for text in os.listdir(TEST_DIR)[:3]:
    #     pth = os.path.join(TEST_DIR, text)
        # print(pth, os.path.isfile(pth))
    with open(filename, 'r', encoding='utf-8') as open_file:
        # if text.endswith('py'):
            # continue
        # with open(pth, 'r', encoding='utf-8') as open_file:
        logging.info("Reading file %s...", filename)
        # text = open_file.read().split('\n')

        dirty_file = open_file.read().split('\n')

    if len(dirty_file) < 10:
        logging.debug("%s", filename)

    # Get the titles...
    # file_title = dirty_file[2].replace('\"', '')      # Title to rename file
    file_title = remove_unwanted(dirty_file[2])     # Title to rename file
    inside_title = dirty_file[2]    # Title for use at top of the book

    logging.info("Title: %s", inside_title)
    logging.info("File title: %s", file_title)

    # print(remove_unwanted(file_title))
    dirty_file = dirty_file[20:-28]

    # Add title to the top of the file plus one extra line...
    text_main.append(inside_title)
    text_main.append('\n')

    logging.info("Adding lines to clean file...")

    # x = dirty_file[-8:]
    # for i in x: print(dirty_file.index(i))
    # logging.info("%s ", ' * '.join(x))

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

def old_main():
    "Old stuff..."
    # Get the command line arguments
    logging.info("Getting command line arguments...")

    # args = cmd_line_args()

    #logging.info("Args: %s ", str(args))

    # filename = args.filename
    # directory = args.directory
    # output = args.output

    # if directory:
    #     os.getcwd()  # If directory is True, get the current directory.

    # if output:
    #     pass         # If output is not none, do something...
    #logging.info("Directory found: %s ", os.path.isdir(TEST_DIR))

def main():
    "Controls the functions, gets cmd line args, etc."

    # FIXME : Some files arent working e.g. Psychopompos

    # x = [x for x in os.listdir(TEST_DIR_PATH)]

    folders = ['fiction', 'essays', 'poetry', 'letters']

    for folder in folders:
        for txt in os.listdir(folder):
            if 'p139.txt' not in txt:
                continue
            # logging.debug("TXT = %s", txt)

            # logging.debug(filename)
            # filename = os.path.join(TEST_DIR_PATH, txt)

            filename = os.path.join(folder, txt)

            sparkling, title = clean_file(filename)
            CLEAN_PATH2 = r'.\abcde'
            # save_base = CLEAN_PATH  # FIXME: Why is this here?
            # save_loc = os.path.join(CLEAN_PATH2, folder)
            save_loc = os.path.realpath('abcde')

            logging.debug("SAVE LOC = %s", save_loc)

            # save_file_name = os.path.join(save_loc, title) + '.txt'
            save_file_name = title + '.txt'

            # savename = os.path.join(save_loc)
            logging.debug("SAVENAME = %s", save_file_name)
            # logging.debug("LENGTH = %d", len(sparkling))

            with open(save_file_name, 'w', encoding='utf-8') as out:
                for i in sparkling:
                    out.write(i + '\n')

    # File details...
    # Title can be found on line '3' (dirty_file[2]) of each file...


if __name__ == "__main__":
    # pass
    main()
# pylint: disable=C0103
