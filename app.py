def init_db():
    conn = sqlite3.connect("pistonrod.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pistonrod (
        sr_no TEXT,
        part_no TEXT,
        rev_date TEXT,
        application TEXT,
        total_length TEXT,
        plating_length TEXT,
        chrome_before TEXT,
        chrome_after TEXT,
        nickel TEXT,
        piston_end TEXT,
        plant TEXT,
        identification TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()