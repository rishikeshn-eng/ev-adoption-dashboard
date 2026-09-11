# ev-adoption-dashboard

A Streamlit dashboard for presenting survey research on attitudinal
ambivalence toward electric four-wheelers among tier-2 Indian city
consumers.

**This ships with synthetic placeholder data** (`data/sample_survey_data.csv`)
matching a plausible survey structure — it exists so the dashboard is
runnable and demonstrably works, not as a stand-in for your real findings.
Replace it with your actual survey export before this represents real
research; the app doesn't care about the data source as long as the
column names match (documented below).

## What it shows

- Adoption-barrier breakdown by category (cost, range anxiety, charging
  infrastructure, resale value uncertainty, etc.)
- Ambivalence score distribution across demographic segments
- City-by-city comparison
- A filterable raw-response table

## Expected data format

`data/sample_survey_data.csv` columns:

| column | type | description |
|---|---|---|
| `respondent_id` | string | unique ID |
| `city` | string | tier-2 city name |
| `age_bracket` | string | e.g. "25-34" |
| `income_bracket` | string | e.g. "5-10L" |
| `primary_barrier` | string | top-cited adoption barrier |
| `ambivalence_score` | float 1-5 | your survey's composite ambivalence measure |
| `would_consider_ev_next_purchase` | bool | |
| `open_response` | string | free-text comment, optional |

If your real export uses different column names, either rename them to
match or edit the `COLUMN_MAP` dict at the top of `app.py`.

## Setup

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Deploy for free (so you can share a live link, not just code)

See `DEPLOY.md` for the step-by-step Streamlit Community Cloud walkthrough.
