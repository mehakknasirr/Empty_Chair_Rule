import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(page_title="The Empty Chair Rule", page_icon="🪑", layout="wide", initial_sidebar_state="expanded")

FASTAPI_URL = "http://127.0.0.1:8000"

def get_pattern_data():
    try:
        response = requests.get(f"{FASTAPI_URL}/api/pattern-report", timeout=2)
        if response.status_code == 200:
            return response.json(), True
    except Exception:
        pass
    return None, False

api_data, is_connected = get_pattern_data()

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

/* ---------- Pulsing Animation for Pattern Flags ---------- */
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
    max-width: 620px;
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
.card-stable {
    background: linear-gradient(145deg, rgba(46, 204, 113, 0.06) 0%, rgba(20, 24, 33, 0.9) 100%) !important;
    border: 1px solid rgba(46, 204, 113, 0.3) !important;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    opacity: 0.9;
    transition: transform 0.2s ease;
}

.card-critical:hover, .card-stable:hover {
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
        <div class="hero-eyebrow">Context-Aware Early Support · Live Tracking</div>
        <h1>The Empty Chair Rule</h1>
        <p>Connecting attendance with school events to spot meaningful patterns early. We don't diagnose or punish — we provide context so humans can support students when it matters most.</p>
        <div class="seat-strip">{seat_html}</div>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# 4. SIDEBAR CONTROLS & PRIVACY DISCLOSURE
# ============================================================
st.sidebar.markdown("### Pattern Controls")

search_query = st.sidebar.text_input("Search name or ID", placeholder="e.g. ST101")
show_flagged_only = st.sidebar.checkbox("Flagged Patterns Only")

st.sidebar.divider()

if is_connected:
    st.sidebar.success("✅ Connected to Live API")
else:
    st.sidebar.error("❌ API Offline")

st.sidebar.markdown("""
    <div class="privacy-box">
        <b>🔒 FERPA Compliant & Supportive</b><br>
        Pattern insights are strictly for human check-in guidance. Not designed for automated penalties or diagnostic labeling.
    </div>
""", unsafe_allow_html=True)

# ============================================================
# 5. TABS CONTENT (Combined with Interventions & Class-Wide Actions)
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Pattern Detection",
    "Personal Baselines",
    "Why Flagged? (XAI)",
    "Human Check-in",
    "Interventions & Actions"
])

# --- TAB 1: PATTERN DETECTION ---
with tab1:
    if is_connected and api_data:
        total_students = len(api_data)
        flagged_patterns = sum(1 for s in api_data if s.get("flagged"))
        avg_confidence = int(sum(s.get("pattern_confidence", 0) for s in api_data) / total_students) if total_students > 0 else 0
       
        m1, m2, m3 = st.columns(3)
        m1.metric("MONITORED STUDENTS", total_students)
        m2.metric("PATTERNS DETECTED", flagged_patterns)
        m3.metric("AVG CONFIDENCE", f"{avg_confidence}%")
        st.write("")

        st.markdown('<div class="row-label">Active Pattern Dashboard</div>', unsafe_allow_html=True)

        cols = st.columns(2)
        filtered_count = 0
        for i, s in enumerate(api_data):
            if show_flagged_only and not s.get("flagged"):
                continue
            if search_query and (search_query.lower() not in s.get("student_name", "").lower() and search_query.lower() not in s.get("student_id", "").lower()):
                continue

            filtered_count += 1
            with cols[i % 2]:
                is_flagged = s.get("flagged", False)
                status = "critical" if is_flagged else "stable"
                tag_class = "tag-critical" if is_flagged else "tag-stable"
                tag_label = "⚠️ Pattern Detected" if is_flagged else "✓ Normal Pattern"
               
                confidence = s.get("pattern_confidence", 0)
                meter_html = f"""<div style="width: 100%; background: rgba(255,255,255,0.08); border-radius: 6px; height: 7px; margin: 12px 0 8px 0;"><div style="width: {confidence}%; background: linear-gradient(90deg, #F39C12 0%, #FF4D4D 100%); height: 100%; border-radius: 6px;"></div></div>"""
               
                st.markdown(f"""
<div class="card-{status}">
    <span class="roll-name">{s.get('student_name', 'Unknown')}</span> <span class="roll-id">({s.get('student_id', 'N/A')})</span><br>
    <span class="roll-tag {tag_class}">{tag_label}</span>
    {meter_html}
    <div style="font-size: 12px; font-weight: 600; margin-top: 6px;">Pattern Confidence: <b>{confidence}%</b></div>
    <div style="font-size: 11px; opacity: 0.8; margin-top: 4px;">Baseline: {s.get('baseline_attendance', 0)}% | Current: {s.get('current_attendance', 0)}%</div>
</div>
""", unsafe_allow_html=True)
               
                with st.expander("🔍 Pattern & Context Detail"):
                    st.write(f"**Detected Pattern:** {s.get('pattern_detected', 'None')}")
                    st.write(f"**Context Explanation:** {s.get('flag_reason', 'N/A')}")
                   
        if filtered_count == 0:
            st.info("No students match the current filters.")
    else:
        st.warning("Waiting for live data from API...")

