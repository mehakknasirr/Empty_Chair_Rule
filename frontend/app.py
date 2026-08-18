import streamlit as st
import pandas as pd
import requests

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(page_title="The Empty Chair Rule", page_icon="🪑", layout="wide", initial_sidebar_state="expanded")

FASTAPI_URL = "http://127.0.0.1:8000"

def get_backend_stats():
    try:
        response = requests.get(f"{FASTAPI_URL}/api/dashboard/stats", timeout=2)
        if response.status_code == 200:
            return response.json(), True
    except Exception:
        pass
    return None, False

api_stats, is_connected = get_backend_stats()

# ============================================================
# 2. LIGHT / DARK THEME COMPATIBLE CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer {visibility: hidden;}

/* ---------- Responsive Background & Text Defaults ---------- */
.stApp {
    background-color: var(--background-color, #0E1117) !important;
    color: var(--text-color, #FAFAFA) !important;
}

/* ---------- Sidebar Styling ---------- */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128, 128, 128, 0.2) !important;
}

span[data-baseweb="tag"] {
    background-color: #EE5959 !important;
    border: none !important;
    border-radius: 4px !important;
    color: #FFFFFF !important;
}

/* ---------- Hero Section ---------- */
.hero {
    background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(14, 17, 23, 0.8) 100%);
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-radius: 12px;
    padding: 32px 36px;
    margin-bottom: 24px;
    position: relative; 
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #EE5959 !important;
    margin-bottom: 8px;
    font-weight: 600;
}
.hero h1 {
    font-size: 32px;
    font-weight: 700;
    line-height: 1.1;
    margin: 0 0 8px 0;
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
    width: 12px;
    height: 12px;
    border-radius: 2px;
}
.seat.filled { background: #EE5959; }
.seat.cooling { background: rgba(238, 89, 89, 0.3); border: 1px solid #EE5959; }
.seat.empty { background: transparent; border: 1px dashed #8B949E; } 

.row-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #EE5959 !important;
    border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    padding-bottom: 8px;
    margin: 8px 0 18px 0;
}

/* ---------- Risk Cards (High Contrast Text) ---------- */
.card-critical {
    background-color: rgba(238, 89, 89, 0.15) !important;
    border: 1.5px solid #EE5959 !important;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
.card-stable {
    background-color: rgba(46, 160, 67, 0.15) !important;
    border: 1.5px solid #2EA043 !important;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
.card-watch {
    background-color: rgba(210, 153, 34, 0.15) !important;
    border: 1.5px solid #D29922 !important;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

.roll-name {
    font-size: 17px;
    font-weight: 700;
}
.roll-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    opacity: 0.75;
    letter-spacing: 1px;
}
.roll-tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px; 
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 4px;
    margin: 8px 0 10px 0;
    font-weight: 700;
}
.tag-critical { background: #EE5959; color: #FFFFFF !important; }
.tag-watch { background: #D29922; color: #000000 !important; }
.tag-stable { background: #2EA043; color: #FFFFFF !important; }

.seat-meter { display: flex; gap: 3px; margin: 10px 0 6px 0; }
.seat-meter div { height: 6px; flex: 1; border-radius: 2px; }

/* ---------- Metric Cards Styling ---------- */
div[data-testid="stMetric"] {
    background-color: rgba(128, 128, 128, 0.08) !important;
    border: 1px solid rgba(128, 128, 128, 0.2) !important;
    padding: 14px 18px;
    border-radius: 10px;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ---------- Tabs Styling ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 1px solid rgba(128, 128, 128, 0.2); }
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    background-color: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #EE5959 !important;
    border-bottom: 2px solid #EE5959 !important;
    font-weight: 600;
} 

/* ---------- Buttons & Action Containers ---------- */
.stButton button, button[kind="primary"] {
    background: #EE5959 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease;
}
.stButton button:hover {
    background: #D84343 !important;
    box-shadow: 0 4px 12px rgba(238, 89, 89, 0.3);
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
# 4. SIDEBAR CONTROLS
# ============================================================
st.sidebar.markdown("### Roll Call Settings")

search_query = st.sidebar.text_input("Search name or ID", placeholder="e.g. STU001")
selected_risk = st.sidebar.multiselect("Risk level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
show_flagged_only = st.sidebar.checkbox("Flagged only")

st.sidebar.divider()

if is_connected:
    st.sidebar.success("Connected to live backend")
else:
    st.sidebar.info("Preview mode — sample data")

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
    if is_connected and api_stats:
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL STUDENTS", api_stats.get("total_students", 0))
        m2.metric("HIGH RISK", api_stats.get("high_risk_count", 0))
        m3.metric("MEDIUM RISK", api_stats.get("medium_risk_count", 0))
        st.write("")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL STUDENTS", "2")
        m2.metric("HIGH RISK", "1")
        m3.metric("MEDIUM RISK", "0")
        st.write("")

    st.markdown('<div class="row-label">Active Seating Chart</div>', unsafe_allow_html=True)

    students = [
        {"name": "Ali Khan", "id": "STU001", "risk": 85, "delta": "+15% this week",
         "status": "critical", "color": "#EE5959", "dept": "BS Information Technology", "sem": "4th Semester",
         "attendance": "52% (Critical)", "note": "Missed 3 consecutive lab sessions."},
        {"name": "Ayesha Ahmed", "id": "STU002", "risk": 15, "delta": "-5% this week",
         "status": "stable", "color": "#2EA043", "dept": "BS Information Technology", "sem": "4th Semester",
         "attendance": "94% (Excellent)", "note": "Active participant in group repositories."},
        {"name": "Priya Raman", "id": "STU003", "risk": 45, "delta": "Stable",
         "status": "watch", "color": "#D29922", "dept": "BS Information Technology", "sem": "4th Semester",
         "attendance": "76% (Moderate)", "note": "Irregular attendance post-break."},
    ]

    cols = st.columns(3)
    tag_map = {
        "critical": ("tag-critical", "🚨 Needs Attention"), 
        "watch": ("tag-watch", "⚠️ Watching"), 
        "stable": ("tag-stable", "✓ Stable")
    }
    
    for col, s in zip(cols, students):
        with col:
            tag_class, tag_label = tag_map[s["status"]]
            
            # Custom Meter Blocks based on individual Risk Color
            presence = 100 - s["risk"]
            filled_blocks = round(presence / 10)
            blocks = "".join(f'<div style="background:{"#EE5959" if i >= filled_blocks else "rgba(128,128,128,0.3)"};"></div>' for i in range(10))
            
            # Distinct Card HTML Block
            st.markdown(f"""
                <div class="card-{s['status']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="roll-name">{s["name"]}</span>
                    </div>
                    <span class="roll-id">{s["id"]}</span><br>
                    <span class="roll-tag {tag_class}">{tag_label}</span>
                    <div class="seat-meter">{blocks}</div>
                    <div style="font-size: 12px; font-weight: 600; margin-top: 6px;">
                        Risk Score: <b>{s['risk']}%</b> <span style="opacity: 0.7; font-size:11px;">({s['delta']})</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Student Detail"):
                st.write(f"**Department:** {s['dept']}")
                st.write(f"**Semester:** {s['sem']}")
                st.write(f"**Attendance:** {s['attendance']}")
                st.write(f"**Notes:** {s['note']}")

# --- TAB 2: ATTENDANCE PATTERNS ---
with tab2:
    st.markdown('<div class="row-label">Weekly Fill Rate</div>', unsafe_allow_html=True)
    
    chart_data = pd.DataFrame(
        {
            "Week 1": [90, 85, 88],
            "Week 2": [82, 78, 80],
            "Week 3": [75, 60, 70],
            "Week 4": [52, 94, 76]
        },
        index=["Ali Khan", "Ayesha Ahmed", "Priya Raman"]
    ).T
    st.line_chart(chart_data, color=["#EE5959", "#2EA043", "#D29922"])

# --- TAB 3: EARLY ALERTS ---
with tab3:
    st.markdown('<div class="row-label">System-Generated Notes</div>', unsafe_allow_html=True)
    st.error("**Early Alert — Ali Khan (STU001)**\n\nAli has missed 3 consecutive lab sessions. Risk score spiked to 85%.")

# --- TAB 4: INTERVENTIONS (FULLY INTERACTIVE) ---
with tab4:
    st.markdown('<div class="row-label">Suggested Next Steps</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    
    with col_a:
        with st.container(border=True):
            st.subheader("High-Risk Intervention")
            st.write("1. Schedule 1-on-1 check-in within 48 hours.\n2. Notify academic advisor.")
            st.write("")
            
            # Interactive Alert Button
            if st.button("🚨 Send Alert", type="primary", key="btn_send_alert", use_container_width=True):
                st.toast("📧 Automated alert sent to Academic Advisor & Student!", icon="✅")
                st.success("Alert notification dispatched successfully for STU001 (Ali Khan).")

    with col_b:
        with st.container(border=True):
            st.subheader("Class-Wide Actions")
            st.write("1. Share lab review recordings.\n2. Add short interactive quizzes.")
            st.write("")
            
            # Downloadable Summary Data
            report_data = "Student_ID,Name,Department,Semester,Attendance_Rate,Risk_Score,Status\nSTU001,Ali Khan,BS IT,4th,52%,85%,High Risk\nSTU002,Ayesha Ahmed,BS IT,4th,94%,15%,Low Risk\nSTU003,Priya Raman,BS IT,4th,76%,45%,Medium Risk"
            
            # Interactive Download Button
            st.download_button(
                label="📥 Download Class Report",
                data=report_data,
                file_name="Class_Risk_Summary_Report.csv",
                mime="text/csv",
                key="btn_download_report",
                use_container_width=True
            )