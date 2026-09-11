# Deploying the dashboard (free, ~10 minutes)

Streamlit Community Cloud is the free path — it deploys straight from a
GitHub repo, no server management.

1. **Push this project to its own GitHub repo** (see the main step-by-step
   in the chat for git basics — same process, different folder: `ev-adoption-dashboard`).
2. Go to **share.streamlit.io** and sign in with your GitHub account.
3. Click **New app**, pick the `ev-adoption-dashboard` repo, branch `main`,
   and set the main file path to `app.py`.
4. Click **Deploy**. First deploy takes 2-3 minutes while it installs
   `requirements.txt`.
5. You'll get a public URL like `https://ev-adoption-dashboard-<random>.streamlit.app`
   — that's what you put in your resume/GitHub README, not just the repo
   link, since a live dashboard is more impressive to click through than
   code someone has to run themselves.
6. Every time you `git push` an update to the repo, the deployed app
   redeploys automatically — no manual redeploy step.

## Before you deploy for real

Swap `data/sample_survey_data.csv` for your actual survey export first —
deploying with synthetic placeholder data and not flagging it clearly would
misrepresent the project. If you deploy before your real data is ready,
keep the "currently showing placeholder data" caption in `app.py` visible
rather than removing it.
