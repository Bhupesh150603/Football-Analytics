# Football Player Performance Analytics Dashboard — Implementation Plan

## Top-Level Overview

Build a portfolio-quality, single-page multi-tab Streamlit dashboard (`app.py`) that lets users
explore and compare synthetic football (soccer) player statistics. All data lives in a local CSV
file (`football_players.csv`). The app ships with a `requirements.txt` and a `README.md`.
Every KPI, ranking, and chart is derived at runtime from the (optionally filtered) DataFrame —
nothing is hard-coded. The UI uses a custom dark, green-pitch theme via Streamlit's config and
inline CSS injected once at startup.

---

## Dataset Schema (`football_players.csv`)

| Column | Type | Description |
|---|---|---|
| `player_id` | int | Unique row identifier (1–N) |
| `player_name` | str | Full name (Firstname Lastname) |
| `team` | str | Club name (8 clubs) |
| `position` | str | GK / DEF / MID / FWD |
| `season` | str | "2021-22", "2022-23", "2023-24" |
| `age` | int | 18–36 |
| `nationality` | str | Country name |
| `appearances` | int | Matches played |
| `minutes_played` | int | Total minutes |
| `goals` | int | Goals scored |
| `assists` | int | Assists |
| `shots` | int | Total shots taken |
| `shots_on_target` | int | Shots on target |
| `pass_accuracy` | float | % (50–95) |
| `key_passes` | int | Passes leading to a shot |
| `tackles` | int | Tackles won |
| `interceptions` | int | Interceptions |
| `yellow_cards` | int | Yellow cards |
| `red_cards` | int | Red cards |
| `clean_sheets` | int | Clean sheets (GK/DEF only, else 0) |
| `saves` | int | Goalkeeper saves (GK only, else 0) |
| `rating` | float | Overall rating 5.0–9.5 |

**Generation rules:**
- `numpy.random.seed(42)` for reproducibility.
- 120 rows: 10 GK, 35 DEF, 40 MID, 35 FWD across three seasons and eight teams.
- Stats are position-aware (e.g. GK have high saves/clean_sheets, FWD have high goals/shots).
- A clearly visible disclaimer banner is shown in the app: *"All data is synthetic and generated
  for demonstration purposes only. It does not represent real-world football statistics."*

---

## KPI Calculations (Overview Page)

| KPI Card | Calculation |
|---|---|
| Total Players | `len(filtered_df['player_name'].unique())` |
| Total Goals | `filtered_df['goals'].sum()` |
| Total Assists | `filtered_df['assists'].sum()` |
| Total Minutes Played | `filtered_df['minutes_played'].sum()` |
| Avg Player Rating | `filtered_df['rating'].mean()` rounded to 2 dp |

All KPIs react to sidebar filters.

---

## Chart Choices

| Page | Chart | Library | Why |
|---|---|---|---|
| Overview | KPI metric cards | Streamlit `st.metric` | Standard, scannable at a glance |
| Overview | Top-10 scorers bar | Plotly Express bar | Ranked comparison |
| Overview | Top-10 assisters bar | Plotly Express bar | Ranked comparison |
| Player Analysis | Goals vs Assists scatter | Plotly Express scatter | Reveals playmaking vs scoring balance |
| Player Analysis | Shots vs Goals scatter | Plotly Express scatter | Shot efficiency / conversion rate |
| Player Analysis | Player radar chart | Plotly Graph Objects | Multi-stat player comparison on same axes |
| Team Analysis | Goals per team bar | Plotly Express bar | Team offensive output |
| Team Analysis | Assists per team bar | Plotly Express bar | Team creative output |
| Team Analysis | Player count per team | Plotly Express bar | Squad size balance |
| Position Analysis | Avg stats by position | Plotly Express grouped bar | Cross-positional comparison |
| Position Analysis | Rating distribution | Plotly Express box | Spread and median rating per position |

All charts use a consistent dark background (`#0e1117`), green accent (`#00ff85`), and white text.
Hover tooltips include player name, team, and the relevant stat values.

---

## Project Structure

```
Football Analysis Dashboard/
├── app.py                  # Main Streamlit application
├── data_generator.py       # Synthetic dataset generator (imported by app.py)
├── football_players.csv    # Pre-generated CSV (created on first run)
├── requirements.txt        # Python dependencies
└── README.md               # Setup, run, and deploy instructions
```

---

## Sub-Tasks

---

### Sub-Task 1 — Generate Synthetic Dataset (`data_generator.py` + `football_players.csv`)

**Intent**
Create a standalone module that generates and saves the reproducible synthetic dataset. Separating
generation from the main app keeps `app.py` clean and allows the CSV to be pre-committed so users
do not need to regenerate it.

**Expected Outcomes**
- `data_generator.py` exists and can be run as a script (`python data_generator.py`).
- `football_players.csv` exists with exactly the columns listed in the schema above and ≥ 120 rows.
- Running the generator twice produces identical output (seeded RNG).
- Position-aware stat distributions are in place (GK: high saves; FWD: high goals; etc.).

