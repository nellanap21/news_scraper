# import libraries
import pandas as pd
import arrow
from openai import OpenAI
import logging
import os
from dotenv import load_dotenv

def summarize_articles(s3_folder_path):
    logger = logging.getLogger(__name__)

    # create filepaths with data
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY-MM-DD')
    articles_filepath = s3_folder_path + formatted_date + '/fox-data.csv'

    # create data frame of articles
    fox_articles = pd.read_csv(filepath_or_buffer=articles_filepath)
    logger.info("created dataframe")

    # add column for combined headline and article
    fox_articles['combined'] = ''
    fox_articles['combined'] = 'This is the start of an article. Here is the headline: ' + fox_articles[
        'headline'] + '. Here is the body: ' + fox_articles['article']
    logger.info("created combined column")

    # list to store short summary of each article
    short_summary = []

    # iterate through data frame and generate a summary for each article
    for row in fox_articles.itertuples():
        logger.info(row.combined)
        result = generate_summary(row.combined)
        short_summary.append(result.content)
    logger.info(short_summary)

    # create new column in data frame
    fox_articles['short_summary'] = short_summary
    logger.info(fox_articles)

    # create file path
    summaries_filepath = s3_folder_path + formatted_date + '/fox_summaries.csv'

    # stores in S3
    fox_articles.to_csv(path_or_buf=summaries_filepath, index=False)

    return fox_articles

def generate_summary(article):

    # setup logging
    logger = logging.getLogger(__name__)

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
                    "text": "You are a careful Fox news script writer that summarizes written Fox articles for YouTube."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "I am going to give you a Fox article. Write a script that summarizes the article in one paragraph with no line breaks. The paragraph has three sentences. The first sentence is a short summary of this headline in 10 words or less. The second and third sentences summarize the article in 50 words or less."
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Please provide the headlines and body of the articles you'd like summarized."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": article
                }
            ]
        }
    ])
    logger.info(completion.choices[0].message)
    return completion.choices[0].message
