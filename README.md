# A Text Analysis of Texas State House of Representatives Bills

This is a text analysis of bills proposed in the Texas State House of
Representatives to extract thematic and semantic topics using several Natural Language Processing techniques, including K-Means Clustering and Latent Dirichlet Allocation (LDA).

## Getting Started

This project uses Python 3.6 and Conda for its environment.


### Installing

```
(1) clone the repository
(2) run $ conda env create
(3) run $ source activate ENV_NAME

Download NLTK (nltk.download())
```

## Downloading the Data

(1) Groups of 100 raw HTML files can be downloaded from the Texas Legislative Online (TLO) FTP using the
following script (one file per bill):

```
./bills/src/ftp_files.py <group name> #group name like `HB00001_HB00099`
```
  
  Example bill: ftp://ftp.legis.state.tx.us/bills/851/billtext/html/house_bills/HB00001_HB00099/HB00001E.htm

(2) Next, parse the text from the HTML files and create a plain text file for each
bill:

```
./bills/src/txt_files.py
```

## Techniques for Topic Extraction

**K-Means**

This technique is only analyzing the summary sentences. It uses Tfidf Vectorizer, K-Means Clustering, and plots the clusters using Multi-Dimensional Scaling (MDS):
<img width="974" alt="screen shot 2017-11-20 at 9 34 57 am" src="https://user-images.githubusercontent.com/19957892/33027285-4d146c70-cdd8-11e7-83d1-db01ffe441df.png">

```
./bills/clustering.py
```

**Latent Dirichlet Allocation (LDA)**

This technique analyzes the summary sentences using Count Vectorizer, LDA, and plots the clusters using Singular Value Decomposition (SVD) and t-distributed Stochastic Neighbor Embedding (TSNE):
<img width="687" alt="screen shot 2017-11-20 at 12 17 26 pm" src="https://user-images.githubusercontent.com/19957892/33034320-13661d1a-cded-11e7-982d-6e266b2158ac.png">
<img width="794" alt="screen shot 2017-11-20 at 12 17 48 pm" src="https://user-images.githubusercontent.com/19957892/33034398-4e3f48bc-cded-11e7-922e-eea78932a1de.png">




## Built With

* [TLO](http://www.capitol.state.tx.us/)- Source of TX legistative bills
* ftp://ftp.legis.state.tx.us/Acceptable_Use_FTP_Public_Site.txt -
  Acceptable use and FTP file structure


## Authors

* **Rachel Haggerty** - *Initial work* - [House
  Bills](https://github.com/rachelhaggerty/bills)


## Acknowledgments

* https://arxiv.org/pdf/1701.00185.pdf
* https://arxiv.org/abs/1510.03820
* http://brandonrose.org/clustering
* https://ahmedbesbes.com/how-to-mine-newsfeed-data-and-extract-interactive-insights-in-python.html

