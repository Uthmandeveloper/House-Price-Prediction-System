# ------------------------------------------------
# 🏡 OFFA HOUSE PRICE PREDICTOR — DASHBOARD STYLE
# ------------------------------------------------
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.graph_objects as go

# ------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------
st.set_page_config(
    page_title="🏠 Offa House Price Prediction Dashboard",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------
# THEME STYLING (LIGHT + PROFESSIONAL)
# ------------------------------------------
st.markdown("""
    <style>
        body {
            background-color: #f4f6f9;
        }
        .stApp {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 1.5rem 2rem;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #004d99;
            font-weight: 700;
        }
        .main-header {
            text-align: center;
            font-size: 2rem !important;
            color: #004d99;
            margin-bottom: 0.5rem;
        }
        hr {
            border: 1px solid #0073e6;
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background-color: #0073e6;
            color: white;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6em 1.2em;
            border: none;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #005bb5;
        }
        .prediction-box {
            background-color: #e8f2ff;
            border-left: 5px solid #0073e6;
            border-radius: 10px;
            padding: 1.2rem;
            color: #003366;
        }
        .footer-text {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------
# PAGE HEADER
# ------------------------------------------
st.markdown("<h1 class='main-header'>🏠 OFFA HOUSE PRICE PREDICTION DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ------------------------------------------
# LOAD MODEL
# ------------------------------------------
@st.cache_data
def load_model():
    return joblib.load("random_forest_model.pkl")

model = load_model()

# ------------------------------------------
# LAYOUT: TWO MAIN COLUMNS
# ------------------------------------------
col1, col2 = st.columns([1.1, 1.1], gap="large")

# ------------------------------------------
# LEFT COLUMN: INPUT FORM
# ------------------------------------------
with col1:
    st.subheader("📋 Enter Property Details")

    areas = ["Sabo", "Ojomu", "Ijagbo", "Igbonna", "Offa Central",
             "Olofa", "Olalomi", "Owode", "Oyun", "Balogun"]

    area_name = st.selectbox("📍 Select Area", areas)
    no_of_bedrooms = st.number_input("🛏 Number of Bedrooms", min_value=1, max_value=10, value=3)
    no_of_bathrooms = st.number_input("🚿 Number of Bathrooms", min_value=1, max_value=6, value=2)
    land_area_sqm = st.number_input("📐 Land Area (sqm)", min_value=200, max_value=1200, step=50, value=500)
    fenced = st.selectbox("🏗️ Fenced?", ["Yes", "No"])
    building_type = st.selectbox("🏠 Building Type", ["Bungalow", "Flat", "Duplex", "Self-Contain"])
    interior_type = st.selectbox("🎨 Interior Type", ["POP", "Ceiling"])
    roof_type = st.selectbox("🏚️ Roof Type", ["Gerrard", "Normal"])
    distance_to_main_road_km = st.slider("🛣️ Distance to Main Road (km)", 0.1, 10.0, 1.0)
    road_type = st.selectbox("🚗 Road Type", ["Tarred", "Untarred"])
    area_type = st.selectbox("🌆 Area Type", ["Urban", "Rural"])
    electricity_reliability_hrs = st.slider("⚡ Electricity Availability (hrs/day)", 1, 24, 12)
    water_supply = st.selectbox("🚰 Water Supply", ["Well Water", "Borehole"])

    predict_btn = st.button("💡 Predict House Price")

# ------------------------------------------
# RIGHT COLUMN: RESULT + VISUALIZATION
# ------------------------------------------
with col2:
    if predict_btn:
        # Prepare input data
        input_dict = {
            "area_name": area_name,
            "no_of_bedrooms": no_of_bedrooms,
            "no_of_bathrooms": no_of_bathrooms,
            "land_area_sqm": land_area_sqm,
            "fenced": fenced,
            "building_type": building_type,
            "interior_type": interior_type,
            "roof_type": roof_type,
            "distance_to_main_road_km": distance_to_main_road_km,
            "road_type": road_type,
            "area_type": area_type,
            "electricity_reliability_hrs": electricity_reliability_hrs,
            "water_supply": water_supply
        }

        df_input = pd.DataFrame([input_dict])

        label_maps = {
            "area_name": {"Offa Central": 0, "Olofa": 1, "Ojomu": 2, "Sabo": 3, "Igbonna": 4,
                        "Ijagbo": 5, "Owode": 6, "Oyun": 7, "Olalomi": 8, "Balogun": 9},
            "fenced": {"No": 0, "Yes": 1},
            "building_type": {"Bungalow": 0, "Duplex": 1, "Flat": 2, "Self-Contain": 3},
            "interior_type": {"Ceiling": 0, "POP": 1},
            "roof_type": {"Normal": 0, "Gerrard": 1},
            "road_type": {"Untarred": 0, "Tarred": 1},
            "area_type": {"Rural": 0, "Urban": 1},
            "water_supply": {"Well Water": 0, "Borehole": 1}
        }

        for col, mapping in label_maps.items():
            df_input[col] = df_input[col].map(mapping)

        predicted_price = model.predict(df_input)[0]

        st.markdown(
            f"<div class='prediction-box'>"
            f"<h3>💰 Estimated Price: ₦{predicted_price:,.2f}</h3>"
            f"<p><b>📍 Location:</b> {area_name}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Price Trend Visualization
        st.markdown("### 📊 Price Trend by Bedrooms")
        trend_data = []
        for beds in range(1, 11):
            temp = df_input.copy()
            temp["no_of_bedrooms"] = beds
            price = model.predict(temp)[0]
            trend_data.append((beds, price))

        trend_df = pd.DataFrame(trend_data, columns=["Bedrooms", "Predicted Price (₦)"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_df["Bedrooms"],
            y=trend_df["Predicted Price (₦)"],
            mode="lines+markers",
            line=dict(color="#0073e6", width=3),
            marker=dict(size=8, color="#1e88e5")
        ))
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Number of Bedrooms",
            yaxis_title="Predicted Price (₦)",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            font=dict(color="#1a1a1a"),
            margin=dict(l=20, r=20, t=30, b=30)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Smart Summary
        if area_type == "Urban":
            st.info("🏙️ This estimate reflects urban pricing trends — typically higher due to accessibility and infrastructure.")
        else:
            st.info("🌾 This estimate reflects rural pricing — often more affordable with larger land spaces.")

# ------------------------------------------
# FOOTER
# ------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='footer-text'>Developed for HND Project — Offa LGA Housing Price System</div>", unsafe_allow_html=True)
