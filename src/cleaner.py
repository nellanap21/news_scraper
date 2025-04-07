from datetime import date
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
import re
import json
import arrow

def clean_scripts(s3_folder_path):

    # get filepath with data
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY-MM-DD')
    summaries_filepath = s3_folder_path + formatted_date + '/summaries.csv'

    # create data frame
    scripts = pd.read_csv(filepath_or_buffer=summaries_filepath)

    # remove instances of "Script:"
    for index, row in scripts.iterrows():
        # TODO: replace logic with regex
        new_script = scripts.at[index, 'script'].replace("**Script:",
                                                        "Welcome to Panoramic News. Many people consider CNN left-wing and Fox right-wing, so the best way to get unbiased news is to compare both sides. My goal is to summarize CNN and Fox articles so you can get a panoramic view of the news. Now, ")
        scripts.at[index, 'script'] = new_script


    # remove instances of "Script"
    for index, row in scripts.iterrows():
        new_script = scripts.at[index, 'script'].replace("**Script", "Welcome to Panoramic News. Many people consider CNN left-wing and Fox right-wing, so the best way to get unbiased news is to compare both sides. My goal is to summarize CNN and Fox articles so you can get a panoramic view of the news. Now, ")
        scripts.at[index, 'script'] = new_script


    # remove instances of "**Conclusion:**"
    for index, row in scripts.iterrows():
        new_script = scripts.at[index, 'script'].replace("**Conclusion:**", "In conclusion, ")
        scripts.at[index, 'script'] = new_script


    # remove instances of "**Conclusion**"
    for index, row in scripts.iterrows():
        new_script = scripts.at[index, 'script'].replace("**Conclusion**", "In conclusion, ")
        scripts.at[index, 'script'] = new_script

    # remove instances of "Section 1:" "Section 2:" and "Section 3:"
    for index, row in scripts.iterrows():
        new_script = scripts.at[index, 'script'].replace("**Section 1: ", "").replace("**Section 2: ", "").replace("**Section 3: ", "")
        scripts.at[index, 'script'] = new_script

    # remove instances of "1." "2." "3." "4." "5."
    for index, row in scripts.iterrows():
        new_script = scripts.at[index, 'script'].replace("1. ", "").replace("2. ", "").replace("3. ", "").replace("4. ", "").replace("5. ", "")
        scripts.at[index, 'script'] = new_script

    # remove dashes
    for index, row in scripts.iterrows():
        new_script = scripts.at[index, 'script'].replace("- ", "").replace("---", "")
        scripts.at[index, 'script'] = new_script

    # replace ending ** with .
    for index, row in scripts.iterrows():
        new_script = scripts.at[index, 'script'].replace("**", ".")
        scripts.at[index, 'script'] = new_script

    # create file path
    scripts_filepath = s3_folder_path + formatted_date + '/scripts.csv'

    # store CSV
    scripts.to_csv(path_or_buf=scripts_filepath, index=False)