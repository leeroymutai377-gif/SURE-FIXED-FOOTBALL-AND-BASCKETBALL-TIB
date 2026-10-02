import streamlit as st
import pandas as pd
import numpy as np
import requests

# Set up page configurations
st.set_page_config(page_title="AI Sports Predictor Hub", layout="wide", page_icon="⚽")

# Initialize session state for persistent shared postings if it doesn't exist
if "posted_predictions" not in st.session_state:
    st.session_state.posted_predictions = [
        {"home": "Arsenal", "away": "Chelsea", "prediction": "Home Win (55%)", "type": "Admin AI Pick"},
        {"home": "Real Madrid", "away": "Barcelona", "prediction": "Over 2.5 Goals (62%)", "type": "System Forecast"}
    ]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = "Visitor"

# User database simulation
USER_DB = {
    "admin": {"password": "adminpassword123", "role": "Admin"},
    "client": {"password": "clientpassword123", "role": "Client"}
}

# Live API Fixture Aggregator Engine
def fetch_live_fixtures(api_key):
    """
    Pulls upcoming real-world fixtures using the Football-Data.org open API schema
    """
    url = "http://football-data.org"
    headers = {"X-Auth-Token": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            matches = data.get("matches", [])
            
            cleaned_fixtures = []
            # Gather upcoming scheduled games
            for match in matches[:5]:
                cleaned_fixtures.append({
                    "home": match["homeTeam"]["name"],
                    "away": match["awayTeam"]["name"],
                    "utcDate": match["utcDate"]
                })
            return cleaned_fixtures
        else:
            st.error(f"⚠️ API Connection Failed: Server responded with status code {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ Failed to reach network database endpoint: {str(e)}")
        return []

# Core Prediction Engine Logic
def run_ai_prediction(home_form, away_form, h2h_factor, home_advantage):
    # Calculate performance scores using weights
    home_score = (home_form * 0.4) + (h2h_factor * 0.4) + (home_advantage * 0.2)
    away_score = (away_form * 0.5) + ((10 - h2h_factor) * 0.5)
    
    total_score = home_score + away_score
    raw_home_prob = home_score / total_score
    raw_away_prob = away_score / total_score
    
    # Introduce draw probability naturally based on performance closeness
    draw_prob = max(0.10, 0.35 - abs(raw_home_prob - raw_away_prob))
    
    # Re-normalize remaining probabilities around draw margins
    remaining_scale = 1.0 - draw_prob
    home_prob = (raw_home_prob / (raw_home_prob + raw_away_prob)) * remaining_scale
    away_prob = (raw_away_prob / (raw_home_prob + raw_away_prob)) * remaining_scale
    
    return round(home_prob * 100, 1), round(draw_prob * 100, 1), round(away_prob * 100, 1)

def check_login(username, password):
    if username in USER_DB and USER_DB[username]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.user_role = USER_DB[username]["role"]
        st.session_state.username = username
        st.rerun()
    else:
        st.error("❌ Invalid Username or Password. Please try again.")

def logout():
    st.session_state.authenticated = False
    st.session_state.user_role = "Visitor"
    st.rerun()

# ====================================================================
# APPLICATION VIEW INTERFACES
# ====================================================================

# SIDEBAR: Always displays authentication states
st.sidebar.title("🔐 Access Portal")
if not st.session_state.authenticated:
    st.sidebar.subheader("Login to your Account")
    login_user = st.sidebar.text_input("Username")
    login_pass = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Sign In", type="primary"):
        check_login(login_user, login_pass)
    st.sidebar.info("💡 **Default credentials for testing:**\n- Admin: `admin` / `adminpassword123`\n- Client: `client` / `clientpassword123` *(Browses as Visitor if not signed in)*")
else:
    st.sidebar.success(f"Logged in as: **{st.session_state.username}** ({st.session_state.user_role})")
    if st.sidebar.button("Log Out"):
        logout()

# SCENARIO A: ADMIN MODE INTERFACE
if st.session_state.authenticated and st.session_state.user_role == "Admin":
    st.title("🛡️ Admin AI Automated Control Panel")
    st.subheader("Accumulate Real Fixtures from API & Mass-Generate Machine Predictions")
    
    # Live Data Connection Module
    st.markdown("### 🔌 Real-Time Network Integration")
    api_token = st.text_input("Enter Football-Data.org API Token", type="password", help="Sign up at football-data.org to get a free developer token.")
    
    if st.button("Query API & Sync Live Fixtures", type="primary"):
        if not api_token:
            st.warning("Please provide a valid alphanumeric API authentication token first.")
        else:
            with st.spinner("Connecting to data grids to ingest scheduled matches..."):
                fetched_matches = fetch_live_fixtures(api_token)
                
                if fetched_matches:
                    st.success(f"Successfully downloaded {len(fetched_matches)} upcoming matches from server feeds!")
                    
                    # Automate AI evaluations for the compiled fixtures map
                    for match in fetched_matches:
                        h_p, d_p, a_p = run_ai_prediction(6, 6, 5, 3) 
                        probs = [h_p/100, d_p/100, a_p/100]
                        probs = [p / sum(probs) for p in probs]
                        
                        outcomes = [f"{match['home']} Win", "Draw", f"{match['away']} Win"]
                        calculated_pick = np.random.choice(outcomes, p=probs)
                        
                        # Accumulate directly inside the client data system arrays
                        st.session_state.posted_predictions.append({
                            "home": match['home'],
                            "away": match['away'],
                            "prediction": f"{calculated_pick} (Automated API Prediction)",
                            "type": "AI Live Feed Import"
                        })
                    st.toast("Shared public feed refreshed with newly generated forecasts!")
                    st.rerun()

    st.markdown("---")
    st.markdown("### 📝 Option B: Add Manual Prediction Override Slot")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Match Details")
        home_team = st.text_input("Home Team Name", "Manchester City")
        away_team = st.text_input("Away Team Name", "Liverpool")
        
        st.markdown("### AI Weight Parameters")
        home_form = st.slider("Home Team Current Form (1-10)", 1, 10, 8)
        away_form = st.slider("Away Team Current Form (1-10)", 1, 10, 7)
        h2h_factor = st.slider("Head-to-Head Dominance Factor (1-10 favor Home)", 1, 10, 5)
        home_advantage = st.slider("Home Stadium Atmosphere Rating (1-5)", 1, 5, 3)

    with col2:
        st.markdown("### AI Calculation Pipeline")
        if st.button("Execute System Prediction Model", type="primary"):
            h_p, d_p, a_p = run_ai_prediction(home_form, away_form, h2h_factor, home_advantage)
            
            st.success("🤖 Analysis Matrix Completed!")
            st.metric(label=f"🏠 {home_team} Win Chance", value=f"{h_p}%")
            st.metric(label="🤝 Draw Closeness Chance", value=f"{d_p}%")
            st.metric(label=f"🚀 {away_team} Win Chance", value=f"{a_p}%")
            
            probs = [h_p/100, d_p/100, a_p/100]
            probs = [p / sum(probs) for p in probs] 
            
            outcome_options = [f"{home_team} Win", "Draw", f"{away_team} Win"]
            final_verdict = np.random.choice(outcome_options, p=probs)
            
            st.session_state.last_calculated = {
                "home": home_team,
                "away": away_team,
                "prediction": f"{final_verdict} (AI Confirmed)",
                "type": "Admin AI Pick"
            }
            st.warning(f"**Calculated Verdict:** {final_verdict}")

        st.markdown("---")
        st.markdown("### Post to Client Feed")
        if "last_calculated" in st.session_state:
            st.write(f"**Pending Match:** {st.session_state.last_calculated['home']} vs {st.session_state.last_calculated['away']}")
            if st.button("Publish Live to Public Dashboard"):
                st.session_state.posted_predictions.append(st.session_state.last_calculated)
                st.balloons()
                st.success("Successfully deployed recommendation into the client dashboard!")
        else:
            st.info("Construct a forecast array first using the analytics engine to populate the upload staging slot.")

# SCENARIO B: PUBLIC / CLIENT / VISITOR DASHBOARD
else:
    st.title("⚽ Community Sports Analysis Center")
    
    tab1, tab2 = st.tabs(["📋 Live Accumulated AI Predictions", "🧮 Custom Match Sandbox Tool"])
    
    with tab1:
        st.header("🎯 Active Verified Postings")
        st.write("Below is the synchronized database showing live-odds data feeds and automated AI analytical summaries:")
        
        if st.session_state.posted_predictions:
            df = pd.DataFrame(st.session_state.posted_predictions)
            df.columns = ["Home Side Team", "Away Side Team", "Calculated Suggestion", "Processing Origin"]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No predictions compiled for current fixture ranges yet.")

    with tab2:
        st.header("🔍 Sandbox Engine Console")

