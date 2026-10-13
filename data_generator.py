"""
data_generator.py
-----------------
Generates a reproducible synthetic football player dataset.
All statistics are SYNTHETIC and do not represent real-world football results.

Run standalone:
    python data_generator.py
Or import and call:
    from data_generator import generate_dataset
    df = generate_dataset()
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SEED = 42

TEAMS = [
    "FC Meridian",
    "Westgate United",
    "Northbridge City",
    "Southport Athletic",
    "Eastfield Rovers",
    "Capital SC",
    "Lakeside FC",
    "Ironclad Town",
]

SEASONS = ["2021-22", "2022-23", "2023-24"]

NATIONALITIES = [
    "English", "Spanish", "French", "German", "Brazilian",
    "Argentine", "Portuguese", "Italian", "Dutch", "Belgian",
    "Norwegian", "Swedish", "Polish", "Croatian", "Senegalese",
    "Ghanaian", "Nigerian", "Moroccan", "Japanese", "South Korean",
]

# Position distribution: 10 GK, 35 DEF, 40 MID, 35 FWD = 120 rows total
POSITION_COUNTS = {"GK": 10, "DEF": 35, "MID": 40, "FWD": 35}

# First and last name pools for synthetic name generation
FIRST_NAMES = [
    "James", "Oliver", "Luca", "Marco", "Carlos", "Rafael", "Ethan", "Noah",
    "Lucas", "Alex", "David", "Stefan", "Kai", "Leon", "Emil", "Hugo",
    "Mateo", "Diego", "Andre", "Pierre", "Sven", "Tobias", "Arjen", "Jan",
    "Mohamed", "Kwame", "Emeka", "Yuki", "Min-Jun", "Sergio",
]
LAST_NAMES = [
    "Silva", "Müller", "Rossi", "García", "Dupont", "Hansen", "Novak",
    "Costa", "Ferreira", "Hernandez", "Kruse", "Wagner", "Becker", "Klein",
    "Okafor", "Mensah", "Diallo", "Nakamura", "Park", "Torres", "Gomez",
    "Martins", "Nkosi", "Eriksen", "Larsson", "Kovač", "Popović", "Dembélé",
    "Mbeki", "Tanaka",
]


# ---------------------------------------------------------------------------
# Helper: position-aware stat ranges
# ---------------------------------------------------------------------------
def _stat_ranges(position: str) -> dict:
    """Return (low, high) random integer ranges per stat keyed by position."""
    base = {
        "appearances":       (15, 38),
        "goals":             (0,  2),
        "assists":           (0,  3),
        "shots":             (0,  5),
        "shots_on_target":   (0,  3),
        "pass_accuracy":     (55, 75),
        "key_passes":        (0,  10),
        "tackles":           (0,  10),
        "interceptions":     (0,  8),
        "yellow_cards":      (0,  3),
        "red_cards":         (0,  1),
        "clean_sheets":      (0,  1),
        "saves":             (0,  1),
    }
    overrides = {
        "GK": {
            "goals":           (0,  1),
            "assists":         (0,  1),
            "shots":           (0,  2),
            "shots_on_target": (0,  1),
            "pass_accuracy":   (60, 80),
            "tackles":         (0,  5),
            "interceptions":   (0,  5),
            "clean_sheets":    (5, 20),
            "saves":           (30, 120),
        },
        "DEF": {
            "goals":           (0,  5),
            "assists":         (0,  6),
            "shots":           (5, 30),
            "shots_on_target": (2, 15),
            "pass_accuracy":   (65, 88),
            "key_passes":      (5, 30),
            "tackles":         (20, 80),
            "interceptions":   (15, 60),
            "clean_sheets":    (2, 15),
        },
        "MID": {
            "goals":           (1, 12),
            "assists":         (3, 15),
            "shots":           (10, 60),
            "shots_on_target": (5, 30),
            "pass_accuracy":   (70, 93),
            "key_passes":      (20, 80),
            "tackles":         (10, 50),
            "interceptions":   (8, 40),
        },
        "FWD": {
            "goals":           (5, 30),
            "assists":         (2, 12),
            "shots":           (30, 120),
            "shots_on_target": (15, 65),
            "pass_accuracy":   (60, 85),
            "key_passes":      (10, 50),
            "tackles":         (2, 20),
            "interceptions":   (1, 15),
        },
    }
    ranges = {**base, **overrides.get(position, {})}
    return ranges


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------
def generate_dataset() -> pd.DataFrame:
    """
    Generate and return a synthetic football player DataFrame.
    Seeded at SEED=42 for full reproducibility.
    """
    rng = np.random.default_rng(SEED)

    rows = []
    player_id = 1

    for season in SEASONS:
        for position, count in POSITION_COUNTS.items():
            ranges = _stat_ranges(position)

            for _ in range(count):
                first = rng.choice(FIRST_NAMES)
                last  = rng.choice(LAST_NAMES)
                name  = f"{first} {last}"

                appearances = int(rng.integers(*ranges["appearances"]))
                minutes     = int(appearances * rng.integers(60, 95))

                goals           = int(rng.integers(*ranges["goals"]))
                assists         = int(rng.integers(*ranges["assists"]))
                shots           = int(rng.integers(*ranges["shots"]))
                shots_on_target = int(min(rng.integers(*ranges["shots_on_target"]), shots))
                pass_accuracy   = round(float(rng.uniform(*ranges["pass_accuracy"])), 1)
                key_passes      = int(rng.integers(*ranges["key_passes"]))
                tackles         = int(rng.integers(*ranges["tackles"]))
                interceptions   = int(rng.integers(*ranges["interceptions"]))
                yellow_cards    = int(rng.integers(*ranges["yellow_cards"]))
                red_cards       = int(rng.integers(*ranges["red_cards"]))
                clean_sheets    = int(rng.integers(*ranges["clean_sheets"]))
                saves           = int(rng.integers(*ranges["saves"]))

                # Rating: base on a weighted combination of normalised stats
                raw_rating = 5.0 + (goals * 0.12) + (assists * 0.10) + \
                             (pass_accuracy / 100 * 2.5) + (tackles * 0.02) + \
                             float(rng.uniform(0, 0.5))
                rating = round(min(max(raw_rating, 5.0), 9.5), 1)

                rows.append({
                    "player_id":        player_id,
                    "player_name":      name,
                    "team":             rng.choice(TEAMS),
                    "position":         position,
                    "season":           season,
                    "age":              int(rng.integers(18, 37)),
                    "nationality":      rng.choice(NATIONALITIES),
                    "appearances":      appearances,
                    "minutes_played":   minutes,
                    "goals":            goals,
                    "assists":          assists,
                    "shots":            shots,
                    "shots_on_target":  shots_on_target,
                    "pass_accuracy":    pass_accuracy,
                    "key_passes":       key_passes,
                    "tackles":          tackles,
                    "interceptions":    interceptions,
                    "yellow_cards":     yellow_cards,
                    "red_cards":        red_cards,
                    "clean_sheets":     clean_sheets,
                    "saves":            saves,
                    "rating":           rating,
                })
                player_id += 1

    df = pd.DataFrame(rows)
    return df


# ---------------------------------------------------------------------------
# Run standalone
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("football_players.csv", index=False)
    print("[OK] Dataset saved to football_players.csv")
    print(f"    Shape : {df.shape}")
    print(f"    Seasons: {sorted(df['season'].unique())}")
    print(f"    Positions: {df['position'].value_counts().to_dict()}")
    print(df.head(5).to_string(index=False))
