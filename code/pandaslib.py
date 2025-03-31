from datetime import datetime
import re
import pandas as pd

def clean_currency(item: str) -> float:
    '''
    Removes currency symbols, commas, and other characters to convert to float.
    '''
    if pd.isna(item):
        return None
    cleaned = re.sub(r'[^\d.]', '', str(item))
    try:
        return float(cleaned)
    except ValueError:
        return None

def extract_year_mdy(timestamp):
    '''
    Parse the date and extract the year (assuming mm/dd/yyyy hh:mm:ss format).
    '''
    try:
        return datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S").year
    except:
        return None

def clean_country_usa(item: str) -> str:
    '''
    Standardizes U.S. country names into 'United States'
    '''
    if not isinstance(item, str):
        return item
    item = item.strip().lower()
    possibilities = [
        'united states of america', 'usa', 'us', 'u.s.', 'united states'
    ]
    if item in possibilities:
        return 'United States'
    return item.title()

if __name__ == '__main__':
    print("""
    Module for data cleaning functions.
    """)
