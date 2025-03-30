# import libraries
import datetime
from datetime import date
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import re
import json
import nltk
from nltk.tokenize import sent_tokenize
from openai import OpenAI
import os
from dotenv import load_dotenv



def tokenize(corpus):

    # TODO: consider not removing quotations
    # remove quotations with regex
    corpus_without_quotes = re.sub(r'"[^"]+"', '', corpus)

    # tokenize the corpus, creating a list of all words in the corpus
    tokens = sent_tokenize(corpus_without_quotes)

    return tokens


def generate_summary(fox_article, cnn_article):

    # load environmental variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {
            "role": "developer",
            "content": [
                {
                    "type": "text",
                    "text": "You are a careful news script writer that summarizes articles from Fox and CNN in an unbiased and even-handed manner."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": fox_article
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Thanks for sharing!"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": cnn_article
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Thank you for sharing this second set of sentences!"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Write a script comparing the two articles that has 3 sections. The first section extracts key points that are the same in both articles. The second section extracts key points that are in the CNN article but not the Fox article. The third section extracts key points that are in the Fox article but not the CNN article. Do not repeat points in any sections. The last sentence is a conclusion that highlights the biggest difference between the two articles."
                }
            ]
        }
    ])
    return completion.choices[0].message


def summarize_articles():
    logger = logging.getLogger(__name__)

    # create filepaths with data
    today = date.today()

    # for testing purposes
    # today = datetime.datetime(2025, 3, 28)

    articles_filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/articles.csv')

    # create data frame of articles
    articles = pd.read_csv(filepath_or_buffer=articles_filepath)

    # create new column tokenized by sentences
    articles["sentences"] = articles["article"].apply(tokenize)

    # add an initial sentence that tells GPT what the variable contains
    for row in articles.itertuples():
        if row.company == "Fox":
            row.sentences.insert(0, "This is a list of sentences from a Fox news article: ")
        if row.company == "CNN":
            row.sentences.insert(0, "This is a list of sentences from a CNN news article on the same topic: ")

    # initialize empty lists to create dataframe
    cnn_article = []
    fox_article = []

    # add lists of strings to create a dataframe
    for row in articles.itertuples():
        if row.company == "Fox":
            fox_article.append(json.dumps(row.sentences))
        if row.company == "CNN":
            cnn_article.append(json.dumps(row.sentences))

    # create dictionary of equal length lists
    raw_data = {"foxArticle": fox_article, "cnnArticle": cnn_article}

    # create new dataframe
    summaries = pd.DataFrame(raw_data)

    # initialize list to hold results from GPT
    comparison_articles = []

    # for every pair of articles, call generate_summary
    for row in summaries.itertuples():
        comparison_articles.append(generate_summary(row[1], row[2]))

    # initialize list to hold scripts
    scripts = []

    # create list of scripts
    for item in comparison_articles:
        scripts.append(item.content)

    # add scripts to data frame
    summaries["script"] = scripts

    # create file path
    summaries_filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/summaries.csv')
    summaries_filepath.parent.mkdir(parents=True, exist_ok=True)

    # stores CSV
    summaries.to_csv(path_or_buf=summaries_filepath, index=False)