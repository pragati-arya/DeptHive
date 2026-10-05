import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="Depthive | GNIOT",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# BACKGROUND + DESIGN
# =========================================================
BG = Path("assets/depthive_bg.png")

if BG.exists():
    bg_css = f"""
    .stApp {{
        background:
            linear-gradient(rgba(244,249,253,0.86), rgba(244,249,253,0.92)),
            url("data:image/png;base64,{{BG64}}");
        background-size: cover;
        background-attachment: fixed;
    }}
    """
else:
    bg_css = """
    .stApp {
        background:
        radial-gradient(circle at 80% 10%, #dff8fa 0%, transparent 30%),
        linear-gradient(135deg, #f7fbff, #edf6fb);
    }
    """

import base64

if BG.exists():
    encoded = base64.b64encode(BG.read_bytes()).decode()
    bg_css = bg_css.replace("{BG64}", encoded)

st.markdown(
    f"""
    <style>
    {bg_css}

    /* REMOVE STREAMLIT DEFAULT SPACE */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.96);
        border-right: 1px solid #dce7ef;
    }}

    section[data-testid="stSidebar"] * {{
        color: #12304d;
    }}

    /* HEADINGS */
    h1, h2, h3 {{
        color: #102f4d !important;
        font-weight: 750 !important;
    }}

    p, label, span {{
        color: #49627a;
    }}

    /* HERO */
    .hero {{
        background: rgba(255,255,255,0.94);
        border: 1px solid #d7e5ef;
        border-radius: 28px;
        padding: 42px 48px;
        margin-bottom: 30px;
        box-shadow: 0 15px 45px rgba(30,70,100,0.10);
    }}

    .hero-title {{
        font-size: 38px;
        font-weight: 800;
        color: #0d3150;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }}

    .hero-main {{
        font-size: 25px;
        font-weight: 700;
        color: #153c5c;
        margin-bottom: 8px;
    }}

    .hero-sub {{
        font-size: 16px;
        color: #647d93;
        margin-bottom: 18px;
    }}

    .hero-tag {{
        display: inline-block;
        padding: 9px 16px;
        border-radius: 30px;
        background: #e5f7f7;
        color: #087f82;
        font-weight: 700;
        font-size: 13px;
    }}

    /* CARDS */
    .card {{
        background: rgba(255,255,255,0.96);
        border: 1px solid #d9e6ef;
        border-radius: 20px;
        padding: 22px;
        min-height: 145px;
        box-shadow: 0 8px 28px rgba(40,75,100,0.07);
    }}

    .card-title {{
        font-size: 13px;
        font-weight: 700;
        color: #71869a;
        text-transform: uppercase;
        letter-spacing: .7px;
    }}

    .card-value {{
        font-size: 32px;
        font-weight: 800;
        color: #102f4d;
        margin-top: 8px;
    }}

    .card-note {{
        font-size: 13px;
        color: #6d8397;
        margin-top: 6px;
    }}

    /* SECTION */
    .section-title {{
        font-size: 24px;
        font-weight: 750;
        color: #102f4d;
        margin-top: 25px;
        margin-bottom: 15px;
    }}

    /* ALERT */
    .alert {{
        background: #fff7e8;
        border-left: 5px solid #f2a900;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }}

    .alert-high {{
        background: #fff0f2;
        border-left: 5px solid #e84d68;
    }}

    .alert-title {{
        font-weight: 750;
        color: #17344f;
    }}

    .alert-text {{
        color: #64788b;
        margin-top: 4px;
        font-size: 14px;
    }}

    /* INFO BOX */
    .info-box {{
        background: rgba(255,255,255,.96);
        border: 1px solid #d9e6ef;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 7px 25px rgba(40,75,100,.06);
    }}

    /* BUTTONS */
    .stButton > button {{
        border-radius: 12px;
        border: 1px solid #cbdde9;
        background: white;
        color: #123653;
        font-weight: 650;
    }}

    .stButton > button:hover {{
        border-color: #16a6a9;
        color: #07878a;
    }}

    /* DATAFRAME */
    [data-testid="stDataFrame"] {{
        border-radius: 15px;
        overflow: hidden;
    }}

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DEMO DATA
# =========================================================
ORG_DATA = {
    "College": {
        "name": "Greater Noida Institute of Technology",
        "subtitle": "College Intelligence Workspace",
        "departments": {
            "Computer Science": 92,
            "Electronics": 84,
            "Mechanical": 76,
            "Civil": 71,
            "Management": 82
        },
        "kpis": {
            "Attendance": (82, 85),
            "Average CGPA": (7.8, 8.0),
            "Placement Rate": (78, 80),
            "Academic Stability": (86, 85)
        },
        "trend": [72, 74, 75, 77, 79, 82, 84]
    },

    "Hospital": {
        "name": "GNIOT Medical Operations Center",
        "subtitle": "Hospital Intelligence Workspace",
        "departments": {
            "Emergency": 78,
            "OPD": 86,
            "ICU": 73,
            "Radiology": 88,
            "Pharmacy": 82
        },
        "kpis": {
            "Bed Utilization": (81, 85),
            "Patient Flow": (76, 80),
            "Staff Availability": (88, 90),
            "Resource Efficiency": (84, 85)
        },
        "trend": [71, 73, 74, 76, 78, 80, 82]
    },

    "Company": {
        "name": "Depthive Enterprise Demo",
        "subtitle": "Corporate Intelligence Workspace",
        "departments": {
            "Technology": 92,
            "Sales": 89,
            "Finance": 86,
            "Human Resources": 81,
            "Marketing": 73
        },
        "kpis": {
            "Revenue Achievement": (91, 95),
            "Customer Retention": (84, 88),
            "Productivity": (87, 90),
            "Cost Efficiency": (79, 85)
        },
        "trend": [76, 78, 80, 81, 83, 85, 87]
    }
}

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown(
        """
        <div style="font-size:25px;font-weight:800;color:#123653;">
        ◆ DEPTHIVE
        </div>
        <div style="color:#71869a;margin-top:6px;margin-bottom:35px;">
        Organizational Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ORGANIZATION")

    org_type = st.selectbox(
        "Organization",
        ["College", "Hospital", "Company"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### INTELLIGENCE")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Department Ranking",
            "Risk Analysis",
            "Predictions",
            "Recommendations",
            "What-If Analysis",
            "Data Management"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.info(
        "Prototype Mode\n\n"
        "Depthive intelligence engine active."
    )

# =========================================================
# CURRENT DATA
# =========================================================
data = ORG_DATA[org_type]
departments = data["departments"]
kpis = data["kpis"]

overall_score = round(np.mean(list(departments.values())), 1)
high_risk = sum(score < 75 for score in departments.values())
trend_change = round(
    ((data["trend"][-1] - data["trend"][0]) / data["trend"][0]) * 100,
    1
)

# =========================================================
# HERO
# =========================================================
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">DEPTHIVE</div>
        <div class="hero-main">{data["name"]}</div>
        <div class="hero-sub">{data["subtitle"]}</div>
        <div class="hero-tag">
            UNDERSTAND &nbsp;•&nbsp; PREDICT &nbsp;•&nbsp; IMPROVE
            &nbsp;•&nbsp; ENABLE BETTER DECISIONS
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# OVERVIEW
# =========================================================
if page == "Overview":

    st.markdown("## Organization Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Overall Health", f"{overall_score}/100")

    with c2:
        st.metric("Total Departments", len(departments))

    with c3:
        st.metric("High Risk Departments", high_risk)

    with c4:
        st.metric("Performance Trend", f"+{trend_change}%")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown("### Department Performance")

        dept_df = pd.DataFrame({
            "Department": list(departments.keys()),
            "Score": list(departments.values())
        }).sort_values("Score", ascending=True)

        st.bar_chart(
            dept_df.set_index("Department"),
            y="Score",
            height=330
        )

    with right:
        st.markdown("### Performance Trend")

        trend_df = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
            "Performance": data["trend"]
        }).set_index("Month")

        st.line_chart(
            trend_df,
            height=330
        )

    st.markdown("## Key Performance Indicators")

    cols = st.columns(4)

    for col, (name, values) in zip(cols, kpis.items()):
        actual, target = values

        with col:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">{name}</div>
                    <div class="card-value">{actual}</div>
                    <div class="card-note">Target: {target}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("## Depthive Intelligence")

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            """
            <div class="info-box">
                <h3>🎯 DETECTED</h3>
                <b>Performance Gap</b>
                <p>Departments below the organizational performance baseline are detected automatically.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            """
            <div class="info-box">
                <h3>🔎 WHY</h3>
                <b>KPI & Resource Pressure</b>
                <p>Depthive identifies declining patterns and KPI gaps contributing to performance changes.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c:
        st.markdown(
            """
            <div class="info-box">
                <h3>💡 ACTION</h3>
                <b>Targeted Intervention</b>
                <p>Recommended actions are generated according to detected performance risks.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# DEPARTMENT RANKING
# =========================================================
elif page == "Department Ranking":

    st.markdown("## Department Ranking")

    ranking = pd.DataFrame({
        "Department": list(departments.keys()),
        "Performance Score": list(departments.values())
    }).sort_values(
        "Performance Score",
        ascending=False
    ).reset_index(drop=True)

    ranking.index = ranking.index + 1
    ranking.insert(0, "Rank", ranking.index)

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )

    best = ranking.iloc[0]
    weakest = ranking.iloc[-1]

    c1, c2 = st.columns(2)

    with c1:
        st.success(
            f"Top performing department: **{best['Department']}** "
            f"({best['Performance Score']}/100)"
        )

    with c2:
        st.warning(
            f"Department requiring attention: **{weakest['Department']}** "
            f"({weakest['Performance Score']}/100)"
        )

# =========================================================
# RISK
# =========================================================
elif page == "Risk Analysis":

    st.markdown("## Risk Analysis")

    for dept, score in sorted(departments.items(), key=lambda x: x[1]):

        if score < 75:
            st.markdown(
                f"""
                <div class="alert alert-high">
                    <div class="alert-title">🔴 HIGH RISK — {dept}</div>
                    <div class="alert-text">
                    Current performance score: {score}/100.
                    Performance is below the 75-point baseline.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif score < 82:
            st.markdown(
                f"""
                <div class="alert">
                    <div class="alert-title">🟡 MODERATE RISK — {dept}</div>
                    <div class="alert-text">
                    Current performance score: {score}/100.
                    Department should be monitored.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.success(
                f"🟢 LOW RISK — {dept}: {score}/100"
            )

# =========================================================
# PREDICTIONS
# =========================================================
elif page == "Predictions":

    st.markdown("## Performance Prediction")

    current = data["trend"][-1]
    previous = data["trend"][-2]

    monthly_change = current - previous
    predicted = round(current + monthly_change, 1)

    c1, c2, c3 = st.columns(3)

    c1.metric("Current Performance", current)
    c2.metric("Recent Change", f"+{monthly_change}")
    c3.metric("Next Period Projection", predicted)

    st.markdown(
        """
        <div class="info-box">
        <h3>Prediction Logic</h3>
        <p>
        Prototype projection uses the recent performance trend.
        In the production version, this layer can use trained
        machine-learning/time-series models with historical organizational data.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    forecast = data["trend"] + [predicted]

    forecast_df = pd.DataFrame({
        "Period": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Next"],
        "Performance": forecast
    }).set_index("Period")

    st.line_chart(forecast_df)

# =========================================================
# RECOMMENDATIONS
# =========================================================
elif page == "Recommendations":

    st.markdown("## AI Recommendation Center")

    weakest = min(departments, key=departments.get)
    score = departments[weakest]

    st.markdown(
        f"""
        <div class="info-box">
            <h3>Priority Department</h3>
            <h2>{weakest}</h2>
            <p>Current performance: <b>{score}/100</b></p>
            <hr>
            <h3>Recommended Actions</h3>
            <p>• Review department-level KPI gaps</p>
            <p>• Identify resource and workload constraints</p>
            <p>• Set a short-term improvement target</p>
            <p>• Re-evaluate performance in the next cycle</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# WHAT IF
# =========================================================
elif page == "What-If Analysis":

    st.markdown("## What-If Analysis")

    st.write(
        "Change the improvement assumption and estimate its impact."
    )

    improvement = st.slider(
        "Expected improvement (%)",
        min_value=0,
        max_value=20,
        value=5
    )

    estimated_score = min(
        100,
        round(overall_score * (1 + improvement / 100), 1)
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Current Score", f"{overall_score}/100")
    c2.metric("Improvement Assumption", f"+{improvement}%")
    c3.metric("Estimated Score", f"{estimated_score}/100")

    st.info(
        "This is a scenario estimate, not a guaranteed outcome."
    )

# =========================================================
# DATA MANAGEMENT
# =========================================================
elif page == "Data Management":

    st.markdown("## Data Management")

    st.write(
        "Organization administrators can upload structured operational data."
    )

    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded is not None:

        try:
            df = pd.read_csv(uploaded)

            if df.empty:
                st.error("The uploaded CSV is empty.")
            else:
                st.success("CSV loaded successfully.")
                st.write(f"Rows: {len(df)}")
                st.write(f"Columns: {len(df.columns)}")
                st.dataframe(
                    df.head(20),
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "DEPTHIVE • Universal Organizational Intelligence & Decision Support Platform • Prototype V1"
)