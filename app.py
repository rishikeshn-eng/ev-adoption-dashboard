"""
EV Adoption Survey Dashboard — Tier-2 India Research

This dashboard visualizes attitudes toward electric vehicle adoption in tier-2 Indian cities.
It measures attitudinal ambivalence, adoption barriers, and purchase intent across demographics.

The interface prioritizes readability and insight discovery, with a sustainability-first aesthetic.
Colors are drawn from natural/environmental themes to reinforce the EV/sustainability narrative.

Run: streamlit run app.py
Deploy: see DEPLOY.md
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="EV Adoption — Tier-2 India",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more intentional, sustainability-forward aesthetic.
# The palette uses: forest green (primary), sage green (accents), earth tones (supporting),
# paired with clean typography for technical clarity.
st.markdown("""
<style>
    /* Main color theme: sustainability-inspired */
    :root {
        --primary-green: #2d6a4f;      /* Forest green - authority, nature */
        --secondary-green: #52b788;    /* Mid-green - growth, vitality */
        --accent-green: #95d5b2;       /* Sage green - calm, analysis */
        --earth-brown: #8b7355;        /* Earth brown - grounding */
        --light-bg: #f1faee;           /* Near-white with green tint */
    }

    /* Typography: improve hierarchy and readability */
    h1 {
        color: #2d6a4f;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #2d6a4f;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    h3 {
        color: #52b788;
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* Metric cards: custom styling for better visual hierarchy */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f1faee 0%, #e8f5e9 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #52b788;
    }

    /* Sidebar: subtle green tint */
    [data-testid="stSidebar"] {
        background-color: #f8fdf8;
    }

    /* Main dividers: use green instead of default gray */
    hr {
        border-top: 2px solid #95d5b2 !important;
        margin: 2rem 0 !important;
    }

    /* Improve button aesthetics */
    button {
        background-color: #52b788;
        color: white;
        border: none;
        border-radius: 6px;
    }

    button:hover {
        background-color: #2d6a4f;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & VALIDATION
# ============================================================================

# Column name mapping allows flexibility in source data formats.
# Edit here if your survey export uses different column names;
# the dashboard logic remains unchanged.
COLUMN_MAP = {
    "respondent_id": "respondent_id",
    "city": "city",
    "age_bracket": "age_bracket",
    "income_bracket": "income_bracket",
    "primary_barrier": "primary_barrier",
    "ambivalence_score": "ambivalence_score",
    "would_consider_ev_next_purchase": "would_consider_ev_next_purchase",
    "open_response": "open_response",
}

DATA_PATH = "data/sample_survey_data.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """
    Load and normalize survey data from CSV.

    Applies column name mapping to handle different source formats
    without changing upstream data exports.
    """
    df = pd.read_csv(path)
    df = df.rename(columns={v: k for k, v in COLUMN_MAP.items()})
    return df


# Load data once per session (Streamlit caches this automatically)
df = load_data(DATA_PATH)

# ============================================================================
# HEADER & CONTEXT
# ============================================================================

st.title("🌱 EV Adoption Attitudes — Tier-2 Indian Cities")

st.markdown("""
**Research focus:** Understanding attitudinal ambivalence toward electric four-wheelers
in emerging markets. This dashboard aggregates survey responses across demographics,
barriers, and purchase intent.

> ⚠️ **Currently showing synthetic placeholder data.** Replace `data/sample_survey_data.csv`
> with your real survey export to activate live analysis.
""")

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.markdown("### 🎯 Refine the view")
st.sidebar.markdown("Use these filters to explore patterns by city and age group.")

cities = st.sidebar.multiselect(
    "City",
    sorted(df["city"].unique()),
    default=sorted(df["city"].unique()),
    help="Select one or more cities to focus analysis."
)

age_filter = st.sidebar.multiselect(
    "Age bracket",
    sorted(df["age_bracket"].unique()),
    default=sorted(df["age_bracket"].unique()),
    help="Narrow by age group to see demographic patterns."
)

# Apply filters to create a working dataset for all downstream charts.
# This single filtered dataset ensures consistency across all metrics.
filtered = df[df["city"].isin(cities) & df["age_bracket"].isin(age_filter)]

# ============================================================================
# TOP-LINE METRICS
# ============================================================================

st.markdown("### 📊 At a glance")

# Organize metrics in a 3-column layout for quick comparison.
# Each metric tells one story: volume, sentiment, and intent.
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Sample size",
        f"{len(filtered)} respondents",
        help="Number of survey responses matching current filters"
    )

with col2:
    ambivalence_avg = filtered["ambivalence_score"].mean()
    st.metric(
        "⚖️ Avg. ambivalence",
        f"{ambivalence_avg:.2f} / 5.0",
        help="Scale measuring conflicted feelings toward EV adoption (higher = more conflicted)"
    )

with col3:
    intent_pct = filtered["would_consider_ev_next_purchase"].mean() * 100
    st.metric(
        "✨ Purchase intent",
        f"{intent_pct:.0f}%",
        help="Respondents who would consider an EV for their next vehicle purchase"
    )

st.markdown("---")

# ============================================================================
# BARRIER ANALYSIS & DISTRIBUTION
# ============================================================================

st.markdown("### 🚧 What's holding adoption back?")

left, right = st.columns(2)

# Left: Adoption barriers as horizontal bar chart
# Horizontal orientation makes barrier labels more readable without crowding.
# Color gradient reinforces that each barrier is distinct.
with left:
    st.markdown("**Primary barriers to adoption**")
    barrier_counts = filtered["primary_barrier"].value_counts().reset_index()
    barrier_counts.columns = ["barrier", "count"]

    # Use sustainability-themed color scale: from sage green (few) to forest green (many)
    fig_barrier = px.bar(
        barrier_counts,
        x="count",
        y="barrier",
        orientation="h",
        color="count",
        color_continuous_scale=["#95d5b2", "#52b788", "#2d6a4f"],
        title=None,
    )
    fig_barrier.update_layout(
        showlegend=False,
        yaxis_title=None,
        xaxis_title="Number of respondents",
        height=350,
        margin=dict(l=150, r=20, t=20, b=50),
        font=dict(size=12),
        plot_bgcolor="rgba(241, 250, 238, 0.5)",  # Light green background
    )
    fig_barrier.update_traces(
        hovertemplate="<b>%{y}</b><br>%{x} respondents<extra></extra>"
    )
    st.plotly_chart(fig_barrier, use_container_width=True)

# Right: Ambivalence score distribution as histogram
# This shows the spread of opinion—are respondents clustered or spread?
# Higher concentration in middle bins indicates true ambivalence.
with right:
    st.markdown("**How split are people?** (Ambivalence distribution)")
    fig_dist = px.histogram(
        filtered,
        x="ambivalence_score",
        nbins=10,
        color_discrete_sequence=["#52b788"],
        title=None,
    )
    fig_dist.update_layout(
        xaxis_title="Ambivalence score (1 = clear yes/no, 5 = very conflicted)",
        yaxis_title="Number of respondents",
        height=350,
        plot_bgcolor="rgba(241, 250, 238, 0.5)",
        font=dict(size=12),
    )
    fig_dist.update_traces(
        hovertemplate="Score %{x}<br>%{y} respondents<extra></extra>"
    )
    st.plotly_chart(fig_dist, use_container_width=True)

st.markdown("---")

# ============================================================================
# GEOGRAPHIC & DEMOGRAPHIC PATTERNS
# ============================================================================

st.markdown("### 🗺️ City-by-city comparison")

# Ambivalence by city reveals geographic variation in EV sentiment.
# This helps identify which markets have stronger adoption readiness.
city_summary = (
    filtered.groupby("city")["ambivalence_score"]
    .mean()
    .reset_index()
    .sort_values("ambivalence_score")
)

fig_city = px.bar(
    city_summary,
    x="ambivalence_score",
    y="city",
    orientation="h",
    color="ambivalence_score",
    color_continuous_scale=["#2d6a4f", "#52b788", "#95d5b2"],
    title=None,
)
fig_city.update_layout(
    yaxis_title=None,
    xaxis_title="Average ambivalence score (lower = stronger readiness)",
    height=300,
    plot_bgcolor="rgba(241, 250, 238, 0.5)",
    margin=dict(l=100, r=20, t=20, b=50),
    font=dict(size=12),
)
fig_city.update_traces(
    hovertemplate="<b>%{y}</b><br>Average score: %{x:.2f}<extra></extra>"
)
st.plotly_chart(fig_city, use_container_width=True)

st.markdown("---")

# ============================================================================
# RESPONDENT-LEVEL DATA & QUALITATIVE INSIGHTS
# ============================================================================

st.markdown("### 💬 What people are saying")
st.markdown("Browse individual responses and open-ended comments below.")

# Checkbox to toggle between all responses and only those with qualitative feedback.
# Researchers often want to focus on respondents who elaborated their views.
show_comments_only = st.checkbox(
    "Show only responses with written comments",
    value=False,
    help="Filter to respondents who provided open-ended feedback"
)

# Apply comment filter and display table
table_df = (
    filtered[filtered["open_response"].astype(str).str.len() > 0]
    if show_comments_only
    else filtered
)

st.dataframe(
    table_df.sort_values("ambivalence_score", ascending=False),
    use_container_width=True,
    hide_index=True,
    height=400,
)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8b7355; font-size: 0.9rem; margin-top: 2rem;">
    <p><strong>About this research</strong><br>
    Survey respondents: tier-2 Indian cities | Focus: EV adoption attitudes &amp; barriers<br>
    Data managed by: Rishi Nair, Sustainable Energy Engineering, IIT Roorkee</p>
    <p style="font-size: 0.85rem;">For analysis questions or data access, contact the researcher.</p>
</div>
""", unsafe_allow_html=True)
