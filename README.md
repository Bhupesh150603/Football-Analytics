# ⚽ Football Player Performance Analytics Dashboard

A portfolio-quality interactive football (soccer) analytics dashboard built with **Python**, **Streamlit**, and **Plotly**.

> **Data Disclaimer:** All statistics are **synthetic** and generated with a seeded random number generator for demonstration purposes only. They do **not** represent real-world football players, clubs, or results.

---

## Features

| Page | Contents |
|---|---|
| 📊 **Overview** | KPI cards (players, goals, assists, minutes, rating) + Top 10 Scorers & Assisters |
| 👤 **Player Analysis** | Goals vs Assists scatter, Shots vs Goals scatter, Radar comparison, Stats table |
| 🏟️ **Team Analysis** | Goals, Assists, and Player count per team |
| 📐 **Position Analysis** | Avg stats grouped bar, Rating box plot, Position summary table |

**Sidebar filters:** Season · Team · Position · Player · CSV download

---

## Project Structure

```
Football Analysis Dashboard/
├── app.py                  # Main Streamlit application
├── data_generator.py       # Synthetic dataset generator
├── football_players.csv    # Pre-generated 360-row CSV (3 seasons × 120 players)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Dataset Schema

120 players × 3 seasons = **360 rows**, 22 columns.

| Column | Type | Description |
|---|---|---|
| `player_id` | int | Unique row ID |
| `player_name` | str | Synthetic full name |
| `team` | str | One of 8 fictional clubs |
| `position` | str | GK / DEF / MID / FWD |
| `season` | str | 2021-22, 2022-23, 2023-24 |
| `age` | int | 18–36 |
| `nationality` | str | 20 nationalities |
| `appearances` | int | Matches played |
| `minutes_played` | int | Total minutes |
| `goals` | int | Goals scored |
| `assists` | int | Assists |
| `shots` | int | Total shots |
| `shots_on_target` | int | Shots on target |
| `pass_accuracy` | float | Pass accuracy % |
| `key_passes` | int | Key passes |
| `tackles` | int | Tackles won |
| `interceptions` | int | Interceptions |
| `yellow_cards` | int | Yellow cards |
| `red_cards` | int | Red cards |
| `clean_sheets` | int | Clean sheets |
| `saves` | int | Goalkeeper saves |
| `rating` | float | Overall rating 5.0–9.5 |

---

## Setup & Run Locally

### 1. Prerequisites
- Python 3.9 or later
- pip

### 2. Clone or download the project

```bash
git clone <your-repo-url>
cd "Football Analysis Dashboard"
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

> **Note:** If `football_players.csv` is missing, the app generates it automatically on first launch.

---

## Deploy to Streamlit Community Cloud (Free)

1. Push this project to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"** → select your repository, branch (`main`), and main file (`app.py`).
4. Click **Deploy** — Streamlit installs dependencies from `requirements.txt` automatically.
5. Your app is live at `https://<your-app>.streamlit.app`.

---

## Regenerate the Dataset

```bash
python data_generator.py
```

This overwrites `football_players.csv` with a fresh reproducible dataset (seed 42).

---

## Screenshots

> *(Add screenshots here after running the app locally.)*

---

## License

MIT — free to use, modify, and distribute.
