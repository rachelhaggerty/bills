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

local_dir = '/Users/rhaggerty/remote/bills/tx/data/'

def is_empty(file):
    file_size=os.stat(file).st_size
    if file_size == 0:
        print("The file {} is empty".format(file))
        return True
    return False


#make sure html file isn't empty, if it is, remove it
def prettify_soup(doc_name):
#     'HB00098I'
    bill_no = doc_name.split('/')[-1].rstrip('.htm')
    output_dir = os.path.join(local_dir, 'text/')
    
    if (is_empty(doc_name)):
        os.remove(doc_name)
    else:
        with open(doc_name, 'rt') as in_file:
            soup = BeautifulSoup(in_file, 'html.parser') 
            pretty_text = soup.get_text(' ', strip=True)
            with open(output_dir + bill_no + '.txt', 'w+', encoding='utf-8') as out_file:
                out_file.write(pretty_text)

for doc_name in glob.glob(local_dir + 'html/*.htm'):
    prettify_soup(doc_name)