**Todo List**
1. Create `data_generator.py` with `generate_dataset()` function and `if __name__ == "__main__"` block.
2. Define team names list (8 clubs), position distribution (10/35/40/35), season list, nationality pool.
3. Use `numpy.random.seed(42)` before all random calls.
4. Generate each column using position-conditional `np.random.randint` / `np.random.uniform` ranges.
5. Assemble into a `pandas.DataFrame`, assign `player_id` (1–N).
6. Save to `football_players.csv` with `index=False`.
7. Verify output: print shape and `df.head()` when run as script.

**Relevant Context**
- No external data source; pure NumPy + Pandas.
- Consumed in `app.py` via `import data_generator` (called only if CSV is missing).

**Status:** `[x] done`

---

### Sub-Task 2 — Core App Shell (`app.py` — layout, config, theme, sidebar)

**Intent**
Set up the Streamlit app skeleton: page config, custom CSS for the dark/green theme, the sidebar
filter widgets, and the CSV data loader. All subsequent pages are built on top of this shell.

**Expected Outcomes**
- `streamlit run app.py` launches without errors on a clean install.
- Dark background with green accent is visible; custom font styling applied.
- Sidebar shows Season, Team, Position, and Player multi-select filters.
- Filtered DataFrame is available as a Python variable for all page modules.
- A synthetic-data disclaimer banner renders at the top of every page.
- CSV download button in the sidebar exports the current filtered data.

**Todo List**
1. Set `st.set_page_config(layout="wide", page_title="Football Analytics", page_icon="⚽")`.
2. Inject custom CSS via `st.markdown("""<style>…</style>""", unsafe_allow_html=True)` — dark bg, green accents, card styling.
3. Write `load_data()` function: load CSV; if missing, call `data_generator.generate_dataset()` then reload.
4. Add input validation: if CSV loads with unexpected columns, show `st.error` and `st.stop()`.
5. Build sidebar: Season multi-select, Team multi-select, Position multi-select, Player multi-select.
6. Apply filters to produce `filtered_df`; if result is empty, show `st.warning` and `st.stop()`.
7. Add CSV download button using `st.download_button` with `filtered_df.to_csv(index=False)`.
8. Add disclaimer banner using `st.info`.
9. Add top-level tab navigation: Overview | Player Analysis | Team Analysis | Position Analysis.

**Relevant Context**
- Streamlit tab navigation: `tab1, tab2, tab3, tab4 = st.tabs([…])`.
- CSS targets `.stApp`, `.stMetric`, `.stSidebar` to avoid breaking Streamlit internals.

**Status:** `[ ] pending`

---

### Sub-Task 3 — Overview Page (KPI Cards + Top Scorers/Assisters)

**Intent**
Implement the first tab: five KPI metric cards and two ranked bar charts showing the top 10 scorers
and top 10 assisters from the filtered data.

**Expected Outcomes**
- Five `st.metric` cards render in a single row: Total Players, Total Goals, Total Assists,
  Total Minutes Played, Avg Rating.
- Top-10 Scorers horizontal bar chart is visible with player name on Y-axis, goals on X-axis.
- Top-10 Assisters horizontal bar chart is visible with the same layout.
- All values update instantly when sidebar filters change.

**Todo List**
1. Inside the Overview tab, create five `st.columns(5)` and place one `st.metric` in each.
2. Compute each KPI from `filtered_df` (see KPI Calculations table above).
3. Build Top-10 Scorers: `filtered_df.nlargest(10, 'goals')` → `px.bar(orientation='h')`.
4. Build Top-10 Assisters: `filtered_df.nlargest(10, 'assists')` → `px.bar(orientation='h')`.
5. Apply consistent chart theme (dark bg, green bars, white axis labels).
6. Use `st.columns(2)` to place both bar charts side by side.
7. Add `st.plotly_chart(use_container_width=True)` for responsive sizing.

**Relevant Context**
- `filtered_df` is computed in Sub-Task 2 and passed into this tab's block.
- Chart color: `color_discrete_sequence=["#00ff85"]`.

**Status:** `[ ] pending`

---

### Sub-Task 4 — Player Analysis Page (Scatter Plots + Radar Chart)

**Intent**
Implement the second tab with three interactive charts: Goals vs Assists scatter, Shots vs Goals
scatter, and a radar comparison chart for up to three selected players.

**Expected Outcomes**
- Goals vs Assists scatter: each dot is a player, colored by position, tooltip shows name and team.
- Shots vs Goals scatter: each dot colored by team, size scaled to `shots_on_target`.
- Radar chart: user selects 1–3 players from a selectbox; radar overlays their stats on the same axes.
- Searchable player statistics table below the charts.