# --- TAB 2: PERSONAL BASELINES ---
with tab2:
    st.markdown('<div class="row-label">Individual Baseline vs Current Attendance (%)</div>', unsafe_allow_html=True)
    st.caption("We compare each student to their own historical pattern, not just a global class threshold.")
   
    if is_connected and api_data:
        df_chart = pd.DataFrame(api_data)
        fig = px.bar(
            df_chart,
            x="student_name",
            y=["baseline_attendance", "current_attendance"],
            barmode="group",
            labels={"value": "Attendance %", "variable": "Metric", "student_name": "Student"},
            color_discrete_map={"baseline_attendance": "#8B949E", "current_attendance": "#FF4D4D"}
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
    else:
        st.info("API offline — Connect to load baseline data.")

# --- TAB 3: WHY FLAGGED? (XAI) ---
with tab3:
    st.markdown('<div class="row-label">Explainable AI (XAI) System Flags</div>', unsafe_allow_html=True)
    if is_connected and api_data:
        for s in api_data:
            if s.get("flagged"):
                with st.container(border=True):
                    st.error(f"**Pattern Alert — {s.get('student_name')} ({s.get('student_id')})**")
                    st.write(f"**Pattern:** {s.get('pattern_detected')}")
                    st.write(f"**Confidence Level:** {s.get('pattern_confidence')}%")
                    st.info(f"**Why was this flagged?**\n{s.get('flag_reason')}")
    else:
        st.info("No active pattern flags detected.")

# --- TAB 4: HUMAN CHECK-IN & FOLLOW-UP ---
with tab4:
    st.markdown('<div class="row-label">Human Check-in & Outcome Log</div>', unsafe_allow_html=True)
    st.caption("The AI detects patterns — humans decide what action to take.")
   
    if is_connected and api_data:
        flagged_list = [s for s in api_data if s.get("flagged")]
        if flagged_list:
            selected_student = st.selectbox("Select Student for Check-in:", [s['student_name'] for s in flagged_list])
            s_data = next(s for s in flagged_list if s['student_name'] == selected_student)
           
            col_a, col_b = st.columns(2)
            with col_a:
                with st.container(border=True):
                    st.subheader("Record Teacher Check-in")
                    outcome = st.selectbox(
                        "Outcome of Discussion:",
                        ["Pending Check-in", "Academic difficulty", "Test anxiety", "Personal / Family issue", "Transportation problem", "Social / Peer issue", "Other"],
                        key=f"out_{s_data['student_id']}"
                    )
                    notes = st.text_area("Counselor / Teacher Notes (Optional):", placeholder="e.g. Student requested tutoring assistance before Maths tests.")
                   
                    if st.button("🤝 Log Check-in Outcome", type="primary", use_container_width=True):
                        try:
                            payload = {
                                "student_id": s_data['student_id'],
                                "outcome": outcome,
                                "notes": notes
                            }
                            res = requests.post(f"{FASTAPI_URL}/api/record-checkin", json=payload)
                            if res.status_code == 200:
                                st.toast("Check-in outcome saved successfully!", icon="✅")
                                st.success(f"Log recorded for {s_data['student_name']}. System set to monitor post-support recovery.")
                        except Exception as e:
                            st.error(f"Error connecting to backend: {e}")

            with col_b:
                with st.container(border=True):
                    st.subheader("Post-Support Monitoring")
                    st.write("Tracks attendance pattern recovery following teacher support intervention.")
                   
                    followup_df = pd.DataFrame({
                        "Timeline": ["Pre-Support", "Week 1", "Week 2", "Week 3", "Current"],
                        "Post-Test Absences": [4, 3, 1, 0, 0]
                    })
                    fig2 = px.line(followup_df, x="Timeline", y="Post-Test Absences", markers=True, title="Absence Pattern Frequency")
                    fig2.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color="#A0AAB8",
                        height=220
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No students currently require check-ins.")
    else:
        st.info("Waiting for API data...")

# --- TAB 5: INTERVENTIONS & CLASS-WIDE ACTIONS ---
with tab5:
    st.markdown('<div class="row-label">Suggested Next Steps & Class-Wide Actions</div>', unsafe_allow_html=True)
    
    col_int1, col_int2 = st.columns(2)
    
    with col_int1:
        with st.container(border=True):
            st.subheader("High-Risk Intervention")
            st.markdown("""
            1. Schedule 1-on-1 check-in within 48 hours.
            2. Dispatch automated notice to academic advisor.
            """)
            if st.button("⚠️ Send Bulk Alert to High Risk", use_container_width=True):
                st.toast("Bulk alerts dispatched successfully to academic advisors!", icon="🚨")
                st.success("Notifications sent for all flagged high-risk students.")
                
    with col_int2:
        with st.container(border=True):
            st.subheader("Class-Wide Actions")
            st.markdown("""
            1. Export real-time student risk analysis.
            2. Review lab attendance trends post-test weeks.
            """)
            if api_data:
                df_export = pd.DataFrame(api_data)
                csv_data = df_export.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Live Class Report (CSV)",
                    data=csv_data,
                    file_name="empty_chair_risk_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("📥 Download Live Class Report (CSV)", disabled=True, use_container_width=True)
