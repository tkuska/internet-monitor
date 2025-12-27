import subprocess
import json
import os
import time
from db import init_db, get_conn
from alert import send_alert
from config import MINIMAL_SPEED

os.environ['TZ'] = 'Europe/Warsaw'
time.tzset()

def run_speedtest():
    result = subprocess.run(
        [
            "/usr/bin/speedtest",
            "--accept-license",
            "--accept-gdpr",
            "--format=json"
        ],
        capture_output=True,
        text=True,
        timeout=120
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    data = json.loads(result.stdout)
    if "download" not in data:
        raise ValueError("Invalid speedtest output")

    download_mbps = round(data["download"]["bandwidth"] * 8 / 1_000_000, 2)
    upload_mbps   = round(data["upload"]["bandwidth"] * 8 / 1_000_000, 2)
    ping_ms       = round(data["ping"]["latency"], 2)

    return download_mbps, upload_mbps, ping_ms

def save(download, upload, ping):
    conn = get_conn()
    cur = conn.cursor()

    connection = get_connection_type()


    cur.execute(
        """
        INSERT INTO speedtests (download, upload, ping, connection)
        VALUES (?, ?, ?, ?)
        """,
        (download, upload, ping, connection)
    )
    conn.commit()
    conn.close()

def get_connection_type():
    try:
        result = subprocess.run(
            ["ip", "route", "get", "8.8.8.8"],
            capture_output=True,
            text=True
        )
        output = result.stdout

        if "dev wlan0" in output:
            return "wifi"
        if "dev eth0" in output:
            return "ethernet"

        return "unknown"
    except Exception:
        return "unknown"

if __name__ == "__main__":
    init_db()
    download, upload, ping = run_speedtest()
    save(download, upload, ping)

    if download < MINIMAL_SPEED:
        send_alert(download, upload, ping)
    if upload < MINIMAL_SPEED:
        send_alert(download, upload, ping)

    print(f"OK ↓{download:.2f} ↑{upload:.2f} ping {ping}")
