from __future__ import print_function

import os
from ftplib import FTP
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import TransformerMixin
from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer
# import nltk
from nltk.corpus import stopwords
from nltk import tokenize
import string
import numpy as np
import re
import glob
from io import open


#do this stuff? ionno
# import nltk 
# nltk.download("stopwords")
# nltk.download('punkt')


summary_list = []
bill_no_list = []
summary_dict = {}
for doc_name in glob.glob(local_dir + 'text/*.txt'):
    bill_no = doc_name.split('/')[-1].rstrip('.txt')
    with open(doc_name, 'rt') as in_file:
        thing = in_file.read()
        sentences_list = tokenize.sent_tokenize(thing)
        summary = sentences_list[2]
    summary_list.append(summary)
    bill_no_list.append(bill_no)
bill_summaries = zip(bill_no_list, summary_list)
for bill, summary in bill_summaries:
    summary_dict[bill] = summary
print(summary_dict)
