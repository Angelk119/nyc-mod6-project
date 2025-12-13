import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# Page config
st.set_page_config(
    page_title="NYC Recycling Performance Predictor",
    page_icon="♻️",
    layout="wide"
)

# Load model
@st.cache_resource
def load_model():
    model = joblib.load('/Users/Marcy_Student/Desktop/marcy/Modeling NYC-waste/NYC_waste_model/models_data/recycling_performance.pkl')
    return model

# Load historical data
@st.cache_data
def load_historical_data():
    df = pd.read_csv('/Users/Marcy_Student/Desktop/marcy/Modeling NYC-waste/NYC_waste_model/models_data/model_2_data.csv')
    return df

recycling_model = load_model()
recycling_df = load_historical_data()

# App header
st.title("♻️ NYC Recycling Performance Predictor")
st.markdown("predict whether a community district will achieve **high recyclable waste collection rate** (>20% recycling ratio) based on recent waste collection patterns.")

# Sidebar inputs
st.sidebar.header("District & Time Period")

borough = st.sidebar.selectbox(
    "Borough",
    ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]
)

communitydistrict = st.sidebar.number_input(
    "Community District",
    min_value=1,
    max_value=18,
    value=1,
    step=1
)

col_month, col_year = st.sidebar.columns(2)
with col_month:
    month_num = st.selectbox(
        "Month",
        options=list(range(1, 13)),
        format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
        index=5
    )
with col_year:
    year_num = st.number_input(
        "Year",
        min_value=2015,
        max_value=2030,
        value=2024,
        step=1
    )

month_str = f"{year_num}-{month_num:02d}"

st.sidebar.markdown("---")
st.sidebar.subheader("Recent Waste Collection (Tons)")

# Waste collection inputs
refuse_lag1 = st.sidebar.number_input(
    "Refuse (Previous Month)",
    min_value=0.0,
    value=5000.0,
    step=100.0,
    help="Refuse tons collected last month"
)

paper_lag1 = st.sidebar.number_input(
    "Paper (Previous Month)",
    min_value=0.0,
    value=800.0,
    step=50.0,
    help="Paper recyclables collected last month"
)

mgp_lag1 = st.sidebar.number_input(
    "MGP (Previous Month)",
    min_value=0.0,
    value=600.0,
    step=50.0,
    help="Metal/Glass/Plastic tons collected last month"
)

refuse_lag12 = st.sidebar.number_input(
    "Refuse (12 Months Ago)",
    min_value=0.0,
    value=5200.0,
    step=100.0,
    help="Refuse tons collected same month last year"
)

# Get population from historical data
district_data = recycling_df[
    (recycling_df['borough'].str.strip().str.title() == borough) & 
    (recycling_df['communitydistrict'] == communitydistrict)
]

if not district_data.empty and 'population_2010' in district_data.columns:
    population_2010 = district_data['population_2010'].iloc[0]
else:
    population_2010 = 50000

# Build input for recycling model
input_data = pd.DataFrame({
    'month': [month_str],
    'borough': [borough],
    'communitydistrict': [str(communitydistrict)],
    'refuse_lag1': [refuse_lag1],
    'paper_lag1': [paper_lag1],
    'mgp_lag1': [mgp_lag1],
    'refuse_lag12': [refuse_lag12],
    'population_2010': [population_2010]
})

# Main content area
st.subheader("🔮 Prediction Results")

# Predict
proba = recycling_model.predict_proba(input_data)[0, 1]
threshold = 0.60
prediction = int(proba >= threshold)

# Display results
if prediction == 1:
    st.success("✅ **High Recycling Performance Expected**")
    st.markdown(f"District **{borough} - CD {communitydistrict}** is predicted to achieve >20% recycling ratio in {month_str}.")
else:
    st.warning("⚠️ **Low Recycling Performance Expected**")
    st.markdown(f"District **{borough} - CD {communitydistrict}** may not reach the 20% recycling target in {month_str}.")

# Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Performance Probability", f"{proba:.1%}")
with col2:
    st.metric("Classification", "High Performance" if prediction == 1 else "Low Performance")

st.markdown("---")

# Model info
st.subheader("ℹ️ Model Information")
st.markdown("""
**Model Type:** Logistic Regression  
**Target:** High recycling performance (>20% recycling ratio)  
**Features:** Temporal patterns, waste type lags, population metrics  
**Performance:** Accuracy 93.2% | Recall 93.5%  
**Threshold:** 60.0%
""")

# Footer
st.markdown("---")
st.caption("NYC Waste Management Analytics | DSNY Monthly Tonnage Data | Model: Logistic Regression")