#!/usr/bin/env python

"""

This module cleans, tokenizes, and creates a vocabulary
data frame for analysis using the summary sentences of the TX State House Bills

"""

import glob
import os
import re

from io import open
from nltk.stem.snowball import SnowballStemmer
from nltk import tokenize
import pandas as pd


class TextPrep(object):
    def __init__(self, local_dir):
        self.local_dir = local_dir
        self.files = glob.glob(self.local_dir + 'text/*.txt')

    def summary_list(self):
        summary_list = []
        for doc_name in self.files:
            with open(doc_name, 'rt') as in_file:
                full_text = in_file.read()
                sentences_list = tokenize.sent_tokenize(full_text)
                summary_tag = re.compile('A BILL TO BE ENTITLED')
                summary_sentences = list(filter(summary_tag.search,
                                                sentences_list))
                for sentence in summary_sentences:
                    cleaned_sentence = \
                        re.sub('.*A BILL TO BE ENTITLED AN ACT relating to ',
                               '', sentence)
            summary_list.append(cleaned_sentence)
        return summary_list

    def bill_name_list(self):
        bill_name_list = [doc_name.split('/')[-1].rstrip('.txt')
                          for doc_name in self.files]
        return bill_name_list

    def summary_dict(self):
        summary_dict = dict(zip(self.bill_name_list(), self.summary_list()))
        return summary_dict

    def tokenize_text(self, text):
        all_tokens = [word.lower()
                      for sent in tokenize.sent_tokenize(text)
                      for word in tokenize.word_tokenize(sent)]
        tokens = [token for token in all_tokens if re.search('[a-zA-Z]', token)]
        return tokens
 
    def tokenize_and_stem(self, text):
        stemmer = SnowballStemmer('english')
        stems = [stemmer.stem(token) for token in self.tokenize_text(text)]
        return stems
    
    def build_vocab_df(self):
        vocab_stemmed = [words_stemmed
                         for summary in self.summary_list()
                         for words_stemmed in self.tokenize_and_stem(summary)]
        vocab_tokenized = [words_tokenized
                           for summary in self.summary_list()
                           for words_tokenized in self.tokenize_text(summary)]
        vocab_df = pd.DataFrame({'words': vocab_tokenized},
                                index=vocab_stemmed)
        return vocab_df
