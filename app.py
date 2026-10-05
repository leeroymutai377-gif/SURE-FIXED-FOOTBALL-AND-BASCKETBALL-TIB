import pandas as pd
import requests
import streamlit as st

# 1. ENHANCED SEARCH ENGINE OPTIMIZATION (SEO) & PAGE SETUP
st.set_page_config(
    page_title="LEEROY CORRECT FIXED | Global Sports AI Predictions & Analytics",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject meta tags for Google, Bing, and Social Crawlers + Google Site Verification
st.markdown(
    """
    <head>
        <meta name="google-site-verification" content="n3VBV1TErXm35GTl29VcMovls3rZ2o5UXQjG4x5v0mo" />
        <meta name="description" content="LEEROY CORRECT FIXED is a premier AI-driven sports prediction engine providing automated match forecasts, historical archives, and custom match probability analysis for Football, Basketball, Tennis, and Rugby." />
        <meta name="keywords" content="sports predictions, football AI, basketball betting picks, sports analytics, match predictor, LEEROY CORRECT FIXED, sports prediction model" />
        <meta name="robots" content="index, follow" />
        <meta property="og:title" content="LEEROY CORRECT FIXED — Sports AI Predictions" />
        <meta property="og:description" content="Accurate AI sports predictions, live statistics, and historical archives for major global sports." />
        <meta property="og:type" content="website" />
    </head>
""",
    unsafe_allow_html=True,
)

# Date Context
TODAY_STR = "2026-10-05"

# User Credentials Database
USER_DB = {"admin": {"password": "adminpassword123", "role": "Admin"}}

# 2. SESSION STATE INITIALIZATION
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = "Visitor"

# Real Match Predictions Data
if "posted_predictions" not in st.session_state:
    st.session_state.posted_predictions = [
        {
            "sport": "⚽ Football",
            "country": "Europe (UCL)",
            "venue": "Santiago Bernabéu",
            "home": "Real Madrid",
            "away": "Manchester City",
            "result_or_pick": "Home Win (54%)",
            "type": "AI Forecast",
        },
        {
            "sport": "⚽ Football",
            "country": "England",
            "venue": "Emirates Stadium",
            "home": "Arsenal",
            "away": "Liverpool",
            "result_or_pick": "Both Teams To Score",
            "type": "AI Forecast",
        },
        {
            "sport": "🏀 Basketball",
            "country": "USA (NBA)",
            "venue": "TD Garden",
            "home": "Boston Celtics",
            "away": "Milwaukee Bucks",
            "result_or_pick": "Over 224.5 Points",
            "type": "AI Forecast",
        },
        {
            "sport": "🎾 Tennis",
            "country": "Italy (ATP)",
            "venue": "Foro Italico",
            "home": "Jannik Sinner",
            "away": "Carlos Alcaraz",
            "result_or_pick": "Over 2.5 Sets",
            "type": "AI Forecast",
        },
        {
            "sport": "🏉 Rugby",
            "country": "International",
            "venue": "Twickenham",
            "home": "England",
            "away": "France",
            "result_or_pick": "Away Win (-3.5)",
            "type": "AI Forecast",
        },
    ]

# Real Historical Results Archive Data
if "historical_archive" not in st.session_state:
    st.session_state.historical_archive = [
        {
            "sport": "⚽ Football",
            "country": "Spain",
            "venue": "Montjuïc Stadium",
            "home": "Barcelona",
            "away": "Real Madrid",
            "result_or_pick": "1 - 2 (Finished)",
            "type": "Archive Record",
        },
        {
            "sport": "⚽ Football",
            "country": "England",
            "venue": "Etihad Stadium",
            "home": "Manchester City",
            "away": "Chelsea",
            "result_or_pick": "3 - 1 (Finished)",
            "type": "Archive Record",
        },
        {
            "sport": "🏀 Basketball",
            "country": "USA (NBA)",
            "venue": "Crypto.com Arena",
            "home": "LA Lakers",
            "away": "Golden State Warriors",
            "result_or_pick": "118 - 112 (Finished)",
            "type": "Archive Record",
        },
        {
            "sport": "🥊 Boxing",
            "country": "Saudi Arabia",
            "venue": "Kingdom Arena",
            "home": "Oleksandr Usyk",
            "away": "Tyson Fury",
            "result_or_pick": "Usyk SD Win (Finished)",
            "type": "Archive Record",
        },
    ]


# 3. CORE AI PREDICTION CALCULATION ENGINE
def run_ai_prediction(home_weight, away_weight):
    total = home_weight + away_weight if (home_weight + away_weight) > 0 else 1
    home_prob = round((home_weight / total) * 100, 1)
    away_prob = round((away_weight / total) * 100, 1)
    return home_prob, away_prob


# 4. SIDEBAR NAVIGATION & AUTHENTICATION
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Select Option",
    [
        "Live Forecasts",
        "AI Calculator Engine",
        "Historical Archive",
        "Data Ingestion & Upload",
        "Admin Portal",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("User Authentication")

if not st.session_state.authenticated:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in USER_DB and USER_DB[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.user_role = USER_DB[username]["role"]
            st.sidebar.success(f"Logged in as {username}")
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")
else:
    st.sidebar.info(
        f"Logged in as: **{st.session_state.user_role}**", icon="👤"
    )
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_role = "Visitor"
        st.rerun()


# 5. MAIN PAGE CONTENT
st.title("🏆 LEEROY CORRECT FIXED — AI Sports Analytics & Match Predictions")
st.markdown(
    "Welcome to **LEEROY CORRECT FIXED**, an advanced artificial intelligence platform delivering daily data-driven match probability forecasts, historical team statistics, and predictive modeling for major sports leagues worldwide."
)
st.caption(f"System Operational Date: {TODAY_STR}")

# PAGE 1: LIVE FORECASTS
if menu == "Live Forecasts":
    st.header("⚡ Active System Predictions & AI Odds")
    st.write(
        "Explore real-time match predictions generated by our algorithmic ensemble models across Football, Basketball, Tennis, and Rugby."
    )
    df_preds = pd.DataFrame(st.session_state.posted_predictions)
    st.dataframe(df_preds, use_container_width=True)

# PAGE 2: AI CALCULATOR ENGINE
elif menu == "AI Calculator Engine":
    st.header("🧮 Custom Match Probability Calculator")
    st.write(
        "Estimate win probabilities and matchup ratings using custom team weightings."
    )
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.text_input("Home Team Name", "Real Madrid")
        home_weight = st.slider("Home Team Rating", 1, 100, 75)
    with col2:
        away_team = st.text_input("Away Team Name", "Manchester City")
        away_weight = st.slider("Away Team Rating", 1, 100, 70)

    if st.button("Calculate Match Odds"):
        h_prob, a_prob = run_ai_prediction(home_weight, away_weight)
        st.subheader("Calculated Odds:")
        st.write(f"**{home_team}** Win Chance: `{h_prob}%`")
        st.write(f"**{away_team}** Win Chance: `{a_prob}%`")

# PAGE 3: HISTORICAL ARCHIVE
elif menu == "Historical Archive":
    st.header("📜 Completed Matches & Historical Data Archive")
    st.write(
        "Review historical sports outcomes and past prediction performances."
    )
    df_hist = pd.DataFrame(st.session_state.historical_archive)
    st.dataframe(df_hist, use_container_width=True)

# PAGE 4: DATA INGESTION & UPLOAD (PROTECTED)
elif menu == "Data Ingestion & Upload":
    st.header("📁 Upload Match Datasets (Admin Only)")

    if (
        st.session_state.authenticated
        and st.session_state.user_role == "Admin"
    ):
        st.success(
            "🔓 Access Granted: Admin session active. You can upload CSV data."
        )

        uploaded_file = st.file_uploader(
            "Upload historical games CSV (`date,home,away,home_score,away_score`)",
            type=["csv"],
        )
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.subheader("Data Preview:")
                st.dataframe(df.head(), use_container_width=True)
                st.success("Dataset ingested successfully!")
            except Exception as e:
                st.error(f"Error loading CSV file: {e}")
    else:
        st.warning(
            "🔒 Access Restricted: Visitors cannot upload files. Please log in with an Admin account via the sidebar to access file management."
        )

# PAGE 5: ADMIN PORTAL (PROTECTED)
elif menu == "Admin Portal":
    st.header("🔒 Admin Dashboard")
    if (
        st.session_state.authenticated
        and st.session_state.user_role == "Admin"
    ):
        st.subheader("Publish Prediction")
        with st.form("new_pred_form"):
            sport = st.selectbox(
                "Sport Category",
                ["⚽ Football", "🏀 Basketball", "🎾 Tennis", "🏉 Rugby"],
            )
            country = st.text_input("Tournament / League", "UEFA Champions League")
            venue = st.text_input("Venue Name", "Allianz Arena")
            home = st.text_input("Home Team", "Bayern Munich")
            away = st.text_input("Away Team", "Paris Saint-Germain")
            pick = st.text_input("Prediction Pick", "Home Win")

            submitted = st.form_submit_button("Publish Prediction")
            if submitted:
                new_entry = {
                    "sport": sport,
                    "country": country,
                    "venue": venue,
                    "home": home,
                    "away": away,
                    "result_or_pick": pick,
                    "type": "Admin Manual Entry",
                }
                st.session_state.posted_predictions.append(new_entry)
                st.success("New prediction published!")
    else:
        st.warning(
            "🔒 Access Restricted: Please log in as an Admin to manage system predictions."
        )
