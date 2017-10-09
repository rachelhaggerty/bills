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
        bills = {'names': self.text_clean.bill_name_list,
                 'synopsis': self.text_clean.summary_list,
                 'cluster': clusters
                }
        bills_df = pd.DataFrame(bills,
                                index = [clusters], 
                                columns = ['synopsis', 'cluster', 'names']
                               )
        vocab_df = self.text_clean.build_vocab_df()
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1] 
        for cluster in range(num_clusters):
            print("Cluster {}:".format(cluster + 1))

            for ind in order_centroids[cluster, :10]: #number of terms
                top_terms = vocab_df.loc[self.terms[ind].split(' ')].values.tolist()[0][0]
                print(' {}'.format(top_terms), end=',')
            print()
            
        return clusters
            
    def plot(self):
        dist = 1 - cosine_similarity(self.tfidf_matrix)
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(dist)
        xs, ys = pos[:, 0], pos[:, 1]
        cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}
        cluster_names = {0: 'school, public, finance, teacher', 
                         1: 'tax, ad, valorem, appraised, homestead', 
                         2: 'certain, criminal, state, offense', 
                         3: 'health, abortion, certain, physicians', 
        }

        cluster_df = pd.DataFrame(dict(x=xs,
                                       y=ys,
                                       label=self.cluster(),
                                       title=self.text_clean.bill_name_list())
                                       )
        groups = cluster_df.groupby('label')
        fig, ax = plt.subplots(figsize=(17, 9))
        ax.margins(0.05)

        for name, group in groups:
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
                    label=cluster_names[name], color=cluster_colors[name], 
                    mec='none')
            ax.set_aspect('auto')
            ax.tick_params(axis= 'x',
                           bottom='off',
                           labelbottom='off',)
            ax.tick_params(axis= 'y', 
                           left='off',
                           labelleft='off')

        ax.legend(numpoints=1)

        for i in range(len(cluster_df)):
            ax.text(cluster_df.loc[i]['x'], cluster_df.loc[i]['y'], cluster_df.loc[i]['title'], size=8)  

        plt.show()
