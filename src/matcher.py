# import libraries
import datetime
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def jaccard_similarity(text1, text2):
    """
    Computes the Jaccard similarity score between two text strings.

    The Jaccard similarity is a measure of similarity between two sets, defined as the size of the
    intersection divided by the size of the union of the sets. This implementation uses whitespace
    to split the input strings into sets of words.

    Args:
        text1 (str): The first input text string.
        text2 (str): The second input text string.

    Returns:
        float: The Jaccard similarity score, a value between 0 and 1, where 0 indicates no similarity
        and 1 indicates identical sets.
    """
    #splits a string into a list based on whitespace
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def cosine_sim(text1, text2):
    """
        Compute cosine similarity between two text strings.

        This function calculates the cosine similarity, which is a metric
        commonly used to measure how similar two text strings are in terms
        of their vector representation. It uses TF-IDF (Term Frequency-Inverse
        Document Frequency) to vectorize the input strings and determines
        their similarity by calculating the cosine angle between their
        vector representations.

        Parameters:
            text1 (str): The first text input for similarity comparison.
            text2 (str): The second text input for similarity comparison.

        Returns:
            float: A value between -1 and 1 representing the cosine similarity
            score between the two input texts. A value closer to 1 indicates
            higher similarity, while a value closer to -1 indicates lower
            similarity.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

def find_matches(s3_folder_path):
    logger = logging.getLogger(__name__)

    # create filepaths with data
    today = datetime.date.today()

    # for testing purposes find articles from specific date
    # today = datetime.datetime(2025, 3, 28)

    cnn_filepath = s3_folder_path + today.strftime("%Y-%m-%d") + '/cnn-data.csv'
    fox_filepath = s3_folder_path + today.strftime("%Y-%m-%d") + '/fox-data.csv'

    # load into data frames
    cnn = pd.read_csv(filepath_or_buffer=cnn_filepath)
    fox = pd.read_csv(filepath_or_buffer=fox_filepath)

    # convert headline column to list
    cnn_headlines = cnn["headline"].tolist()
    fox_headlines = fox["headline"].tolist()

    # Create a matrix to hold jaccard similarity scores
    jac_matrix = pd.DataFrame(np.empty((len(fox_headlines), len(cnn_headlines))))

    # initialize list to hold matches
    jac_matches = []

    # iterate through every pair of articles and calculate score
    for i in range(len(fox_headlines)):
        for j in range(len(cnn_headlines)):
            similarity = jaccard_similarity(fox_headlines[i], cnn_headlines[j])
            jac_matrix.at[i, j] = similarity
            # TODO use ML to determine best cutoff value
            if similarity > 0.15:
                jac_matches.append(tuple([i, j]))

    logger.info(jac_matches)
    # Create a matrix to hold cosine similarity scores
    cos_matrix = pd.DataFrame(np.empty((len(fox_headlines), len(cnn_headlines))))

    # initialize list to hold matches
    cos_matches = []
    # iterate through every pair of articles and calculate score
    for i in range(len(fox_headlines)):
        for j in range(len(cnn_headlines)):
            similarity = cosine_sim(fox_headlines[i], cnn_headlines[j])
            cos_matrix.at[i, j] = similarity
            # How to determine best cutoff value
            if similarity > 0.25:
                cos_matches.append(tuple([i, j]))

    logger.info(cos_matches)
    # First find unique tuples from both Jaccard and Cosine similarity
    unique_set = set(jac_matches + cos_matches)

    # convert back to list
    unique_matches = list(unique_set)
    unique_matches.append((6,1))
    logger.info(unique_matches)

    # check if no matches found
    if len(unique_matches) == 0:
        return None

    # create lists of equal length to hold data
    companies = []
    headlines = []
    articles = []

    # iterate through matches and append articles to lists
    for tup in unique_matches:
        companies.append(fox.iat[tup[0], 0])
        headlines.append(fox.iat[tup[0], 1])
        articles.append(fox.iat[tup[0], 2])
        companies.append(cnn.iat[tup[1], 0])
        headlines.append(cnn.iat[tup[1], 1])
        articles.append(cnn.iat[tup[1], 2])

    # create dictionary of equal length lists
    raw_data = {"company": companies, "headline": headlines, "article": articles}

    # create data frame
    articles = pd.DataFrame(raw_data)

    # create file path
    articles_filepath = s3_folder_path + today.strftime("%Y-%m-%d") + '/articles.csv'

    # stores CSV
    articles.to_csv(path_or_buf=articles_filepath, index=False)

    return 1