# Project Title

This is a text analysis of bills proposed in the Texas State House of
Representatives using Texas Legislature Online (TLO).

## Getting Started

This project uses Conda for its environment.

### Prerequisites


```
BeautifulSoup
NLTK
Pandas
Sci-Kit Learn
```

### Installing



```
Run setup.py or Makefile?
```

## Command Line Usage

Groups of 100 bill text HTML files can be downloaded from the TLO FTP using the
following script:
./bills/ftp_files.py <group name> #group name like HB00001_HB00099

The follow script will parse the HTML files and write individual txt files for each
bill's text to the local directory:
./bills/txt_files.py


## Built With

* [TLO](http://www.capitol.state.tx.us/)- Source of TX legistative bills
* [TLO Acceptable
  Use](ftp://ftp.legis.state.tx.us/Acceptable_Use_FTP_Public_Site.txt)-
  Acceptable use and FTP file structure


## Authors

* **Rachel Haggerty** - *Initial work* - [House
  Bills](https://github.com/rachelhaggerty/bills)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to http://brandonrose.org/clustering

