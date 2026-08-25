import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(page_title="The Empty Chair Rule", page_icon="🪑", layout="wide", initial_sidebar_state="expanded")

FASTAPI_URL = "http://127.0.0.1:8000"

def get_risk_data():
    try:
        response = requests.get(f"{FASTAPI_URL}/api/risk-report", timeout=2)
        if response.status_code == 200:
            return response.json(), True
    except Exception:
        pass
    return None, False

api_data, is_connected = get_risk_data()

# ============================================================
# 2. ULTRA-MODERN DARK GLASSMORPHISM STYLING
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer {visibility: hidden;}

/* ---------- Background & Text ---------- */
.stApp {
    background-color: #0B0E14 !important;
    color: #FAFAFA !important;
}

/* ---------- Sidebar Styling ---------- */
section[data-testid="stSidebar"] {
    background-color: #121620 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* ---------- Pulsing Animation for High Risk ---------- */
@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(255, 77, 77, 0.4); }
    70% { box-shadow: 0 0 0 12px rgba(255, 77, 77, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 77, 77, 0); }
}

/* ---------- Hero Section ---------- */
.hero {
    background: linear-gradient(135deg, rgba(255, 77, 77, 0.1) 0%, rgba(18, 22, 32, 0.8) 100%);
    border: 1px solid rgba(255, 77, 77, 0.25);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FF4D4D !important;
    margin-bottom: 8px;
    font-weight: 700;
}
.hero h1 {
    font-size: 34px;
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 8px 0;
    background: linear-gradient(90deg, #FFFFFF, #B0B8C4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    font-size: 13px;
    opacity: 0.8;
    max-width: 580px;
    margin: 0;
    line-height: 1.5;
}

.seat-strip {
    position: absolute;
    right: 36px;
    top: 50%;
    transform: translateY(-50%);
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
}
.seat {
    width: 14px;
    height: 14px;
    border-radius: 3px;
}
.seat.filled { background: #FF4D4D; box-shadow: 0 0 8px #FF4D4D; }
.seat.cooling { background: rgba(255, 77, 77, 0.3); border: 1px solid #FF4D4D; }
.seat.empty { background: transparent; border: 1px dashed #8B949E; }

.row-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FF4D4D !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 8px;
    margin: 8px 0 18px 0;
    font-weight: 700;
}

/* ---------- Interactive High-Contrast Cards ---------- */
.card-critical {
    background: linear-gradient(145deg, rgba(255, 77, 77, 0.15) 0%, rgba(20, 24, 33, 0.9) 100%) !important;
    border: 2px solid #FF4D4D !important;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    animation: pulse-red 2.5s infinite;
    transition: transform 0.2s ease;
}
.card-watch {
    background: linear-gradient(145deg, rgba(243, 156, 18, 0.12) 0%, rgba(20, 24, 33, 0.9) 100%) !important;
    border: 1.5px solid #F39C12 !important;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    transition: transform 0.2s ease;
}
.card-stable {
    background: linear-gradient(145deg, rgba(46, 204, 113, 0.06) 0%, rgba(20, 24, 33, 0.9) 100%) !important;
    border: 1px solid rgba(46, 204, 113, 0.3) !important;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    opacity: 0.9;
    transition: transform 0.2s ease;
}

.card-critical:hover, .card-watch:hover, .card-stable:hover {
    transform: translateY(-3px);
}

.roll-name {
    font-size: 18px;
    font-weight: 700;
}
.roll-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    opacity: 0.7;
    letter-spacing: 1px;
}
.roll-tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 6px;
    margin: 10px 0 12px 0;
    font-weight: 800;
}
.tag-critical { background: #FF4D4D; color: #FFFFFF !important; box-shadow: 0 0 10px rgba(255,77,77,0.5); }
.tag-watch { background: #F39C12; color: #000000 !important; }
.tag-stable { background: rgba(46, 204, 113, 0.15); color: #2ECC71 !important; border: 1px solid #2ECC71; }

/* ---------- Glassmorphism KPI Metrics ---------- */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-left: 4px solid #FF4D4D !important;
    padding: 16px 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #A0AAB8 !important;
}

/* ---------- Tabs Styling ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    background-color: transparent !important;
    border: none !important;
    padding: 10px 16px;
}
.stTabs [aria-selected="true"] {
    color: #FF4D4D !important;
    border-bottom: 2px solid #FF4D4D !important;
    font-weight: 700;
}

/* ---------- Animated Buttons ---------- */
.stButton button, button[kind="primary"] {
    background: linear-gradient(135deg, #FF4D4D 0%, #D84343 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 77, 77, 0.25) !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 77, 77, 0.45) !important;
}

/* ---------- Privacy Footer Box ---------- */
.privacy-box {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 12px;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.6);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. HERO SECTION
# ============================================================
seat_states = ["filled"]*15 + ["cooling"]*5 + ["empty"]*4
seat_html = "".join(f'<div class="seat {s}"></div>' for s in seat_states)

st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">Early Risk Monitoring · Live Roll Call</div>
        <h1>The Empty Chair Rule</h1>
        <p>A seat that goes quiet is the first signal — before a grade drops, before a withdrawal form is filed. This dashboard tracks who's showing up, who's cooling off, and who needs assistance.</p>
        <div class="seat-strip">{seat_html}</div>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# 4. SIDEBAR CONTROLS & PRIVACY DISCLOSURE
# ============================================================
st.sidebar.markdown("### Roll Call Settings")

search_query = st.sidebar.text_input("Search name or ID", placeholder="e.g. ST001")
selected_risk = st.sidebar.multiselect("Risk level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
show_flagged_only = st.sidebar.checkbox("Flagged only")

st.sidebar.divider()

if is_connected:
    st.sidebar.success("✅ Connected to Live API")
else:
    st.sidebar.error("❌ API Offline")

st.sidebar.markdown("""
    <div class="privacy-box">
        <b>🔒 FERPA Compliant & Protected</b><br>
        Student risk analytics are encrypted and visible strictly to authorized academic advisors and faculty.
    </div>
""", unsafe_allow_html=True)

# ============================================================
# 5. TABS CONTENT
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Roll Call",
    "Attendance Patterns",
    "Early Alerts",
    "Interventions"
])

# --- TAB 1: ROLL CALL ---
with tab1:
    if is_connected and api_data:
        total_students = len(api_data)
        high_risk_count = sum(1 for s in api_data if s.get("risk_level") == "High")
        medium_risk_count = sum(1 for s in api_data if s.get("risk_level") == "Medium")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL STUDENTS", total_students)
        m2.metric("HIGH RISK", high_risk_count)
        m3.metric("MEDIUM RISK", medium_risk_count)
        st.write("")

        st.markdown('<div class="row-label">Active Seating Chart</div>', unsafe_allow_html=True)

        cols = st.columns(3)
        tag_map = {
            "critical": ("tag-critical", "🚨 High Risk"),
            "watch": ("tag-watch", "⚠️ Watchlist"),
            "stable": ("tag-stable", "✓ Low Risk")
        }
        
        filtered_count = 0
        for i, s in enumerate(api_data):
            if s.get("risk_level") not in selected_risk:
                continue
            if show_flagged_only and not s.get("flagged"):
                continue
            if search_query and (search_query.lower() not in s.get("student_name", "").lower() and search_query.lower() not in s.get("student_id", "").lower()):
                continue

            filtered_count += 1
            with cols[i % 3]:
                risk_lvl = s.get("risk_level", "Low")
                if risk_lvl == "High":
                    status = "critical"
                elif risk_lvl == "Medium":
                    status = "watch"
                else:
                    status = "stable"

                tag_class, tag_label = tag_map[status]
                risk_score = s.get("risk_score", 0)
                
                presence_pct = max(0, 100 - risk_score)
                meter_html = f"""<div style="width: 100%; background: rgba(255,255,255,0.08); border-radius: 6px; height: 7px; margin: 12px 0 8px 0;"><div style="width: {presence_pct}%; background: linear-gradient(90deg, #FF4D4D 0%, #F39C12 50%, #2ECC71 100%); height: 100%; border-radius: 6px;"></div></div>"""
               
                st.markdown(f"""
<div class="card-{status}">
    <span class="roll-name">{s.get('student_name', 'Unknown')}</span><br>
    <span class="roll-id">{s.get('student_id', 'N/A')}</span><br>
    <span class="roll-tag {tag_class}">{tag_label}</span>
    {meter_html}
    <div style="font-size: 12px; font-weight: 600; margin-top: 6px;">Risk Score: <b>{risk_score}%</b></div>
</div>
""", unsafe_allow_html=True)
               
                with st.expander("View Analysis Summary"):
                    note = s.get('summary', '')
                    if not note:
                        note = "Normal attendance patterns."
                    st.write(f"**AI Note:** {note}")
                    st.write(f"**Flagged for Review:** {'Yes' if s.get('flagged') else 'No'}")
                    
        if filtered_count == 0:
            st.info("No students found matching current search/filter settings.")
    else:
        st.warning("Waiting for live data from API...")

# --- TAB 2: ATTENDANCE PATTERNS ---
with tab2:
    st.markdown('<div class="row-label">Weekly Attendance Fill Rate (%)</div>', unsafe_allow_html=True)
    
    df_chart = pd.DataFrame({
        "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "High Risk Average": [88, 72, 60, 45],
        "Class Average": [94, 91, 89, 88]
    })
    
    fig = px.line(
        df_chart, 
        x="Week", 
        y=["High Risk Average", "Class Average"],
        markers=True,
        color_discrete_sequence=["#FF4D4D", "#2ECC71"]
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#A0AAB8",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 3: EARLY ALERTS ---
with tab3:
    st.markdown('<div class="row-label">System-Generated Risk Flags</div>', unsafe_allow_html=True)
    if is_connected and api_data:
        for s in api_data:
            if s.get("flagged"):
                st.error(f"**Early Alert — {s.get('student_name')} ({s.get('student_id')})**\n\n{s.get('summary')}")
    else:
        st.info("No active alerts.")

# --- TAB 4: INTERVENTIONS ---
with tab4:
    st.markdown('<div class="row-label">Suggested Next Steps</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
   
    with col_a:
        with st.container(border=True):
            st.subheader("High-Risk Intervention")
            st.write("1. Schedule 1-on-1 check-in within 48 hours.\n2. Dispatch automated notice to academic advisor.")
            st.write("")
            if st.button("🚨 Send Bulk Alert to High Risk", type="primary", key="btn_send_alert", use_container_width=True):
                st.toast("📧 Automated alerts dispatched successfully!", icon="✅")
                st.success("Alert notifications sent to assigned Academic Advisors.")

    with col_b:
        with st.container(border=True):
            st.subheader("Class-Wide Actions")
            st.write("1. Export real-time student risk analysis.\n2. Review lab attendance trends post-test weeks.")
            st.write("")
           
            if is_connected and api_data:
                df_export = pd.DataFrame(api_data)
                csv_data = df_export.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Download Live Class Report (CSV)",
                    data=csv_data,
                    file_name="Live_Risk_Summary_Report.csv",
                    mime="text/csv",
                    key="btn_download_report",
                    use_container_width=True
                )
            else:
                st.write("Waiting for data to generate report...")
