# IR Project

Information Retrieval from Semi-Structured Data

## Brief

In this project, I have created an IR system for semi-structured data, in this case CSV (comma separated values) data. The data-set contains 8807 records of shows on [Netflix](https://netflix.com) - including the show name, director's name, cast, date of release, length/duration, genre and the plot.

The aim is to build a search engine for netflix shows, based on topics learnt throughout the information retrieval course and some concepts of natural language processing.

## Usage

First clone the repo and using `pip` install all the dependencies as mentioned in [requirements.txt](./requirements.txt)

For development mode, run 

```sh
./dev
```

For production mode, run

```sh
./prod
```

These commands will do the following

1. Clean the raw CSV data
2. Train the Doc2Vec model
3. Build Indexes
4. Run the flask server in dev/prod mode

The web application will be served at http://localhost:5000
