import streamlit as st
import pandas as pd
import time
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

# Import custom modules
from data_simulator import update_buffer
from utils import check_anomaly, calculate_risk, classify_contamination

# --- PAGE CONFIG ---
st.set_page_config(page_title="Trinity Codex – Water Intelligence System", layout="wide")

# --- DARK THEME ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
                    url("https://images.unsplash.com/photo-1518063319789-7217e6706b04?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["pH", "TDS", "Turbidity"])

# --- SIDEBAR ---
st.sidebar.title("🛡️ TRINITY CODEX")
menu = st.sidebar.radio("Navigation", [
    "Home & Monitor",
    "Geo-Tagged Map",
    "Analytics & AI Insights",
    "Eco-Bot & SOS"
])

# =========================================================
# 🧪 SECTION 1: REAL-TIME MONITORING
# =========================================================
if menu == "Home & Monitor":
    st.title("🚰 Real-Time Water Quality Network")

    # Update real-time buffer
    st.session_state.data = update_buffer(st.session_state.data)

    latest = st.session_state.data.iloc[-1]
    ph, tds, turb = latest["pH"], latest["TDS"], latest["Turbidity"]

    # --- ANOMALY CHECK ---
    anomalies = check_anomaly(ph, tds, turb)

    # --- METRICS ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("pH Level", ph,
                  delta="ANOMALY" if anomalies["ph"] else "Safe",
                  delta_color="inverse" if anomalies["ph"] else "normal")

    with col2:
        st.metric("TDS (mg/L)", tds,
                  delta="HIGH" if anomalies["tds"] else "Safe",
                  delta_color="inverse" if anomalies["tds"] else "normal")

    with col3:
        st.metric("Turbidity (NTU)", turb,
                  delta="SPIKE" if anomalies["turb"] else "Safe",
                  delta_color="inverse" if anomalies["turb"] else "normal")

    # --- RISK SCORE ---
    risk_score = calculate_risk(ph, tds, turb)
    st.metric("⚠️ Risk Score", round(risk_score, 2))

    # --- CLASSIFICATION ---
    cont_type, confidence = classify_contamination(ph, tds, turb)
    st.info(f"🧪 Contamination Type: {cont_type} ({int(confidence*100)}% confidence)")

    # --- LIVE CHART ---
    st.subheader("📊 Live Sensor Trends")

    fig = go.Figure()

    fig.add_trace(go.Scatter(y=st.session_state.data["pH"], name="pH"))
    fig.add_trace(go.Scatter(y=st.session_state.data["TDS"], name="TDS"))
    fig.add_trace(go.Scatter(y=st.session_state.data["Turbidity"], name="Turbidity"))

    st.plotly_chart(fig, use_container_width=True)

    # Auto refresh
    time.sleep(2)
    st.rerun()

# =========================================================
# 🌍 SECTION 2: GEO MAP
# =========================================================
elif menu == "Geo-Tagged Map":
    st.header("📍 Contamination Zone Mapping")

    m = folium.Map(location=[10.8505, 78.7047], zoom_start=13, tiles="CartoDB dark_matter")

    sensor_points = [
        {"lat": 10.85, "lon": 78.70, "risk": "high"},
        {"lat": 10.86, "lon": 78.71, "risk": "medium"},
        {"lat": 10.84, "lon": 78.69, "risk": "safe"},
    ]

    for s in sensor_points:
        color = "red" if s["risk"]=="high" else "orange" if s["risk"]=="medium" else "green"

        folium.CircleMarker(
            location=[s["lat"], s["lon"]],
            radius=10,
            color=color,
            fill=True,
            popup=f"Risk: {s['risk']}"
        ).add_to(m)

    folium.Circle(
        location=[10.8505, 78.7047],
        radius=600,
        color="red",
        fill=True,
        opacity=0.3
    ).add_to(m)

    st_folium(m, width=1000, height=500)
