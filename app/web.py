from flask import Flask, render_template, request
from db import init_db, get_conn
import json
import os
import time

app = Flask(__name__)
MIN_DOWNLOAD = float(os.getenv("MIN_DOWNLOAD", 0))
os.environ['TZ'] = 'Europe/Warsaw'
time.tzset()

@app.route("/")
def index():
    range_param = request.args.get("range", "24h")

    if range_param == "7d":
        limit = 7 * 48
        title = "Ostatnie 7 dni"
    else:
        limit = 48
        title = "Ostatnie 24 godziny"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT timestamp, download, upload, ping
        FROM speedtests
        ORDER BY timestamp DESC
        LIMIT {limit}
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        # brak danych – renderujemy pusty widok
        return render_template(
            "index.html",
            rows=[],
            title=title,
            range=range_param,
            min_download=MIN_DOWNLOAD,
            labels="[]",
            downloads="[]",
            uploads="[]",
            pings="[]",
            stats=None
        )

    chart_rows = rows[::-1]

    labels = [r[0] for r in chart_rows]
    downloads = [r[1] for r in chart_rows]
    uploads = [r[2] for r in chart_rows]
    pings = [r[3] for r in chart_rows]

    stats = {
        "download_min": min(downloads),
        "download_avg": sum(downloads) / len(downloads),
        "download_max": max(downloads),
    }

    return render_template(
        "index.html",
        rows=rows,
        title=title,
        range=range_param,
        min_download=MIN_DOWNLOAD,
        labels=json.dumps(labels),
        downloads=json.dumps(downloads),
        uploads=json.dumps(uploads),
        pings=json.dumps(pings),
        stats=stats
    )

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
