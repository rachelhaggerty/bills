#!/usr/bin/env python

""" 

Builds a Latent Dirichlet Allocation (LDA) model on the bill summary 
sentences and plots the results

"""

import os

import bokeh.plotting as bp
from bokeh.models import HoverTool
from bokeh.models import BoxSelectTool
from bokeh.plotting import figure
from bokeh.plotting import output_notebook
from bokeh.plotting import show
import lda
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE

import bills.preprocess as pp


class LDAModel(object):
    def __init__(self, local_dir, n_topics, n_iter):
        self.local_dir = local_dir
        self.preprocess= pp.TextPrep(local_dir)
        self.n_topics = n_topics 
        self.n_iter = n_iter
        self.cvz, self.terms = self.vectorize()
        self.topics, self.lda_model = self.lda_run()

    def vectorize(self):
        cvectorizer = CountVectorizer(max_df=.8,
                                      tokenizer=self.preprocess.tokenize_text)
        full_summaries = self.preprocess.summary_dict()
        summary_list = list(full_summaries.values())
        cvz = cvectorizer.fit_transform(summary_list)
        terms = cvectorizer.get_feature_names()
        return cvz, terms

    def lda_run(self):
        n_topics = self.n_topics
        n_iter = self.n_iter
        lda_model = lda.LDA(n_topics=n_topics, n_iter=n_iter)
        X_topics = lda_model.fit_transform(self.cvz)
        n_top_words = 8
        topic_summaries = []
        topic_word = lda_model.topic_word_  # get the topic words
        vocab = self.terms 
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
            topic_summaries.append(' '.join(topic_words))
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))     
            # return topic_words 
        return X_topics, lda_model
               
    def plot(self):
        svd = TruncatedSVD(n_components=25)
        svd_tfidf = svd.fit_transform(self.preprocess.tfidf_matrix)
        tsne_model = TSNE(n_components=2, verbose=1, n_iter=300)
        tsne_tfidf = tsne_model.fit_transform(svd_tfidf)
        tsne_lda = tsne_model.fit_transform(self.X_topics)
        doc_topic = self.lda_model.doc_topic_
        lda_keys = []
        for i, tweet in enumerate(summary_list):
                lda_keys += [doc_topic[i].argmax()]
        colormap = np.array(["#6d8dca", "#69de53", "#723bca", "#c3e14c",
                             "#c84dc9", "#68af4e", "#6e6cd5",
                             "#e3be38", "#4e2d7c", "#5fdfa8", "#d34690",
                             "#3f6d31", "#d44427", "#7fcdd8", "#cb4053",
                             "#5e9981", "#803a62", "#9b9e39", "#c88cca",
                             "#e1c37b", "#34223b", "#bdd8a3", "#6e3326",
                             "#cfbdce", "#d07d3c", "#52697d", "#7d6d33",
                             "#d27c88", "#36422b", "#b68f79"])
        plot_lda = bp.figure(plot_width=700, plot_height=600,
                             title="LDA topic visualization",
                             tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
                             x_axis_type=None, y_axis_type=None, min_border=1)
        lda_df = pd.DataFrame(tsne_lda, columns=['x','y'])
        lda_df['description'] = self.preprocess.summary_list
        lda_df['topic'] = lda_keys
        lda_df['topic'] = lda_df['topic'].map(int)
        plot_lda.scatter(source=lda_df, x='x', y='y', color=colormap[lda_keys])
        hover = plot_lda.select(dict(type=HoverTool))
        hover.tooltips={"description":"@description", "topic":"@topic"}
        show(plot_lda)
        

if __name__ == '__main__':
    model = LDAModel('./tx-data/', 15, 10)
    model.plot()
