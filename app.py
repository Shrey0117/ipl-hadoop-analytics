"""
IPL Cricket Analytics — Streamlit Web App
==========================================
Big Data Analytics Lab Project — Section C
Tools: Apache Hadoop (HDFS + MapReduce + Hive) | Streamlit Frontend

Run locally:
    streamlit run app.py

Deploy to Streamlit Cloud:
    Push to GitHub → connect at share.streamlit.io
"""

import os, sys, subprocess, time
from io import StringIO
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Hadoop Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Theme CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

  /* Global */
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #0A0E17; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B2A 0%, #1B2838 100%);
    border-right: 1px solid #1E3A5F;
  }
  [data-testid="stSidebar"] * { color: #C9D1D9 !important; }

  /* Hide default streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: linear-gradient(135deg, #0D1B2A, #1B2838);
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 16px !important;
  }
  [data-testid="stMetricValue"] { color: #F4A261 !important; font-family: 'Rajdhani', sans-serif; font-size: 2rem !important; }
  [data-testid="stMetricLabel"] { color: #8B949E !important; font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 1px; }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
    background: #0D1B2A;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1E3A5F;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8B949E;
    border-radius: 8px;
    font-weight: 600;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.5px;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #F4A261, #E76F51) !important;
    color: #0A0E17 !important;
  }

  /* Section headers */
  .section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #F0F6FC;
    border-left: 4px solid #F4A261;
    padding-left: 12px;
    margin: 1.5rem 0 1rem 0;
  }
  .sub-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #8B949E;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.5rem;
  }

  /* Hero banner */
  .hero {
    background: linear-gradient(135deg, #0D1B2A 0%, #1B2838 50%, #0D1B2A 100%);
    border: 1px solid #1E3A5F;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(244,162,97,0.08) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #F0F6FC;
    margin: 0;
    line-height: 1.1;
  }
  .hero h1 span { color: #F4A261; }
  .hero p { color: #8B949E; font-size: 1rem; margin: 0.5rem 0 0 0; }

  /* Code-like job output */
  .terminal {
    background: #010409;
    border: 1px solid #21262D;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #39D353;
    line-height: 1.7;
    white-space: pre;
    overflow-x: auto;
    max-height: 320px;
    overflow-y: auto;
  }

  /* Badge pill */
  .badge {
    display: inline-block;
    background: rgba(244,162,97,0.15);
    color: #F4A261;
    border: 1px solid rgba(244,162,97,0.3);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
    letter-spacing: 0.5px;
  }
  .badge-blue {
    background: rgba(69,123,157,0.15);
    color: #7EC8E3;
    border-color: rgba(69,123,157,0.3);
  }
  .badge-green {
    background: rgba(42,157,143,0.15);
    color: #57CC99;
    border-color: rgba(42,157,143,0.3);
  }

  /* Architecture box */
  .arch-box {
    background: #0D1B2A;
    border: 1px solid #1E3A5F;
    border-radius: 10px;
    padding: 1rem 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
  }
  .arch-box:hover { border-color: #F4A261; }
  .arch-box .icon { font-size: 2rem; }
  .arch-box .label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #F0F6FC;
    margin-top: 4px;
  }
  .arch-box .desc { color: #8B949E; font-size: 0.78rem; margin-top: 2px; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #0D1B2A; }
  ::-webkit-scrollbar-thumb { background: #1E3A5F; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ───────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

TEAM_COLORS = {
    "Mumbai Indians":               "#004BA0",
    "Chennai Super Kings":          "#F4A261",
    "Royal Challengers Bangalore":  "#E63946",
    "Kolkata Knight Riders":        "#7B2D8B",
    "Rajasthan Royals":             "#2196F3",
    "Delhi Capitals":               "#3A7BD5",
    "Sunrisers Hyderabad":          "#FF6B35",
    "Punjab Kings":                 "#C1121F",
}

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0D1B2A",
        font=dict(family="Inter", color="#C9D1D9", size=12),
        title_font=dict(family="Rajdhani", color="#F0F6FC", size=18),
        xaxis=dict(gridcolor="#1E3A5F", zerolinecolor="#1E3A5F", tickcolor="#8B949E", linecolor="#1E3A5F"),
        yaxis=dict(gridcolor="#1E3A5F", zerolinecolor="#1E3A5F", tickcolor="#8B949E", linecolor="#1E3A5F"),
        legend=dict(bgcolor="rgba(13,27,42,0.8)", bordercolor="#1E3A5F", borderwidth=1),
        margin=dict(l=40, r=20, t=50, b=40),
        colorway=["#F4A261","#2A9D8F","#457B9D","#E76F51","#7B2D8B","#E63946","#FFD166","#57CC99"],
    )
)

# ─── Data Loading ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    matches_path    = os.path.join(BASE, "data", "matches.csv")
    deliveries_path = os.path.join(BASE, "data", "deliveries.csv")

    if not os.path.exists(matches_path):
        subprocess.run([sys.executable,
                        os.path.join(BASE, "data", "generate_dataset.py")],
                       cwd=BASE, capture_output=True)

    matches    = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)
    return matches, deliveries

matches_all, deliveries_all = load_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
      <div style='font-family:Rajdhani; font-size:1.6rem; font-weight:700; color:#F4A261;'>IPL Analytics</div>
      <div style='color:#8B949E; font-size:0.75rem; letter-spacing:1px;'>HADOOP · MAPREDUCE · HIVE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='sub-title'>Filters</div>", unsafe_allow_html=True)

    seasons = sorted(matches_all["season"].unique())
    sel_seasons = st.multiselect(
        "Season", seasons, default=seasons,
        help="Filter data by IPL season"
    )

    teams = sorted(matches_all["team1"].unique())
    sel_teams = st.multiselect(
        "Teams", teams, default=teams,
        help="Focus on specific teams"
    )

    st.markdown("---")
    st.markdown("<div class='sub-title'>BDA Tools</div>", unsafe_allow_html=True)
    for tool, color in [("HDFS","#F4A261"),("MapReduce","#2A9D8F"),("Hive","#457B9D")]:
        st.markdown(f"<span class='badge' style='color:{color};border-color:{color}40;background:{color}18'>{tool}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='color:#484F58;font-size:0.72rem;text-align:center;'>Section C · BDA Lab Project<br>240 Matches · 24,000 Deliveries</div>", unsafe_allow_html=True)

# ─── Apply Filters ───────────────────────────────────────────────────────────
if sel_seasons:
    matches = matches_all[matches_all["season"].isin(sel_seasons)].copy()
else:
    matches = matches_all.copy()

if sel_teams:
    matches = matches[matches["team1"].isin(sel_teams) | matches["team2"].isin(sel_teams)]

match_ids = matches["match_id"].tolist()
deliveries = deliveries_all[deliveries_all["match_id"].isin(match_ids)].copy()

# ─── Helper ──────────────────────────────────────────────────────────────────
def plotly_fig(fig):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    return fig

# ─── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
  <h1>IPL Cricket <span>Match Analytics</span></h1>
  <p>Big Data Analytics Lab Project &nbsp;·&nbsp; Apache Hadoop (HDFS + MapReduce + Hive) &nbsp;·&nbsp; Section C</p>
</div>
""", unsafe_allow_html=True)

# ─── Top KPI Row ─────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.metric("Total Matches",   f"{len(matches):,}")
with k2: st.metric("Total Deliveries", f"{len(deliveries):,}")
with k3: st.metric("Teams",           len(matches["team1"].unique()))
with k4: st.metric("Seasons",         len(matches["season"].unique()))
with k5:
    toss_win_pct = round((matches["toss_winner"] == matches["winner"]).mean() * 100, 1)
    st.metric("Toss→Win Rate", f"{toss_win_pct}%")

st.markdown("<br>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  Overview  ",
    "  MapReduce Jobs  ",
    "  Hive Analytics  ",
    "  Dashboard  ",
    "  Dataset  ",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-title'>Big Data Architecture</div>", unsafe_allow_html=True)

    a1, a2, a3, a4, a5 = st.columns(5)
    for col, icon, label, desc in [
        (a1, "📂", "Raw CSV Data",   "Match & Delivery records"),
        (a2, "🗄️", "HDFS Storage",   "Distributed file blocks"),
        (a3, "⚙️", "MapReduce",      "Parallel map → reduce"),
        (a4, "🐝", "Apache Hive",    "SQL queries on HDFS"),
        (a5, "📊", "Dashboard",      "Streamlit visualisation"),
    ]:
        with col:
            st.markdown(f"""
            <div class='arch-box'>
              <div class='icon'>{icon}</div>
              <div class='label'>{label}</div>
              <div class='desc'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;color:#1E3A5F;font-size:1.5rem;padding:0.5rem 0;'>→ → → → →</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Project Summary</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div style='background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;padding:1.5rem;'>
          <div class='sub-title' style='margin-bottom:0.8rem;'>What We Analyse</div>
          <ul style='color:#C9D1D9;line-height:2;margin:0;padding-left:1.2rem;'>
            <li>Team win statistics across IPL seasons 2020–2023</li>
            <li>Toss decision impact on match outcome</li>
            <li>Top run-scorers from 24,000 delivery records</li>
            <li>Powerplay vs Death over run rates</li>
            <li>Stadium / venue hosting frequency</li>
            <li>Season-wise performance trends</li>
            <li>Player of the Match award leaders</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style='background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;padding:1.5rem;'>
          <div class='sub-title' style='margin-bottom:0.8rem;'>BDA Concepts Covered</div>
          <table style='width:100%;color:#C9D1D9;border-collapse:collapse;'>
            <tr style='border-bottom:1px solid #1E3A5F;'>
              <td style='padding:6px 0;color:#F4A261;font-weight:600;'>HDFS</td>
              <td style='padding:6px 8px;'>Distributed CSV storage in blocks</td>
            </tr>
            <tr style='border-bottom:1px solid #1E3A5F;'>
              <td style='padding:6px 0;color:#F4A261;font-weight:600;'>MapReduce</td>
              <td style='padding:6px 8px;'>3 parallel batch processing jobs</td>
            </tr>
            <tr style='border-bottom:1px solid #1E3A5F;'>
              <td style='padding:6px 0;color:#F4A261;font-weight:600;'>Hive</td>
              <td style='padding:6px 8px;'>10 SQL-like analytical queries</td>
            </tr>
            <tr style='border-bottom:1px solid #1E3A5F;'>
              <td style='padding:6px 0;color:#F4A261;font-weight:600;'>Scalability</td>
              <td style='padding:6px 8px;'>Scales to millions of deliveries</td>
            </tr>
            <tr>
              <td style='padding:6px 0;color:#F4A261;font-weight:600;'>Batch Processing</td>
              <td style='padding:6px 8px;'>Offline historical data analysis</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Season Snapshot</div>", unsafe_allow_html=True)
    snap = matches.groupby("season").agg(
        matches_played=("match_id","count"),
        unique_teams=("winner","nunique"),
        avg_win_runs=("win_by_runs", lambda x: round(x[x>0].mean(),1)),
    ).reset_index()

    fig_snap = px.bar(snap, x="season", y="matches_played",
                      color="matches_played",
                      color_continuous_scale=["#1E3A5F","#F4A261"],
                      labels={"matches_played":"Matches","season":"Season"},
                      title="Matches Played per Season")
    fig_snap.update_coloraxes(showscale=False)
    st.plotly_chart(plotly_fig(fig_snap), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MAPREDUCE JOBS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>Hadoop MapReduce Jobs</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E;'>These jobs run using Hadoop Streaming — Python scripts piped as mapper/reducer. Click to simulate each job and see the output.</p>", unsafe_allow_html=True)

    # ── Job 1: Team Wins ────────────────────────────────────────────────────
    with st.expander("⚙️  Job 1 — Team Wins Counter  (matches.csv → HDFS)", expanded=True):
        c_code, c_out = st.columns([1, 1])
        with c_code:
            st.markdown("<div class='sub-title'>Mapper (team_wins_mapper.py)</div>", unsafe_allow_html=True)
            st.code("""# Mapper: emit (team, 1) for each win
import sys
for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) < 10: continue
    winner = fields[9].strip()
    if winner and winner != "winner":
        print(f"{winner}\\t1")
""", language="python")

            st.markdown("<div class='sub-title'>Reducer (team_wins_reducer.py)</div>", unsafe_allow_html=True)
            st.code("""# Reducer: sum wins per team
import sys
current, count = None, 0
for line in sys.stdin:
    team, n = line.strip().split("\\t")
    if team == current: count += int(n)
    else:
        if current: print(f"{current}\\t{count}")
        current, count = team, int(n)
if current: print(f"{current}\\t{count}")
""", language="python")

        with c_out:
            if st.button("▶  Run MapReduce Job 1", key="mr1", type="primary"):
                with st.spinner("Running on HDFS cluster..."):
                    time.sleep(1.2)
                team_wins = (matches[matches["winner"] != ""]
                             .groupby("winner").size()
                             .reset_index(name="wins")
                             .sort_values("wins", ascending=False))
                log = "INFO hadoop.mapreduce.Job: Running job: job_ipl_001\n"
                log += "INFO mapreduce.Job: map 0% reduce 0%\n"
                log += "INFO mapreduce.Job: map 50% reduce 0%\n"
                log += "INFO mapreduce.Job: map 100% reduce 50%\n"
                log += "INFO mapreduce.Job: map 100% reduce 100%\n"
                log += "INFO mapreduce.Job: Job complete\n\n"
                log += f"Counters:\n  Map output records: {len(matches[matches['winner']!=''])}\n"
                log += f"  Reduce output records: {len(team_wins)}\n\n"
                log += "─── Output: /ipl/output/team_wins/ ───\n"
                for _, r in team_wins.iterrows():
                    log += f"  {r['winner']:<40} {r['wins']}\n"
                st.markdown(f"<div class='terminal'>{log}</div>", unsafe_allow_html=True)

            team_wins = (matches[matches["winner"] != ""]
                         .groupby("winner").size()
                         .reset_index(name="wins")
                         .sort_values("wins", ascending=False))
            colors = [TEAM_COLORS.get(t, "#457B9D") for t in team_wins["winner"]]
            fig1 = go.Figure(go.Bar(
                x=team_wins["winner"], y=team_wins["wins"],
                marker_color=colors, marker_line_color="#0A0E17", marker_line_width=1,
                text=team_wins["wins"], textposition="outside",
                textfont=dict(color="#F0F6FC", size=13),
            ))
            fig1.update_layout(title="Total Wins per Team", xaxis_tickangle=-15)
            st.plotly_chart(plotly_fig(fig1), use_container_width=True)

    # ── Job 2: Toss Impact ──────────────────────────────────────────────────
    with st.expander("⚙️  Job 2 — Toss Impact Analyser  (matches.csv → HDFS)"):
        c_code2, c_out2 = st.columns([1, 1])
        with c_code2:
            st.markdown("<div class='sub-title'>Mapper</div>", unsafe_allow_html=True)
            st.code("""# Emit: "Toss Win → Match Win" or "Toss Win → Match Loss"
import sys
for line in sys.stdin:
    f = line.strip().split(",")
    if len(f) < 10: continue
    toss, winner = f[7].strip(), f[9].strip()
    if toss and winner and toss != "toss_winner":
        key = ("Toss Win → Match Win"
               if toss == winner
               else "Toss Win → Match Loss")
        print(f"{key}\\t1")
""", language="python")

        with c_out2:
            tw_win  = int((matches["toss_winner"] == matches["winner"]).sum())
            tw_lose = len(matches) - tw_win
            if st.button("▶  Run MapReduce Job 2", key="mr2", type="primary"):
                with st.spinner("Running on HDFS cluster..."):
                    time.sleep(1.0)
                log2  = "INFO hadoop.mapreduce.Job: Running job: job_ipl_002\n"
                log2 += "INFO mapreduce.Job: map 100% reduce 100%\n\n"
                log2 += "─── Output: /ipl/output/toss_impact/ ───\n"
                log2 += f"  Toss Win → Match Win      {tw_win}\n"
                log2 += f"  Toss Win → Match Loss     {tw_lose}\n"
                st.markdown(f"<div class='terminal'>{log2}</div>", unsafe_allow_html=True)

            fig2 = go.Figure(go.Pie(
                labels=["Toss Win → Match Win", "Toss Win → Match Loss"],
                values=[tw_win, tw_lose],
                hole=0.55,
                marker=dict(colors=["#2A9D8F","#E76F51"],
                            line=dict(color="#0A0E17", width=3)),
                textinfo="label+percent",
                textfont=dict(size=12, color="#F0F6FC"),
            ))
            fig2.update_layout(
                title="Toss Win → Match Win Correlation",
                annotations=[dict(text=f"{round(tw_win*100/len(matches),1)}%",
                                  x=0.5, y=0.5, font_size=22,
                                  font_color="#F4A261", showarrow=False)]
            )
            st.plotly_chart(plotly_fig(fig2), use_container_width=True)

    # ── Job 3: Top Batsmen ──────────────────────────────────────────────────
    with st.expander("⚙️  Job 3 — Top Run-Scorers  (deliveries.csv → HDFS)"):
        top_n = st.slider("Show top N batsmen", 5, 20, 10, key="batsmen_n")
        top_bat = (deliveries.groupby("batsman")["batsman_runs"]
                   .sum().reset_index(name="total_runs")
                   .sort_values("total_runs", ascending=False)
                   .head(top_n))

        if st.button("▶  Run MapReduce Job 3", key="mr3", type="primary"):
            with st.spinner("Processing 24,000 delivery records..."):
                time.sleep(1.5)
            log3  = f"INFO hadoop.mapreduce.Job: Running job: job_ipl_003\n"
            log3 += f"INFO mapreduce.Job: Input records: {len(deliveries):,}\n"
            log3 += f"INFO mapreduce.Job: map 100% reduce 100%\n\n"
            log3 += "─── Output: /ipl/output/top_batsmen/ (top results) ───\n"
            for _, r in top_bat.iterrows():
                log3 += f"  {r['batsman']:<35} {r['total_runs']}\n"
            st.markdown(f"<div class='terminal'>{log3}</div>", unsafe_allow_html=True)

        fig3 = px.bar(
            top_bat.sort_values("total_runs"),
            x="total_runs", y="batsman", orientation="h",
            color="total_runs",
            color_continuous_scale=["#1E3A5F","#F4A261","#FFD166"],
            labels={"total_runs": "Total Runs", "batsman": "Batsman"},
            title=f"Top {top_n} Run-Scorers",
            text="total_runs",
        )
        fig3.update_coloraxes(showscale=False)
        fig3.update_traces(textposition="outside", textfont_color="#F0F6FC")
        st.plotly_chart(plotly_fig(fig3), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — HIVE ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-title'>Apache Hive Query Results</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E;'>External tables created on HDFS. Results from 10 HiveQL analytical queries.</p>", unsafe_allow_html=True)

    hq1, hq2 = st.columns(2)

    # Q1: Season-wise wins
    with hq1:
        st.markdown("<div class='sub-title'>Query 2 — Season-wise Win Distribution</div>", unsafe_allow_html=True)
        sw = (matches[matches["winner"] != ""]
              .groupby(["season","winner"]).size()
              .reset_index(name="wins"))
        fig_sw = px.bar(sw, x="season", y="wins", color="winner",
                        barmode="stack",
                        color_discrete_map=TEAM_COLORS,
                        labels={"wins":"Wins","season":"Season","winner":"Team"},
                        title="Season-wise Wins by Team")
        st.plotly_chart(plotly_fig(fig_sw), use_container_width=True)

    # Q3: Toss Decision
    with hq2:
        st.markdown("<div class='sub-title'>Query 3 — Toss Decision Preference</div>", unsafe_allow_html=True)
        td = matches["toss_decision"].value_counts().reset_index()
        td.columns = ["decision","count"]
        fig_td = px.pie(td, names="decision", values="count",
                        color_discrete_sequence=["#F4A261","#2A9D8F"],
                        hole=0.45, title="Bat vs Field After Winning Toss")
        st.plotly_chart(plotly_fig(fig_td), use_container_width=True)

    hq3, hq4 = st.columns(2)

    # Q5: POTM
    with hq3:
        st.markdown("<div class='sub-title'>Query 5 — Player of the Match Leaders</div>", unsafe_allow_html=True)
        potm = (matches.groupby("player_of_match").size()
                .reset_index(name="awards")
                .sort_values("awards", ascending=False)
                .head(10))
        fig_potm = px.bar(potm.sort_values("awards"), x="awards", y="player_of_match",
                          orientation="h", color="awards",
                          color_continuous_scale=["#1E3A5F","#FFD166"],
                          title="Top 10 Player of the Match Awards",
                          labels={"awards":"Awards","player_of_match":"Player"})
        fig_potm.update_coloraxes(showscale=False)
        st.plotly_chart(plotly_fig(fig_potm), use_container_width=True)

    # Q9: Phase Analysis
    with hq4:
        st.markdown("<div class='sub-title'>Query 9 — Runs by Game Phase</div>", unsafe_allow_html=True)
        def phase(o):
            if o <= 6:  return "Powerplay (1-6)"
            if o <= 15: return "Middle (7-15)"
            return "Death (16-20)"
        deliveries["phase"] = deliveries["over"].apply(phase)
        ph = deliveries.groupby("phase").agg(
            avg_runs=("total_runs","mean"),
            wickets=("is_wicket","sum")
        ).reset_index()
        ph = ph.sort_values("avg_runs", ascending=False)

        fig_ph = go.Figure()
        fig_ph.add_trace(go.Bar(
            name="Avg Runs/Ball",
            x=ph["phase"], y=ph["avg_runs"],
            marker_color=["#E76F51","#F4A261","#2A9D8F"],
            yaxis="y1",
        ))
        fig_ph.add_trace(go.Scatter(
            name="Wickets",
            x=ph["phase"], y=ph["wickets"],
            mode="lines+markers",
            marker=dict(size=10, color="#FFD166"),
            line=dict(color="#FFD166", width=2),
            yaxis="y2",
        ))
        fig_ph.update_layout(
            title="Avg Runs per Ball & Wickets by Phase",
            yaxis=dict(title="Avg Runs/Ball", gridcolor="#1E3A5F"),
            yaxis2=dict(title="Wickets", overlaying="y", side="right",
                        gridcolor="#1E3A5F", showgrid=False),
            legend=dict(x=0.01, y=0.99),
        )
        st.plotly_chart(plotly_fig(fig_ph), use_container_width=True)

    # Q8: Venue
    st.markdown("<div class='sub-title'>Query 8 — Most Matches Hosted by Venue</div>", unsafe_allow_html=True)
    venue = (matches.groupby(["venue","city"]).size()
             .reset_index(name="matches")
             .sort_values("matches", ascending=False)
             .head(8))
    fig_v = px.bar(venue, x="venue", y="matches",
                   color="city",
                   color_discrete_sequence=px.colors.qualitative.Pastel,
                   title="Stadium Hosting Frequency",
                   labels={"matches":"Matches Hosted","venue":"Stadium"})
    fig_v.update_xaxes(tickangle=-20)
    st.plotly_chart(plotly_fig(fig_v), use_container_width=True)

    # Q10: Win margin
    st.markdown("<div class='sub-title'>Query 10 — Win Margin Distribution</div>", unsafe_allow_html=True)
    wm1, wm2 = st.columns(2)
    with wm1:
        runs_wins = matches[matches["win_by_runs"] > 0]["win_by_runs"]
        fig_rm = px.histogram(runs_wins, nbins=15,
                              title="Win by Runs Distribution",
                              labels={"value":"Margin (Runs)","count":"Matches"},
                              color_discrete_sequence=["#F4A261"])
        st.plotly_chart(plotly_fig(fig_rm), use_container_width=True)
    with wm2:
        wkt_wins = matches[matches["win_by_wickets"] > 0]["win_by_wickets"]
        fig_wm = px.histogram(wkt_wins, nbins=9,
                              title="Win by Wickets Distribution",
                              labels={"value":"Margin (Wickets)","count":"Matches"},
                              color_discrete_sequence=["#2A9D8F"])
        st.plotly_chart(plotly_fig(fig_wm), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — FULL DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-title'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E;'>All 3 MapReduce jobs + Hive query results in one unified view.</p>", unsafe_allow_html=True)

    # Row 1: Wins + Toss
    d1, d2 = st.columns([2, 1])
    with d1:
        tw = (matches[matches["winner"] != ""]
              .groupby("winner").size()
              .reset_index(name="wins")
              .sort_values("wins", ascending=False))
        colors_d = [TEAM_COLORS.get(t, "#457B9D") for t in tw["winner"]]
        fig_d1 = go.Figure(go.Bar(
            x=tw["winner"], y=tw["wins"], marker_color=colors_d,
            text=tw["wins"], textposition="outside",
            textfont=dict(color="#F0F6FC"),
        ))
        fig_d1.update_layout(title="MR Job 1 — Total Wins per Team", xaxis_tickangle=-15)
        st.plotly_chart(plotly_fig(fig_d1), use_container_width=True)

    with d2:
        tw_w = int((matches["toss_winner"] == matches["winner"]).sum())
        tw_l = len(matches) - tw_w
        fig_d2 = go.Figure(go.Pie(
            labels=["Toss Win\n→ Match Win","Toss Win\n→ Match Loss"],
            values=[tw_w, tw_l], hole=0.55,
            marker=dict(colors=["#2A9D8F","#E76F51"],
                        line=dict(color="#0A0E17",width=3)),
        ))
        fig_d2.update_layout(title="MR Job 2 — Toss Impact")
        st.plotly_chart(plotly_fig(fig_d2), use_container_width=True)

    # Row 2: Top batsmen + phase
    d3, d4 = st.columns([1, 1])
    with d3:
        tb = (deliveries.groupby("batsman")["batsman_runs"]
              .sum().reset_index(name="runs")
              .sort_values("runs").tail(10))
        fig_d3 = px.bar(tb, x="runs", y="batsman", orientation="h",
                        color="runs",
                        color_continuous_scale=["#1E3A5F","#FFD166"],
                        title="MR Job 3 — Top Run-Scorers",
                        labels={"runs":"Runs","batsman":"Player"})
        fig_d3.update_coloraxes(showscale=False)
        st.plotly_chart(plotly_fig(fig_d3), use_container_width=True)

    with d4:
        ph2 = deliveries.groupby("phase")["total_runs"].mean().reset_index()
        fig_d4 = px.bar(ph2, x="phase", y="total_runs",
                        color="phase",
                        color_discrete_sequence=["#E76F51","#F4A261","#2A9D8F"],
                        title="Hive Q9 — Avg Runs by Game Phase",
                        labels={"total_runs":"Avg Runs/Ball","phase":"Phase"})
        st.plotly_chart(plotly_fig(fig_d4), use_container_width=True)

    # Row 3: Season-wise stacked
    sw2 = (matches[matches["winner"] != ""]
           .groupby(["season","winner"]).size()
           .reset_index(name="wins"))
    fig_d5 = px.bar(sw2, x="season", y="wins", color="winner",
                    barmode="stack",
                    color_discrete_map=TEAM_COLORS,
                    title="Hive Q2 — Season-wise Win Distribution",
                    labels={"wins":"Wins","season":"Season","winner":"Team"})
    st.plotly_chart(plotly_fig(fig_d5), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DATASET EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-title'>HDFS Dataset Explorer</div>", unsafe_allow_html=True)

    e1, e2 = st.tabs(["  matches.csv  ", "  deliveries.csv  "])

    with e1:
        st.markdown(f"<span class='badge'>HDFS Path: /ipl/input/matches/matches.csv</span> <span class='badge badge-green'>{len(matches):,} rows</span> <span class='badge badge-blue'>13 columns</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col_filter = st.multiselect("Filter by Team", sorted(matches["team1"].unique()),
                                     default=[], key="match_team_filter")
        display_m = matches if not col_filter else matches[
            matches["team1"].isin(col_filter) | matches["team2"].isin(col_filter)]
        st.dataframe(display_m.style.background_gradient(
            subset=["win_by_runs","win_by_wickets"],
            cmap="YlOrRd"), use_container_width=True, height=400)

        m_stats = matches.describe().round(2)
        st.markdown("<div class='sub-title' style='margin-top:1rem;'>Descriptive Statistics</div>", unsafe_allow_html=True)
        st.dataframe(m_stats, use_container_width=True)

    with e2:
        st.markdown(f"<span class='badge'>HDFS Path: /ipl/input/deliveries/deliveries.csv</span> <span class='badge badge-green'>{len(deliveries):,} rows</span> <span class='badge badge-blue'>14 columns</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        over_filter = st.slider("Filter by Over", 1, 20, (1, 20), key="over_filter")
        display_d = deliveries[deliveries["over"].between(*over_filter)]
        st.dataframe(display_d.head(500), use_container_width=True, height=400)

        st.markdown("<div class='sub-title' style='margin-top:1rem;'>Delivery Stats</div>", unsafe_allow_html=True)
        st.dataframe(deliveries[["batsman_runs","extras","total_runs","is_wicket"]].describe().round(3),
                     use_container_width=True)
