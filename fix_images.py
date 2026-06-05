import sqlite3

conn = sqlite3.connect("backend/data.db")
tools = conn.execute("SELECT id, name, image_url FROM tools").fetchall()

for t in tools:
    old_url = t[2]
    # Fix localhost URLs to production backend
    if old_url and "localhost:8000" in old_url:
        new_url = old_url.replace("http://localhost:8000", "https://backend-six-alpha-77.vercel.app")
        conn.execute("UPDATE tools SET image_url = ? WHERE id = ?", (new_url, t[0]))

conn.commit()

# Verify
tools = conn.execute("SELECT id, name, image_url FROM tools").fetchall()
broken = [t for t in tools if "localhost" in t[2]]
print(f"Total tools: {len(tools)}")
print(f"Still broken: {len(broken)}")
for t in tools[:3]:
    print(f"  {t[0]}: {t[1]} -> {t[2]}")

conn.close()
