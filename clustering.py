#!/usr/bin/env python

import glob
import os
import re

from io import open

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline

import text_cleaning as tc


class Clustering(object):
    def __init__(self, local_dir, num_clusters):
        self.local_dir = local_dir
        self.text_clean = tc.TextPrep(local_dir)
        self.num_clusters = num_clusters
        self.tfidf_matrix, self.terms = self.vectorize()
        self.clusters, self.top_terms_dict = self.cluster()

    def vectorize(self):
        tfidf_vectorizer = TfidfVectorizer(max_df=.8,
                                           stop_words='english',
                                           use_idf=True,
                                           tokenizer=self.text_clean.tokenize_and_stem
                                          )
        full_summaries = self.text_clean.summary_dict()
        summary_list = list(full_summaries.values())
        tfidf_matrix = tfidf_vectorizer.fit_transform(summary_list)
        terms = tfidf_vectorizer.get_feature_names()
        return tfidf_matrix, terms

    def cluster(self):
        num_clusters = self.num_clusters
        km = KMeans(n_clusters=num_clusters)
        km.fit(self.tfidf_matrix)
        clusters = km.labels_.tolist()
        vocab_df = self.text_clean.build_vocab_df()
        order_centroids = km.cluster_centers_.argsort()[:, ::-1] 
        top_terms_dict = {}
        for cluster in range(self.num_clusters):
            top_terms_list = []
            for ind in order_centroids[cluster, :10]: #replace 10 with n words per cluster
                top_terms = vocab_df.loc[self.terms[ind].split(' ')].values.tolist()[0][0]
                top_terms_list.append(top_terms)
            top_terms_dict[cluster] = top_terms_list    
        return clusters, top_terms_dict
           
    def plot(self):
        dist = 1 - cosine_similarity(self.tfidf_matrix)
        mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
        pos = mds.fit_transform(dist)
        xs, ys = pos[:, 0], pos[:, 1]
        color_list = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']
        cluster_colors = dict(zip(self.top_terms_dict.keys(), color_list))
        cluster_names = self.top_terms_dict
        cluster_df = pd.DataFrame(dict(x=xs,
                                       y=ys,
                                       label=self.clusters,
                                       title=self.text_clean.bill_name_list()))
        groups = cluster_df.groupby('label')
        fig, ax = plt.subplots(figsize=(17, 9))
        ax.margins(0.05)
        for name, group in groups:
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=10, 
                    label=cluster_names[name], color=cluster_colors[name], 
                    mec='none')
            ax.set_aspect('auto')
            ax.tick_params(axis= 'x',
                           bottom='off',
                           labelbottom='off',)
            ax.tick_params(axis= 'y', 
                           left='off',
                           labelleft='off')
        ax.legend(numpoints=1, loc='lower left', bbox_to_anchor=(0, -0.1))
        for i in range(len(cluster_df)):
            ax.text(cluster_df.loc[i]['x'], cluster_df.loc[i]['y'], cluster_df.loc[i]['title'], size=8)  
        plt.show()


if __name__ == '__main__':
    doit = Clustering('/Users/rhaggerty/remote/bills/tx/data/', 4)
    doit.plot()