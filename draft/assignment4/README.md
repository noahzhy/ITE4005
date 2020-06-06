# Recommender system

A recommender system or a recommendation system (sometimes replacing "system" with a synonym such as platform or engine) is a subclass of information filtering system that seeks to predict the "rating" or "preference" that a user would give to an item.
Recommender systems have become increasingly popular in recent years, and are utilized in a variety of areas including movies, music, news, books, research articles, search queries, social tags, and products in general. There are also recommender systems for experts, collaborators, jokes, restaurants, garments, financial services, life insurance, romantic partners (online dating), and Twitter pages.

## Movie recommender system
The purpose of this program(project) is to create a recommendation system based on the training data and to guess the new incoming data and to give the closest movie rating.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites & Installation

```
$ git clone http://hconnect.hanyang.ac.kr/2017_ITE4005_10066/2017_ITE4005_2012003716.git
$ cd 2017_ITE4005_2012003716/assignment4/
$ make
```

## Run the test

### Automatic test with sample input(Recomended)

```
$ bash ./run.sh

check out the output data with postfix ('.base_prediction.txt')
$ cd ./data/
```

### Manual test
** NOTICE: training data, test data and info data should be
prepared in a same directory before running the program **

```
$ ./bin/recommender [training_data] [test_data]

check out the output data with postfix ('.base_prediction.txt')
$ cd [training_data directory]
```

### Clean up the executable, output files

```
$ make clean
```

## Development environment

* Operating System: Ubuntu 14.05 LTS 64-bit
* Compilation: g++ compiler
* Language: C/C++ with C++ standard 11
* Source code editor: Vim
* Source code version control: Git
* This project follows HYU coding convention faithfully
* The movie rating data source: [movielens](http://grouplens.org/datasets/movielens/)

## Authors

* **Kwangil Cho**
    * student ID: 2012003716
    * senior of department of computer science
    * member of [Lab.SCS](http://scslab.hanyang.ac.kr/)
