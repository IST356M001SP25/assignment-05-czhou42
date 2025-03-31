import pandas as pd
import streamlit as st
import pandaslib as pl

CACHE_DIR = "cache"

if __name__ == '__main__':
    # 1. Load data
    states_data = pd.read_csv(f"{CACHE_DIR}/states.csv")
    survey_data = pd.read_csv(f"{CACHE_DIR}/survey.csv")

    years = survey_data['year'].dropna().unique()
    col_frames = []
    for year in years:
        path = f"{CACHE_DIR}/col_{int(year)}.csv"
        if os.path.exists(path):
            col = pd.read_csv(path)
            col_frames.append(col)
    col_data = pd.concat(col_frames, ignore_index=True)

    # 2. Merge data
    survey_data['_country'] = survey_data["Which country do you work in?"].apply(pl.clean_country_usa)
    states_data.columns = ['state', 'code']
    survey_states_combined = pd.merge(
        survey_data,
        states_data,
        left_on="If you're in the U.S., what state do you work in?",
        right_on="state",
        how="inner"
    )

    survey_states_combined['_full_city'] = survey_states_combined["If you're in the U.S., what city do you work in?"].fillna('') + \
                                           ", " + survey_states_combined['code'] + ", " + survey_states_combined['_country']

    combined = pd.merge(
        survey_states_combined,
        col_data,
        left_on=['year', '_full_city'],
        right_on=['year', 'City'],
        how='inner'
    )

    # 3. Normalize salary
    combined['__annual_salary_cleaned'] = combined['What is your annual salary?'].apply(pl.clean_currency)
    combined['_annual_salary_adjusted'] = (combined['__annual_salary_cleaned'] / combined['COL Index']) * 100

    # 4. Save dataset and reports
    combined.to_csv(f"{CACHE_DIR}/survey_dataset.csv", index=False)

    # Report by age
    report_age = combined.pivot_table(
        index="_full_city",
        columns="How old are you?",
        values="_annual_salary_adjusted",
        aggfunc="mean"
    )
    report_age.to_csv(f"{CACHE_DIR}/annual_salary_adjusted_by_location_and_age.csv")

    # Report by education
    report_edu = combined.pivot_table(
        index="_full_city",
        columns="What is your highest level of education?",
        values="_annual_salary_adjusted",
        aggfunc="mean"
    )
    report_edu.to_csv(f"{CACHE_DIR}/annual_salary_adjusted_by_location_and_education.csv")
