#!/usr/bin/env python

"""

This script grabs the text from the HTM files and
creates an individual .txt file for each bill in 
./tx-data/text 

These files include the text of the bills as a single Unicode string

"""

import glob
import os

from bs4 import BeautifulSoup
from io import open


def is_empty(file):
    file_size=os.stat(file).st_size
    if file_size == 0:
        print("The file {} is empty".format(file))
        return True
    return False


def prettify_soup(doc_name):
    bill_no = doc_name.split('/')[-1].rstrip('.htm')
    output_dir = os.path.join(os.getcwd(), 'tx-data/text/')
    if (is_empty(doc_name)):
        os.remove(doc_name)
    else:
        with open(doc_name, 'rt') as in_file:
            soup = BeautifulSoup(in_file, 'html.parser') 
            pretty_text = soup.get_text(' ', strip=True)
            with open(output_dir + bill_no + '.txt', 'w+', encoding='utf-8') as out_file:
                out_file.write(pretty_text)


if __name__ == '__main__':
    for doc_name in glob.glob(local_dir + 'html/*.htm'):
        prettify_soup(doc_name)
