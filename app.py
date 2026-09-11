"""
EV adoption survey dashboard.

Run: streamlit run app.py
Deploy: see DEPLOY.md
"""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="EV Adoption — Tier-2 India", layout="wide")

# If your real survey export uses different column names, edit this map
# rather than renaming your source file.
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
    df = pd.read_csv(path)
    df = df.rename(columns={v: k for k, v in COLUMN_MAP.items()})
    return df


df = load_data(DATA_PATH)

st.title("EV Adoption Attitudes — Tier-2 Indian Cities")
st.caption(
    "Survey research on attitudinal ambivalence toward electric four-wheelers. "
    "Currently showing placeholder/synthetic data — replace data/sample_survey_data.csv "
    "with your real export to make this live."
)

# --- Sidebar filters ---
st.sidebar.header("Filters")
cities = st.sidebar.multiselect("City", sorted(df["city"].unique()), default=sorted(df["city"].unique()))
age_filter = st.sidebar.multiselect("Age bracket", sorted(df["age_bracket"].unique()), default=sorted(df["age_bracket"].unique()))
filtered = df[df["city"].isin(cities) & df["age_bracket"].isin(age_filter)]

# --- Top-line metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Respondents (filtered)", len(filtered))
col2.metric("Avg. ambivalence score", f"{filtered['ambivalence_score'].mean():.2f} / 5")
col3.metric("Would consider EV next purchase", f"{filtered['would_consider_ev_next_purchase'].mean()*100:.0f}%")

st.divider()

# --- Barrier breakdown ---
left, right = st.columns(2)
with left:
    st.subheader("Primary adoption barrier")
    barrier_counts = filtered["primary_barrier"].value_counts().reset_index()
    barrier_counts.columns = ["barrier", "count"]
    fig = px.bar(barrier_counts, x="count", y="barrier", orientation="h",
                 color="barrier", title=None)
    fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Respondents")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Ambivalence score distribution")
    fig2 = px.histogram(filtered, x="ambivalence_score", nbins=10)
    fig2.update_layout(xaxis_title="Ambivalence score (1-5)", yaxis_title="Respondents")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- City comparison ---
st.subheader("Ambivalence by city")
city_summary = filtered.groupby("city")["ambivalence_score"].mean().reset_index().sort_values("ambivalence_score")
fig3 = px.bar(city_summary, x="city", y="ambivalence_score")
fig3.update_layout(yaxis_title="Avg. ambivalence score", xaxis_title=None)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Raw data / open responses ---
st.subheader("Respondent-level data")
show_comments_only = st.checkbox("Only show rows with an open-ended comment", value=False)
table_df = filtered[filtered["open_response"].astype(str).str.len() > 0] if show_comments_only else filtered
st.dataframe(table_df, use_container_width=True, hide_index=True)