elif menu == "Analytics & AI Insights":
    st.header("📊 Data Analytics & AI Insights")

    if "data" not in st.session_state or st.session_state.data.empty:
        st.warning("No data available. Go to Home & Monitor first.")
    else:
        df = st.session_state.data.copy()

        # =========================
        # 📈 CORRELATION HEATMAP
        # =========================
        st.subheader("🔗 Correlation Heatmap")

        corr = df.corr()

        import plotly.express as px
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu")
        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # 📊 ANOMALY DETECTION
        # =========================
        st.subheader("⚠️ Anomaly Frequency")

        df["ph_anomaly"] = (df["pH"] < 6.5) | (df["pH"] > 8.5)
        df["tds_anomaly"] = df["TDS"] > 500
        df["turb_anomaly"] = df["Turbidity"] > 5

        anomaly_count = {
            "pH": df["ph_anomaly"].sum(),
            "TDS": df["tds_anomaly"].sum(),
            "Turbidity": df["turb_anomaly"].sum()
        }

        st.bar_chart(anomaly_count)

        # =========================
        # 🧪 CONTAMINANT DISTRIBUTION
        # =========================
        st.subheader("🧪 Contaminant Distribution")

        def classify(row):
            if row["TDS"] > 500:
                return "Chemical"
            elif row["Turbidity"] > 5:
                return "Physical"
            else:
                return "Safe"

        df["Type"] = df.apply(classify, axis=1)

        dist = df["Type"].value_counts()
        st.bar_chart(dist)

        # =========================
        # 🧠 AI INSIGHT ENGINE
        # =========================
        st.subheader("🧠 AI Insight Summary")

        insights = []

        # Trend detection
        if len(df) > 10:
            if df["TDS"].iloc[-1] > df["TDS"].iloc[0]:
                insights.append("📈 TDS levels are showing an increasing trend.")

            if df["Turbidity"].mean() > 4:
                insights.append("🌫️ Turbidity levels are consistently high.")

            if df["pH"].mean() > 8:
                insights.append("⚗️ Water is tending towards alkaline conditions.")

        # Risk pattern
        high_risk = ((df["TDS"] > 500) | (df["Turbidity"] > 5)).sum()

        if high_risk > len(df) * 0.3:
            insights.append("🚨 High frequency of contamination detected.")

        # Final output
        if insights:
            for i in insights:
                st.info(i)
        else:
            st.success("✅ System stable. No major risk patterns detected.")

# =========================================================
# 🤖 SECTION 3: ECO BOT + SOS
# =========================================================
elif menu == "Eco-Bot & SOS":
    st.header("🤖 Eco-Redemption Bot & Emergency System")

    tab1, tab2 = st.tabs(["Eco Bot", "SOS System"])

    # --- ECO BOT ---
    with tab1:
        st.subheader("🌱 Sustainable Solutions")

        contaminant = st.selectbox("Select Contamination Type", ["Chemical", "Biological", "Physical"])

        if st.button("Get Solution"):
            if contaminant == "Chemical":
                st.success("Use biofilters with Prosopis juliflora to absorb heavy metals.")
            elif contaminant == "Biological":
                st.success("Apply UV or chlorination treatment.")
            else:
                st.success("Use sedimentation and filtration techniques.")

    # --- SOS SYSTEM ---
    with tab2:
        st.subheader("🚨 Emergency SOS")

        phone = st.text_input("Register Phone Number")

        if st.button("Register"):
            st.toast(f"{phone} registered for alerts")

        st.divider()

        if st.button("🚨 AUTO SOS CHECK"):
            # Use latest data for real logic
            if "data" in st.session_state and not st.session_state.data.empty:
                latest = st.session_state.data.iloc[-1]
                ph, tds = latest["pH"], latest["TDS"]

                if ph > 9 or tds > 1000:
                    with st.status("Triggering SOS..."):
                        time.sleep(1)
                        st.write("Identifying affected residents...")
                        time.sleep(1)
                        st.write("Sending alerts...")
                    st.error("🚨 ALERT SENT to 1,245 residents")
                else:
                    st.success("System stable — no alert needed")
            else:
                st.warning("No data available yet. Visit Home & Monitor first.")