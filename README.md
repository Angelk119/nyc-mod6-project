# ♻️ NYC Waste Management Analytics: Recycling Performance Prediction
--------

## Project Overview

This project develops a predictive analytics solution to help the NYC Department of Sanitation (DSNY) identify community districts at risk of falling below the 20% recycling target. By analyzing historical waste collection patterns, the system forecasts which districts are likely to achieve high recycling performance (>20% recycling ratio) a month in advance.

-------
## Primary Business Objectives
1. Predictive Monitoring: Forecast recycling performance at the community district level

2. Resource Optimization: Enable DSNY to proactively allocate education and outreach resources

3. Target Achievement: Support NYC's goal of increasing recycling rates across all boroughs

4. Anomaly Detection: Identify districts with unusually high refuse generation
-----------
## Dataset Information
### Primary Dataset: DSNY Monthly Tonnage Data
Source: NYC Open Data - [DSNY Monthly Tonnage](https://data.cityofnewyork.us/City-Government/DSNY-Monthly-Tonnage-Data/ebb7-mvp5/about_data)
- Coverage: Monthly waste collection data by community district (2022-2025)
- Records: ~2,700 monthly district-level observations
### Secondary Dataset: Population Data
- Source: NYC Open Data - [Population by Community District](https://data.cityofnewyork.us/City-Government/New-York-City-Population-By-Community-Districts/xi7c-iiu2/about_data)
- Coverage: 2010 Census data mapped to community districts

**Data dictionary**
| Column                | Description                                                   | Type              |
|-----------------------|---------------------------------------------------------------|-------------------|
| month                 | Reporting month (YYYY-MM)                                     | Period            |
| borough               | NYC borough                                                   | Categorical       |
| communitydistrict     | Community district number (1–18)                              | Integer           |
| refusetonscollected   | Total refuse (non-recyclable) tons                            | Continuous        |
| papertonscollected    | Paper recyclables collected (tons)                            | Continuous        |
| mgptonscollected      | Metal/Glass/Plastic recyclables (tons)                        | Continuous        |
| resorganicstons       | Residential organics (tons)                                   | Continuous        |
| schoolorganictons     | School organics (tons)                                        | Continuous        |
| otherorganicstons     | Other organics (tons)                                         | Continuous        |
| xmastreetons          | Christmas tree collection (tons)                              | Continuous        |
| population_2010       | 2010 Census population                                        | Integer           |
| recycling_ratio       | (Paper + MGP) / (Paper + MGP + Refuse)                        | Continuous [0–1]  |
| high_recycling        | Binary flag: recycling_ratio > 0.2                            | Binary            |
---------
### Environment Setup & Reproduction
1. Environment setup
```bash
# Clone the repo
git clone [https://github.com/yourusername/project.git](https://github.com/yourusername/project.git)
cd project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
2. Data Download
- Download the CSVs from [NYC open data link1](https://data.cityofnewyork.us/City-Government/DSNY-Monthly-Tonnage-Data/ebb7-mvp5/about_data) AND [NYC open data link2](https://data.cityofnewyork.us/City-Government/New-York-City-Population-By-Community-Districts/xi7c-iiu2/about_data)

- Save them to the datasets/ folder (ensure to change the paths accordingly in the notebooks).
- Run eda_clean.ipynb to clean the data and generate data needed for the modeling process.
- Run clean_models_notebook to train and evaluate models, saving files .pkl and config.json
- Run the app: streamlit run app/app.py

**IMPORTANT:** Ensure to check files paths in the loading process.


