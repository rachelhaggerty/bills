#!/usr/bin/env pythoni

""" Clean, tokenize, feature extraction for analysis """

import glob
import os
import re
from io import open

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import tokenize
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity

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
            summary_sentences = list(filter(summary_tag.search, sentences_list))
            for sentence in summary_sentences:
                cleaned_sentence = \
                        re.sub('.*A BILL TO BE ENTITLED AN ACT relating to ', 
                                '', sentence)
        summary_list.append(cleaned_sentence)
        bill_no_list.append(bill_no)
    bill_summaries = list(zip(bill_no_list, summary_list))
    for bill, summary in bill_summaries:
        summary_dict[bill] = summary
    return summary_dict


def tokenize_text(text):
    tokens = [word.lower() for sent in tokenize.sent_tokenize(text) for word in tokenize.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def tokenize_and_stem(text):
    stemmer = SnowballStemmer('english')
    allwords_tokenized = tokenize_text(text)
    stems = [stemmer.stem(t) for t in allwords_tokenized]
    return stems


def build_vocab_df():
    full_summaries = summary_dict()
    summary_list = list(full_summaries.values())
    names_list = list(full_summaries.keys())
    vocab_stemmed = []
    vocab_tokenized = []
    for summary in summary_list:
        words_tokenized = tokenize_text(summary)
        words_stemmed = tokenize_and_stem(summary)

        vocab_tokenized.extend(words_tokenized)
        vocab_stemmed.extend(words_stemmed)

    vocab_df = pd.DataFrame({'words': vocab_tokenized}, index = vocab_stemmed)
    return vocab_df


tfidf_vectorizer = TfidfVectorizer(max_df=.8, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem,)
full_summaries = summary_dict()
summary_list = list(full_summaries.values())
tfidf_matrix = tfidf_vectorizer.fit_transform(summary_list)
terms = tfidf_vectorizer.get_feature_names()
