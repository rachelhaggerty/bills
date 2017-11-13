# A Text Analysis of Texas State House of Representatives Bills

This is a text analysis of bills proposed in the Texas State House of
Representatives to extract thematic and semantic topics using several NLP techniques, including K-Means Clustering.

## Getting Started

This project uses Python 3.6 and Conda for its environment.


### Installing

```
(1) clone the repository
(2) run $ conda env create
(3) run $ source activate ENV_NAME
```

## Command Line Usage

Groups of 100 bill raw HTML files can be downloaded from the Texas Legislative Online (TLO) FTP using the
following script:

```
./bills/ftp_files.py <group name> #group name like HB00001_HB00099
```
  
  Example bill: ftp://ftp.legis.state.tx.us/bills/851/billtext/html/house_bills/HB00001_HB00099/HB00001E.htm

The follow script will parse the text from the HTML files and write individual txt files for each
bill to the local directory:

```
./bills/txt_files.py
```

## Techniques for Topic Extraction

**K-Means**
This technique is only analyzing the summary sentences. It uses Tfidf Vectorizer, K-Means Clusters, and plotting using MDS, similar to the tutorial at brandonrose.org/clustering:
<img width="973" alt="screen shot 2017-11-13 at 1 35 17 pm" src="https://user-images.githubusercontent.com/19957892/32745389-2fcb97c0-c878-11e7-8f39-b2d5d4e7ff36.png">



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

