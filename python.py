from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect("devices.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS device_location (
            device_id TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            timestamp INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json
    device_id = data["device_id"]
    lat = data["lat"]
    lng = data["lng"]
    ts = int(time.time())

    conn = sqlite3.connect("devices.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO device_location(device_id, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?)
    """, (device_id, lat, lng, ts))

    conn.commit()
    conn.close()
    return jsonify({"status": "location updated"})

@app.route("/get_location/<device_id>", methods=["GET"])
def get_location(device_id):
    conn = sqlite3.connect("devices.db")
    cur = conn.cursor()
    cur.execute("SELECT latitude, longitude, timestamp FROM device_location WHERE device_id=?", (device_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({
            "device_id": device_id,
            "latitude": row[0],
            "longitude": row[1],
            "last_seen": row[2]
        })
    else:
        return jsonify({"error": "device not found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
