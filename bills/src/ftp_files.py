#!/usr/bin/env python
"""

This script pulls 100 State of Texas House Bill HTML files of the 851
legislative session from state.tx.us FTP server and saves them locally
as individual .htm files.

Usage: ./bills/src/ftp_files.py <group name> #group name like HB00001_HB00099

The naming convention for individual documents is: <bill chamber><bill type><bill suffix><bill version>
File Name   Description
<bill chamber>  H=House, S=Senate
<bill type> B=Bill, J=Joint Resolution, R=Resolution, C=Concurrent Resolution
<bill suffix>   5-digit number
<bill version>  I=Introduced, S=Senate Committee Report, H=House Committee Report, E=Engrossed, F=Enrolled

FTP Directory structure:
/bills/<legislative session>/<document type>/<text format>/<bill type>/<grouping of 100 bills>

"""

import os
import sys

from ftplib import FTP


def get_files():
    ftp = FTP('ftp.legis.state.tx.us')
    ftp.login()
    ftp.cwd('/bills/851/billtext/html/house_bills/{}'.format(sys.argv[1]))
    files = ftp.nlst()
    html_dir = 'tx-data/html'
    if not os.path.exists(html_dir):
            os.makedirs(html_dir)

    for file in files:
        html_filename = os.path.join(html_dir, file)
        print("Getting filename " + file)
        ftp.retrbinary('RETR {}'.format(file), open(html_filename, 'wb').write)
        print("Saving at {}".format(html_filename))


if __name__ == '__main__':
    get_files()
