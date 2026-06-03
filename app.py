
import streamlit as st
import pandas as pd
import joblib

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Insurance Cost Predictor",
    page_icon="🏥",
    layout="centered"
)

# ----------------------------
# Load Model and Scaler
# ----------------------------
model = joblib.load("insurance_model.pkl")
scaler = joblib.load("scaler.pkl")

# ----------------------------
# Title
# ----------------------------
st.title("🏥 Insurance Cost Predictor")
st.markdown(
    """
    Predict your estimated medical insurance charges using Machine Learning.
    """
)

st.divider()

# ----------------------------
# User Inputs
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=25
    )

    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=60.0,
        value=25.0
    )

with col2:
    children = st.number_input(
        "Children",
        min_value=0,
        max_value=10,
        value=0
    )

    sex = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

smoker = st.selectbox(
    "Smoker",
    ["No", "Yes"]
)

region = st.selectbox(
    "Region",
    ["northeast", "northwest", "southeast", "southwest"]
)

st.divider()

# ----------------------------
# Prediction
# ----------------------------
if st.button("Predict Insurance Cost"):

    is_female = 1 if sex == "Female" else 0
    is_smoker = 1 if smoker == "Yes" else 0

    region_southeast = 1 if region == "southeast" else 0

    bmi_category_obese = 1 if bmi >= 30 else 0

    scaled_values = scaler.transform(
        [[age, bmi, children]]
    )

    age_scaled = scaled_values[0][0]
    bmi_scaled = scaled_values[0][1]
    children_scaled = scaled_values[0][2]

    input_df = pd.DataFrame(
        [[
            age_scaled,
            is_female,
            bmi_scaled,
            children_scaled,
            is_smoker,
            region_southeast,
            bmi_category_obese
        ]],
        columns=[
            'age',
            'is_female',
            'bmi',
            'children',
            'is_smoker',
            'region_southeast',
            'bmi_category_obese'
        ]
    )

    prediction = model.predict(input_df)

    st.success("Prediction Generated Successfully!")

    st.metric(
        label="Estimated Insurance Cost",
        value=f"₹{prediction[0]:,.2f}"
    )

st.divider()

st.caption(
    "Built with Python, Scikit-Learn and Streamlit"
)
