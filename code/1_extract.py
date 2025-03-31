import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# URLs
STATES_URL = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
SURVEY_URL = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"

if __name__ == '__main__':
    # Extract and save states.csv
    states_df = pd.read_csv(STATES_URL)
    states_df.to_csv(f"{CACHE_DIR}/states.csv", index=False)

    # Extract and save survey.csv with year column
    survey_df = pd.read_csv(SURVEY_URL)
    survey_df["year"] = survey_df["Timestamp"].apply(pl.extract_year_mdy)
    survey_df.to_csv(f"{CACHE_DIR}/survey.csv", index=False)

    # Extract COL data per year
    unique_years = survey_df["year"].dropna().unique()
    for year in unique_years:
        col_url = f"https://gist.githubusercontent.com/robertdfrench/801b4b9730c7a179c67192c0c57fc20d/raw/cost_of_living_{int(year)}.csv"
        try:
            col_df = pd.read_csv(col_url)
            col_df["year"] = int(year)
            col_df.to_csv(f"{CACHE_DIR}/col_{int(year)}.csv", index=False)
        except Exception as e:
            print(f"Failed to extract COL data for year {year}:", e)