**Todo List**
1. Goals vs Assists: `px.scatter(filtered_df, x='assists', y='goals', color='position', hover_data=['player_name','team'])`.
2. Shots vs Goals: `px.scatter(filtered_df, x='shots', y='goals', color='team', size='shots_on_target', hover_data=['player_name'])`.
3. Radar chart: define axes = `['goals','assists','shots_on_target','pass_accuracy','tackles','rating']`.
4. Normalize each axis to 0–1 range across `filtered_df` before plotting so all metrics are comparable.
5. Use `go.Scatterpolar` traces, one per selected player, with `fill='toself'`.
6. Add a `st.multiselect` (max 3 players) above the radar chart for player selection.
7. Searchable table: `st.dataframe(filtered_df[display_cols].sort_values('rating', ascending=False))`.
8. Apply consistent dark chart theme across all three charts.

**Relevant Context**
- Radar normalization: `(val - col_min) / (col_max - col_min)` per column.
- `go.Figure(layout=go.Layout(polar=dict(bgcolor="#1a1a2e"), paper_bgcolor="#0e1117"))`.

**Status:** `[ ] pending`

---

### Sub-Task 5 — Team Analysis Page

**Intent**
Implement the third tab with team-level aggregated bar charts for goals, assists, and player count.

**Expected Outcomes**
- Three bar charts rendered in a 2+1 layout: Goals by Team, Assists by Team, Players per Team.
- All charts react to the season and position sidebar filters (team filter intentionally left wide
  so users can still compare teams).

**Todo List**
1. Aggregate: `team_df = filtered_df.groupby('team').agg(goals=('goals','sum'), assists=('assists','sum'), players=('player_name','nunique')).reset_index()`.
2. Goals by Team: `px.bar(team_df, x='team', y='goals', color='goals', color_continuous_scale='Greens')`.
3. Assists by Team: same pattern with `y='assists'`.
4. Players per Team: `px.bar(team_df, x='team', y='players')` with flat green color.
5. Sort all charts by descending value for readability.
6. Layout: `st.columns(2)` for goals + assists; full-width for player count.

**Relevant Context**
- Grouped aggregation via `pandas.DataFrame.groupby().agg()`.
- Color continuous scale gives a heatmap feel without a separate library.

**Status:** `[ ] pending`

---

### Sub-Task 6 — Position Analysis Page

**Intent**
Implement the fourth tab comparing average statistics and rating distributions across the four
positions (GK, DEF, MID, FWD).

**Expected Outcomes**
- Grouped bar chart showing average goals, assists, pass_accuracy, tackles, rating by position.
- Box plot showing rating distribution per position.
- A position-summary stat table (average values per position) rendered below the charts.

**Todo List**
1. Aggregate: `pos_df = filtered_df.groupby('position')[stat_cols].mean().reset_index()`.
2. Melt `pos_df` to long format for grouped bar: `pd.melt(pos_df, id_vars='position', value_vars=[…])`.
3. Grouped bar: `px.bar(melted, x='position', y='value', color='variable', barmode='group')`.
4. Box plot: `px.box(filtered_df, x='position', y='rating', color='position')`.
5. Position order on X-axis: `["GK","DEF","MID","FWD"]`.
6. Render stat table with `st.dataframe(pos_df.round(2))`.

**Relevant Context**
- `pd.melt` long-format transformation is required by Plotly Express grouped bars.
- Position ordering: pass `category_orders={"position": ["GK","DEF","MID","FWD"]}` to `px`.

**Status:** `[ ] pending`

---

### Sub-Task 7 — `requirements.txt` and `README.md`

**Intent**
Provide the exact dependency list and clear documentation so any developer can run or deploy the
project in under five minutes.

**Expected Outcomes**
- `requirements.txt` lists pinned or minimum-version packages needed.
- `README.md` includes: project description, dataset disclaimer, setup steps (venv + pip install),
  local run command, Streamlit Community Cloud deploy instructions, and project structure tree.

**Todo List**
1. Create `requirements.txt` with: `streamlit`, `pandas`, `numpy`, `plotly`.
2. Create `README.md` with sections: Overview, Disclaimer, Project Structure, Setup & Run, Deploy,
   Features, Screenshots placeholder.
3. Include exact commands: `python -m venv venv`, `pip install -r requirements.txt`,
   `streamlit run app.py`.
4. Include Streamlit Community Cloud deployment steps (GitHub push + connect repo).

**Relevant Context**
- No other third-party dependencies are required.
- Streamlit Community Cloud requires a public GitHub repo and a `requirements.txt` in the root.

**Status:** `[ ] pending`

---

## Implementation Order

```
Sub-Task 1  →  Sub-Task 2  →  Sub-Task 3  →  Sub-Task 4  →  Sub-Task 5  →  Sub-Task 6  →  Sub-Task 7
  Dataset       App Shell       Overview       Player         Team          Position       Docs
  Generator                       Page         Analysis       Analysis      Analysis
```

Each sub-task is independent once its predecessor is complete.
