#!/usr/bin/env pythoni

""" Clean text for analysis """

from __future__ import print_function

import os
import re
import glob
from io import open

local_dir = '/Users/rhaggerty/remote/bills/tx/data/'


def summary_dict():
    summary_list = []
    bill_no_list = []
    summary_dict = {}
    for doc_name in glob.glob(local_dir + 'text/*.txt'):
        bill_no = doc_name.split('/')[-1].rstrip('.txt')
        with open(doc_name, 'rt') as in_file:
            full_text = in_file.read()
            sentences_list = tokenize.sent_tokenize(full_text)
            summary_tag = re.compile('A BILL TO BE ENTITLED')
            summary_sentences = filter(summary_tag.search, sentences_list)
            for sentence in summary_sentences:
                cleaned_sentence = \
                        re.sub('.*A BILL TO BE ENTITLED AN ACT relating to ', 
                                '', sentence)
        summary_list.append(cleaned_sentence)
        bill_no_list.append(bill_no)
    bill_summaries = zip(bill_no_list, summary_list)
    for bill, summary in bill_summaries:
        summary_dict[bill] = summary
    return summary_dict
