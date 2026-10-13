"""
app.py
------
Football Player Performance Analytics Dashboard
Built with Streamlit + Plotly.

DISCLAIMER: All data is synthetic and generated for demonstration purposes only.
            It does not represent real-world football statistics.

Run:
    streamlit run app.py
"""

import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Page config — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
BG          = "#0a0d14"
SURFACE     = "#131720"
SURFACE_2   = "#1a2030"
BORDER      = "#1f3a28"
ACCENT      = "#00e676"        # primary green
ACCENT_DIM  = "#00a854"
ACCENT_GLOW = "rgba(0,230,118,0.18)"
PURPLE      = "#bb86fc"
BLUE        = "#4fc3f7"
AMBER       = "#ffd54f"
PINK        = "#f48fb1"
TEXT        = "#e8eaf0"
TEXT_MUTED  = "#6b7385"

GREEN_SEQ   = ["#003d1f", "#006633", "#009946", "#00cc5c", "#00e676"]
POSITION_COLORS = {"GK": AMBER, "DEF": BLUE, "MID": PURPLE, "FWD": PINK}
POSITION_ORDER  = ["GK", "DEF", "MID", "FWD"]
RADAR_COLORS    = [ACCENT, PURPLE, BLUE]

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = f"""
<style>
/* ── Google Font import ───────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global reset ─────────────────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body, .stApp {{
    background-color: {BG} !important;
    color: {TEXT};
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-size: 14px;
    line-height: 1.55;
}}

/* ── Hide Streamlit chrome ────────────────────────────────────────── */
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

/* ── Custom scrollbar ─────────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {ACCENT_DIM}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {ACCENT}; }}

/* ── Main content area padding ────────────────────────────────────── */
.block-container {{
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 1400px;
}}

/* ── Hero banner ──────────────────────────────────────────────────── */
.hero-banner {{
    background: linear-gradient(135deg, {SURFACE_2} 0%, #0d1f15 100%);
    border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT};
    border-radius: 10px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
}}
.hero-title {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {ACCENT};
    margin: 0;
    letter-spacing: -0.02em;
}}
.hero-sub {{
    font-size: 0.82rem;
    color: {TEXT_MUTED};
    margin: 0.25rem 0 0 0;
}}
.hero-icon {{
    font-size: 2.8rem;
    line-height: 1;
}}

/* ── Disclaimer banner ────────────────────────────────────────────── */
.disclaimer {{
    background: rgba(255,213,79,0.08);
    border: 1px solid rgba(255,213,79,0.3);
    border-radius: 7px;
    padding: 0.55rem 1rem;
    font-size: 0.78rem;
    color: #ffe082;
    margin-bottom: 1.2rem;
}}

/* ── Section header cards ─────────────────────────────────────────── */
.section-header {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 3px solid {ACCENT};
    border-radius: 7px;
    padding: 0.55rem 1rem;
    margin: 1.4rem 0 0.8rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: {TEXT};
    letter-spacing: 0.01em;
}}

/* ── KPI metric cards ─────────────────────────────────────────────── */
[data-testid="stMetric"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1.1rem 1rem 0.9rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}}
[data-testid="stMetric"]:hover {{
    border-color: {ACCENT};
    box-shadow: 0 0 18px {ACCENT_GLOW};
}}
[data-testid="stMetric"]::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, {ACCENT_DIM}, {ACCENT});
    border-radius: 10px 10px 0 0;
}}
[data-testid="stMetricLabel"] > div {{
    color: {TEXT_MUTED} !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
[data-testid="stMetricValue"] > div {{
    color: {ACCENT} !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}}
[data-testid="stMetricDelta"] {{
    display: none;
}}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] > div {{
    padding: 0;
}}

/* Sidebar logo block */
.sidebar-logo {{
    background: linear-gradient(135deg, #0d1f15, {SURFACE_2});
    border-bottom: 1px solid {BORDER};
    padding: 1.2rem 1.2rem 1rem;
    margin-bottom: 0.5rem;
    text-align: center;
}}
.sidebar-logo-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {ACCENT};
    margin: 0.4rem 0 0.15rem;
    letter-spacing: 0.02em;
}}
.sidebar-logo-sub {{
    font-size: 0.7rem;
    color: {TEXT_MUTED};
    margin: 0;
}}

/* Sidebar section labels */
.sidebar-section {{
    font-size: 0.68rem;
    font-weight: 600;
    color: {ACCENT_DIM};
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 0.6rem 1.2rem 0.2rem;
    margin-top: 0.4rem;
}}

/* Sidebar filter widgets */
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSelectbox label {{
    color: {TEXT} !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] {{
    background-color: {SURFACE_2} !important;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background-color: {ACCENT_DIM} !important;
    color: #000 !important;
    border-radius: 4px !important;
    font-size: 0.72rem !important;
}}

/* Sidebar active-filter counter */
.filter-stats {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 6px;
    margin: 0.6rem 1rem;
    padding: 0.55rem 0.85rem;
    font-size: 0.75rem;
    color: {TEXT_MUTED};
    display: flex;
    justify-content: space-between;
}}
.filter-stats span {{
    color: {ACCENT};
    font-weight: 600;
}}

/* ── Tab bar ──────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 3px;
    gap: 2px;
    margin-bottom: 1.2rem;
}}
[data-testid="stTabs"] button[role="tab"] {{
    background: transparent !important;
    color: {TEXT_MUTED} !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 0.45rem 1rem !important;
    border: none !important;
    transition: background 0.15s, color 0.15s;
}}
[data-testid="stTabs"] button[role="tab"]:hover {{
    color: {TEXT} !important;
    background: {SURFACE_2} !important;
}}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
    background: {SURFACE_2} !important;
    color: {ACCENT} !important;
    font-weight: 600 !important;
    box-shadow: 0 0 0 1px {BORDER};
}}

/* ── Plotly chart wrapper ──────────────────────────────────────────── */
[data-testid="stPlotlyChart"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 0.25rem;
    overflow: hidden;
}}

/* ── Dataframe ────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {{
    background: {SURFACE};
    border: 1px solid {BORDER} !important;
    border-radius: 8px;
    overflow: hidden;
}}
[data-testid="stDataFrame"] th {{
    background: {SURFACE_2} !important;
    color: {TEXT_MUTED} !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}}
[data-testid="stDataFrame"] td {{
    font-size: 0.82rem !important;
}}

/* ── Download button ──────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {{
    background: linear-gradient(135deg, {ACCENT_DIM}, {ACCENT}) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    border-radius: 7px !important;
    border: none !important;
    width: 100% !important;
    padding: 0.55rem 1rem !important;
    letter-spacing: 0.02em;
    transition: opacity 0.15s;
}}
[data-testid="stDownloadButton"] > button:hover {{
    opacity: 0.88 !important;
}}

/* ── Multiselect (main area) ──────────────────────────────────────── */
[data-baseweb="select"] [data-baseweb="tag"] {{
    background-color: {ACCENT_DIM} !important;
    color: #000 !important;
    border-radius: 4px !important;
}}

/* ── Alert / info banners ─────────────────────────────────────────── */
[data-testid="stAlert"] {{
    border-radius: 7px;
    font-size: 0.82rem;
}}

/* ── Horizontal rule ──────────────────────────────────────────────── */
hr {{
    border: none;
    border-top: 1px solid {BORDER};
    margin: 1rem 0;
}}

/* ── Headings (fallback) ─────────────────────────────────────────── */
h1 {{ color: {ACCENT}  !important; font-weight: 700; letter-spacing:-0.02em; }}
h2 {{ color: {TEXT}    !important; font-weight: 600; }}
h3 {{ color: {TEXT}    !important; font-weight: 600; font-size: 0.95rem; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Plotly base layout (applied to every figure)
# ---------------------------------------------------------------------------
_PLOTLY_BASE = dict(
    paper_bgcolor=SURFACE,
    plot_bgcolor=SURFACE_2,
    font=dict(color=TEXT, family="Inter, Segoe UI, sans-serif", size=12),
    margin=dict(l=50, r=20, t=55, b=45),
    xaxis=dict(
        gridcolor="#1e2535", zerolinecolor="#1e2535",
        tickfont=dict(size=11), title_font=dict(size=12),
    ),
    yaxis=dict(
        gridcolor="#1e2535", zerolinecolor="#1e2535",
        tickfont=dict(size=11), title_font=dict(size=12),
    ),
    legend=dict(
        bgcolor=SURFACE_2, bordercolor=BORDER, borderwidth=1,
        font=dict(size=11), orientation="h",
        yanchor="bottom", y=1.02, xanchor="right", x=1,
    ),
    hoverlabel=dict(
        bgcolor=SURFACE_2, bordercolor=BORDER,
        font=dict(color=TEXT, size=12),
    ),
    title_font=dict(size=13, color=TEXT),
    title_x=0.0,
    title_pad=dict(l=4, b=8),
)


def apply_layout(fig, title: str = "", height: int = 380) -> go.Figure:
    """Apply the standard dark theme + optional title to any Plotly figure."""
    layout = dict(**_PLOTLY_BASE, height=height)
    if title:
        layout["title"] = dict(text=title, font=dict(size=13, color=TEXT), x=0, pad=dict(l=4, b=8))
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def section(label: str) -> None:
    """Render a styled section-header card."""
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Required columns
# ---------------------------------------------------------------------------
REQUIRED_COLUMNS = {
    "player_id", "player_name", "team", "position", "season", "age",
    "nationality", "appearances", "minutes_played", "goals", "assists",
    "shots", "shots_on_target", "pass_accuracy", "key_passes", "tackles",
    "interceptions", "yellow_cards", "red_cards", "clean_sheets", "saves", "rating",
}


# ---------------------------------------------------------------------------
# Data loader
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading player data…")
def load_data() -> pd.DataFrame:
    csv_path = "football_players.csv"
    if not os.path.exists(csv_path):
        try:
            import data_generator
            df = data_generator.generate_dataset()
            df.to_csv(csv_path, index=False)
        except Exception as exc:
            st.error(f"Could not generate dataset: {exc}")
            st.stop()

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        st.error(f"Failed to read '{csv_path}': {exc}")
        st.stop()

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        st.error(
            f"Dataset is missing required columns: {sorted(missing)}. "
            "Delete 'football_players.csv' and restart to regenerate."
        )
        st.stop()

    df["season"] = df["season"].astype(str)
    df["position"] = pd.Categorical(df["position"], categories=POSITION_ORDER, ordered=True)
    return df


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
df_all = load_data()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    # Logo / brand block
    st.markdown(
        f"""
        <div class="sidebar-logo">
            <div style="font-size:2.2rem;">⚽</div>
            <div class="sidebar-logo-title">Football Analytics</div>
            <div class="sidebar-logo-sub">Performance Dashboard</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">Filters</div>', unsafe_allow_html=True)

    all_seasons = sorted(df_all["season"].unique())
    sel_seasons = st.multiselect("Season", options=all_seasons, default=all_seasons)

    all_teams = sorted(df_all["team"].unique())
    sel_teams = st.multiselect("Team", options=all_teams, default=all_teams)

    sel_positions = st.multiselect(
        "Position",
        options=POSITION_ORDER,
        default=POSITION_ORDER,
        help="GK · DEF · MID · FWD",
    )

    # Pre-filter so the Player dropdown only shows relevant names
    pre_filtered = df_all[
        df_all["season"].isin(sel_seasons) &
        df_all["team"].isin(sel_teams) &
        df_all["position"].isin(sel_positions)
    ]

    all_players = sorted(pre_filtered["player_name"].unique())
    sel_players = st.multiselect(
        "Player",
        options=all_players,
        default=[],
        placeholder="All players",
        help="Leave blank to include all",
    )

    # Active-filter summary pill
    n_rows = len(pre_filtered)
    n_players = pre_filtered["player_name"].nunique()
    st.markdown(
        f"""
        <div class="filter-stats">
            <span>Rows</span><span>{n_rows:,}</span>
        </div>
        <div class="filter-stats" style="margin-top:4px;">
            <span>Players</span><span>{n_players:,}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">Export</div>', unsafe_allow_html=True)
    csv_bytes = pre_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇  Download Filtered CSV",
        data=csv_bytes,
        file_name="football_players_filtered.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------------------------
# Final filter
# ---------------------------------------------------------------------------
filtered_df = pre_filtered.copy()
if sel_players:
    filtered_df = filtered_df[filtered_df["player_name"].isin(sel_players)]

if filtered_df.empty:
    st.warning("No data matches the current filters. Please broaden your selections in the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-banner">
        <div class="hero-icon">⚽</div>
        <div>
            <p class="hero-title">Football Player Performance Analytics</p>
            <p class="hero-sub">
                Interactive analytics across {filtered_df["player_name"].nunique():,} players ·
                {filtered_df["team"].nunique()} teams ·
                {filtered_df["season"].nunique()} season(s)
            </p>
        </div>
    </div>
    <div class="disclaimer">
        ⚠️ <strong>Synthetic data only.</strong>
        All statistics are artificially generated for portfolio demonstration purposes and
        do <em>not</em> represent real-world football players, clubs, or results.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_players, tab_teams, tab_positions = st.tabs([
    "📊  Overview",
    "👤  Player Analysis",
    "🏟  Team Analysis",
    "📐  Position Analysis",
])


# ===========================================================================
# TAB 1 — OVERVIEW
# ===========================================================================
with tab_overview:

    # ── KPI row ──────────────────────────────────────────────────────────
    total_players = filtered_df["player_name"].nunique()
    total_goals   = int(filtered_df["goals"].sum())
    total_assists = int(filtered_df["assists"].sum())
    total_minutes = int(filtered_df["minutes_played"].sum())
    avg_rating    = round(float(filtered_df["rating"].mean()), 2)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("👥  Total Players",        f"{total_players:,}")
    k2.metric("⚽  Total Goals",          f"{total_goals:,}")
    k3.metric("🎯  Total Assists",        f"{total_assists:,}")
    k4.metric("⏱  Minutes Played",       f"{total_minutes:,}")
    k5.metric("⭐  Avg Player Rating",    f"{avg_rating}")

    # ── Top-10 charts ─────────────────────────────────────────────────────
    section("Top 10 Performers")
    top_scorers   = filtered_df.nlargest(10, "goals")[["player_name", "team", "goals"]].copy()
    top_assisters = filtered_df.nlargest(10, "assists")[["player_name", "team", "assists"]].copy()

    col_l, col_r = st.columns(2)

    with col_l:
        fig_sc = px.bar(
            top_scorers.sort_values("goals"),
            x="goals", y="player_name",
            orientation="h",
            text="goals",
            hover_data={"team": True, "goals": True, "player_name": False},
            color_discrete_sequence=[ACCENT],
            labels={"goals": "Goals", "player_name": ""},
        )
        fig_sc.update_traces(
            textposition="outside",
            textfont=dict(size=11, color=TEXT),
            marker_line_width=0,
        )
        apply_layout(fig_sc, title="🥇  Top 10 Scorers")
        fig_sc.update_layout(yaxis=dict(tickfont=dict(size=11)))
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_r:
        fig_as = px.bar(
            top_assisters.sort_values("assists"),
            x="assists", y="player_name",
            orientation="h",
            text="assists",
            hover_data={"team": True, "assists": True, "player_name": False},
            color_discrete_sequence=[PURPLE],
            labels={"assists": "Assists", "player_name": ""},
        )
        fig_as.update_traces(
            textposition="outside",
            textfont=dict(size=11, color=TEXT),
            marker_line_width=0,
        )
        apply_layout(fig_as, title="🎯  Top 10 Assisters")
        st.plotly_chart(fig_as, use_container_width=True)

    # ── Rating distribution across all positions ──────────────────────────
    section("Rating Distribution")
    fig_hist = px.histogram(
        filtered_df,
        x="rating",
        color="position",
        nbins=30,
        barmode="overlay",
        opacity=0.75,
        color_discrete_map=POSITION_COLORS,
        category_orders={"position": POSITION_ORDER},
        labels={"rating": "Player Rating", "count": "Players", "position": "Position"},
    )
    apply_layout(fig_hist, title="Player Rating Distribution by Position", height=300)
    fig_hist.update_layout(bargap=0.05)
    st.plotly_chart(fig_hist, use_container_width=True)


# ===========================================================================
# TAB 2 — PLAYER ANALYSIS
# ===========================================================================
with tab_players:

    # ── Scatter pair ──────────────────────────────────────────────────────
    section("Attacking Output")
    col_l, col_r = st.columns(2)

    with col_l:
        fig_ga = px.scatter(
            filtered_df,
            x="assists", y="goals",
            color="position",
            color_discrete_map=POSITION_COLORS,
            hover_data={"player_name": True, "team": True, "season": True,
                        "goals": True, "assists": True},
            labels={"assists": "Assists", "goals": "Goals", "position": "Position"},
            category_orders={"position": POSITION_ORDER},
            trendline="ols",
            trendline_color_override=ACCENT,
        )
        fig_ga.update_traces(
            selector=dict(mode="markers"),
            marker=dict(size=7, opacity=0.82, line=dict(width=0.5, color=BG)),
        )
        apply_layout(fig_ga, title="Goals vs Assists")
        st.plotly_chart(fig_ga, use_container_width=True)

    with col_r:
        fig_sg = px.scatter(
            filtered_df,
            x="shots", y="goals",
            color="team",
            size="shots_on_target",
            size_max=18,
            hover_data={"player_name": True, "position": True,
                        "shots_on_target": True, "shots": True},
            labels={"shots": "Shots", "goals": "Goals", "team": "Team"},
        )
        fig_sg.update_traces(marker=dict(opacity=0.78, line=dict(width=0.5, color=BG)))
        apply_layout(fig_sg, title="Shots vs Goals  (size = shots on target)")
        st.plotly_chart(fig_sg, use_container_width=True)

    # ── Radar comparison ──────────────────────────────────────────────────
    section("Player Radar Comparison")

    RADAR_STATS  = ["goals", "assists", "shots_on_target", "pass_accuracy", "tackles", "rating"]
    RADAR_LABELS = ["Goals", "Assists", "SoT", "Pass Acc", "Tackles", "Rating"]

    available_players = sorted(filtered_df["player_name"].unique())
    radar_players = st.multiselect(
        "Select up to 3 players to compare on radar",
        options=available_players,
        default=available_players[:3] if len(available_players) >= 3 else available_players,
        max_selections=3,
        key="radar_select",
    )

    if radar_players:
        radar_agg = (
            filtered_df[filtered_df["player_name"].isin(radar_players)]
            .groupby("player_name")[RADAR_STATS]
            .mean()
            .reset_index()
        )
        col_min   = filtered_df[RADAR_STATS].min()
        col_max   = filtered_df[RADAR_STATS].max()
        col_range = (col_max - col_min).replace(0, 1)

        fig_radar = go.Figure()
        for idx, row in radar_agg.iterrows():
            vals = [(row[s] - col_min[s]) / col_range[s] for s in RADAR_STATS]
            clr  = RADAR_COLORS[idx % len(RADAR_COLORS)]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=RADAR_LABELS + [RADAR_LABELS[0]],
                fill="toself",
                name=row["player_name"],
                line=dict(color=clr, width=2),
                fillcolor=clr + "28",
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "%{theta}: %{r:.2f}<extra></extra>"
                ),
            ))

        fig_radar.update_layout(
            paper_bgcolor=SURFACE,
            polar=dict(
                bgcolor=SURFACE_2,
                radialaxis=dict(
                    visible=True, range=[0, 1],
                    color=TEXT_MUTED, gridcolor="#1e2535",
                    tickfont=dict(size=9), showticklabels=False,
                ),
                angularaxis=dict(
                    color=TEXT, gridcolor="#1e2535",
                    tickfont=dict(size=11),
                ),
            ),
            font=dict(color=TEXT, family="Inter, sans-serif"),
            legend=dict(
                bgcolor=SURFACE_2, bordercolor=BORDER, borderwidth=1,
                font=dict(size=11), orientation="h",
                yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
            ),
            margin=dict(l=70, r=70, t=30, b=60),
            height=420,
            hoverlabel=dict(bgcolor=SURFACE_2, bordercolor=BORDER, font=dict(color=TEXT)),
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("Select at least one player above to display the radar chart.")

    # ── Player statistics table ────────────────────────────────────────────
    section("Player Statistics Table")
    display_cols = [
        "player_name", "team", "position", "season", "age",
        "appearances", "goals", "assists", "shots", "shots_on_target",
        "pass_accuracy", "key_passes", "tackles", "interceptions",
        "yellow_cards", "red_cards", "clean_sheets", "saves", "rating",
    ]
    table_df = (
        filtered_df[display_cols]
        .sort_values("rating", ascending=False)
        .reset_index(drop=True)
    )
    max_goals   = int(table_df["goals"].max())   or 1
    max_assists = int(table_df["assists"].max()) or 1

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        height=420,
        column_config={
            "player_name":   st.column_config.TextColumn("Player", width=140),
            "team":          st.column_config.TextColumn("Team", width=140),
            "position":      st.column_config.TextColumn("Pos", width=55),
            "season":        st.column_config.TextColumn("Season", width=80),
            "age":           st.column_config.NumberColumn("Age", width=55),
            "appearances":   st.column_config.NumberColumn("Apps", width=60),
            "goals":         st.column_config.ProgressColumn(
                                 "Goals", min_value=0, max_value=max_goals, format="%d"),
            "assists":       st.column_config.ProgressColumn(
                                 "Assists", min_value=0, max_value=max_assists, format="%d"),
            "shots":         st.column_config.NumberColumn("Shots", width=65),
            "shots_on_target": st.column_config.NumberColumn("SoT", width=60),
            "pass_accuracy": st.column_config.NumberColumn("Pass %", format="%.1f", width=70),
            "key_passes":    st.column_config.NumberColumn("KP", width=55),
            "tackles":       st.column_config.NumberColumn("Tkl", width=55),
            "interceptions": st.column_config.NumberColumn("Int", width=55),
            "yellow_cards":  st.column_config.NumberColumn("YC", width=50),
            "red_cards":     st.column_config.NumberColumn("RC", width=50),
            "clean_sheets":  st.column_config.NumberColumn("CS", width=50),
            "saves":         st.column_config.NumberColumn("Saves", width=65),
            "rating":        st.column_config.ProgressColumn(
                                 "Rating", min_value=5.0, max_value=9.5, format="%.1f"),
        },
    )


# ===========================================================================
# TAB 3 — TEAM ANALYSIS
# ===========================================================================
with tab_teams:

    team_df = (
        filtered_df
        .groupby("team", as_index=False)
        .agg(goals=("goals", "sum"), assists=("assists", "sum"),
             players=("player_name", "nunique"),
             avg_rating=("rating", "mean"))
        .round({"avg_rating": 2})
    )

    # ── Goals + Assists side by side ──────────────────────────────────────
    section("Offensive Output by Team")
    col_l, col_r = st.columns(2)

    with col_l:
        fig_tg = px.bar(
            team_df.sort_values("goals"),
            x="goals", y="team", orientation="h",
            text="goals",
            color="goals", color_continuous_scale=GREEN_SEQ,
            hover_data={"avg_rating": ":.2f", "players": True},
            labels={"goals": "Goals", "team": "", "avg_rating": "Avg Rating"},
        )
        fig_tg.update_traces(
            textposition="outside", textfont=dict(size=11),
            marker_line_width=0,
        )
        apply_layout(fig_tg, title="Goals by Team")
        fig_tg.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_tg, use_container_width=True)

    with col_r:
        fig_ta = px.bar(
            team_df.sort_values("assists"),
            x="assists", y="team", orientation="h",
            text="assists",
            color="assists",
            color_continuous_scale=["#1a0a2e", "#7c5cd8", PURPLE],
            hover_data={"avg_rating": ":.2f", "players": True},
            labels={"assists": "Assists", "team": "", "avg_rating": "Avg Rating"},
        )
        fig_ta.update_traces(
            textposition="outside", textfont=dict(size=11),
            marker_line_width=0,
        )
        apply_layout(fig_ta, title="Assists by Team")
        fig_ta.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_ta, use_container_width=True)

    # ── Squad size + Avg rating ───────────────────────────────────────────
    section("Squad Composition")
    col_l, col_r = st.columns(2)

    with col_l:
        fig_tp = px.bar(
            team_df.sort_values("players"),
            x="players", y="team", orientation="h",
            text="players",
            color_discrete_sequence=[BLUE],
            labels={"players": "Unique Players", "team": ""},
        )
        fig_tp.update_traces(
            textposition="outside", textfont=dict(size=11),
            marker_line_width=0,
        )
        apply_layout(fig_tp, title="Players per Team")
        st.plotly_chart(fig_tp, use_container_width=True)

    with col_r:
        fig_tr = px.bar(
            team_df.sort_values("avg_rating"),
            x="avg_rating", y="team", orientation="h",
            text="avg_rating",
            color="avg_rating",
            color_continuous_scale=[f"{ACCENT_DIM}44", ACCENT],
            labels={"avg_rating": "Avg Rating", "team": ""},
        )
        fig_tr.update_traces(
            textposition="outside",
            texttemplate="%{x:.2f}",
            textfont=dict(size=11),
            marker_line_width=0,
        )
        apply_layout(fig_tr, title="Average Player Rating by Team")
        fig_tr.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_tr, use_container_width=True)


# ===========================================================================
# TAB 4 — POSITION ANALYSIS
# ===========================================================================
with tab_positions:

    STAT_COLS  = ["goals", "assists", "shots_on_target", "pass_accuracy",
                  "tackles", "interceptions", "key_passes", "rating"]
    GROUP_STATS = ["goals", "assists", "shots_on_target", "pass_accuracy", "tackles", "rating"]

    pos_df = (
        filtered_df
        .groupby("position", as_index=False, observed=True)[STAT_COLS]
        .mean()
        .round(2)
    )
    pos_df["position"] = pd.Categorical(pos_df["position"], categories=POSITION_ORDER, ordered=True)
    pos_df = pos_df.sort_values("position")

    # ── Grouped bar ────────────────────────────────────────────────────────
    section("Average Stats by Position")
    melted = pos_df.melt(
        id_vars="position", value_vars=GROUP_STATS,
        var_name="Stat", value_name="Average",
    )
    fig_pb = px.bar(
        melted,
        x="position", y="Average",
        color="Stat", barmode="group",
        category_orders={"position": POSITION_ORDER},
        color_discrete_sequence=[ACCENT, PURPLE, BLUE, AMBER, PINK, "#80cbc4"],
        labels={"position": "Position", "Average": "Average Value"},
    )
    apply_layout(fig_pb, title="Average Key Stats by Position", height=380)
    fig_pb.update_traces(marker_line_width=0)
    fig_pb.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_pb, use_container_width=True)

    # ── Box + violin side by side ─────────────────────────────────────────
    section("Rating Distribution")
    col_l, col_r = st.columns(2)

    with col_l:
        fig_box = px.box(
            filtered_df,
            x="position", y="rating",
            color="position",
            color_discrete_map=POSITION_COLORS,
            category_orders={"position": POSITION_ORDER},
            points="outliers",
            labels={"position": "Position", "rating": "Rating"},
        )
        apply_layout(fig_box, title="Rating Box Plot by Position")
        fig_box.update_traces(marker=dict(size=4, opacity=0.6))
        st.plotly_chart(fig_box, use_container_width=True)

    with col_r:
        fig_vio = px.violin(
            filtered_df,
            x="position", y="rating",
            color="position",
            color_discrete_map=POSITION_COLORS,
            category_orders={"position": POSITION_ORDER},
            box=True, points=False,
            labels={"position": "Position", "rating": "Rating"},
        )
        apply_layout(fig_vio, title="Rating Violin Plot by Position")
        st.plotly_chart(fig_vio, use_container_width=True)

    # ── Position summary table ─────────────────────────────────────────────
    section("Position Summary  (averages across filtered data)")
    st.dataframe(
        pos_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "position":         st.column_config.TextColumn("Position", width=100),
            "goals":            st.column_config.NumberColumn("Avg Goals",     format="%.2f"),
            "assists":          st.column_config.NumberColumn("Avg Assists",   format="%.2f"),
            "shots_on_target":  st.column_config.NumberColumn("Avg SoT",       format="%.2f"),
            "pass_accuracy":    st.column_config.NumberColumn("Avg Pass %",    format="%.2f"),
            "tackles":          st.column_config.NumberColumn("Avg Tackles",   format="%.2f"),
            "interceptions":    st.column_config.NumberColumn("Avg Interc.",   format="%.2f"),
            "key_passes":       st.column_config.NumberColumn("Avg Key Pass",  format="%.2f"),
            "rating":           st.column_config.ProgressColumn(
                                    "Avg Rating", min_value=5.0, max_value=9.5, format="%.2f"),
        },
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <hr>
    <p style="text-align:center; color:{TEXT_MUTED}; font-size:0.75rem; margin:0.5rem 0 1.5rem;">
        Football Analytics Dashboard &nbsp;·&nbsp; Synthetic data only &nbsp;·&nbsp;
        Built with Streamlit &amp; Plotly
    </p>
    """,
    unsafe_allow_html=True,
)
