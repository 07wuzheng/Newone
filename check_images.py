import sqlite3, os
# Check both locations
for path in ["data.db", "backend/data.db"]:
    if os.path.exists(path):
        print(f"=== {path} ({os.path.getsize(path)} bytes) ===")
        conn = sqlite3.connect(path)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        if 'tools' in [t[0] for t in tables]:
            rows = conn.execute("SELECT id, name, image_url FROM tools").fetchall()
            for r in rows:
                print(f"  {r[0]}: {r[1]} -> {r[2]}")
        conn.close()
