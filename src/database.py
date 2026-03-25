"""
database.py - SQL Integration for Traffic Violations
"""
import sqlite3
import pandas as pd
import os


DB_PATH = "../data/traffic_violations.db"


def create_connection():
    """Create and return a SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    print(f"✅ Connected to database: {DB_PATH}")
    return conn


def load_data_to_db(csv_path: str):
    """Load cleaned CSV into SQLite database."""
    print("⏳ Loading data into SQLite...")
    
    df = pd.read_csv(csv_path, low_memory=False)
    
    conn = create_connection()
    
    # ── Main violations table ─────────────────────────────────────
    df.to_sql("violations", conn, if_exists="replace", 
              index=False, chunksize=10000)
    
    print(f"✅ Loaded {len(df):,} rows into 'violations' table")
    
    # ── Create indexes for faster queries ────────────────────────
    cursor = conn.cursor()
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_date      ON violations('Date Of Stop')",
        "CREATE INDEX IF NOT EXISTS idx_violation  ON violations(ViolationCategory)",
        "CREATE INDEX IF NOT EXISTS idx_gender     ON violations(Gender)",
        "CREATE INDEX IF NOT EXISTS idx_race       ON violations(Race)",
        "CREATE INDEX IF NOT EXISTS idx_make       ON violations(Make)",
        "CREATE INDEX IF NOT EXISTS idx_accident   ON violations(Accident)",
        "CREATE INDEX IF NOT EXISTS idx_subagency  ON violations(SubAgency)",
    ]
    
    for idx in indexes:
        cursor.execute(idx)
    
    conn.commit()
    print("✅ Indexes created for fast querying")
    conn.close()
    return True


def run_query(sql: str) -> pd.DataFrame:
    """Run a SQL query and return results as DataFrame."""
    conn = create_connection()
    result = pd.read_sql_query(sql, conn)
    conn.close()
    return result


def get_summary_stats() -> dict:
    """Return key summary statistics via SQL."""
    conn = create_connection()
    
    stats = {}
    
    queries = {
        "total_violations"  : "SELECT COUNT(*) FROM violations",
        "total_accidents"   : "SELECT COUNT(*) FROM violations WHERE Accident = 1",
        "total_fatal"       : "SELECT COUNT(*) FROM violations WHERE Fatal = 1",
        "total_alcohol"     : "SELECT COUNT(*) FROM violations WHERE Alcohol = 1",
        "total_hazmat"      : "SELECT COUNT(*) FROM violations WHERE HAZMAT = 1",
        "unique_locations"  : "SELECT COUNT(DISTINCT Location) FROM violations",
    }
    
    for key, query in queries.items():
        result = conn.execute(query).fetchone()[0]
        stats[key] = result
    
    conn.close()
    return stats