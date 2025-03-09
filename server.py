from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import os

app = FastAPI()
index_file_path = "index.html"

@app.get("/", response_class=HTMLResponse)
def serve_index():
    if os.path.exists(index_file_path):
        with open(index_file_path, "r") as file:
            return HTMLResponse(content=file.read())
    return {"error": "index.html file not found"}

# Serve static files under the "/static" path
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

# MQTT Setup using WebSockets
MQTT_BROKER = "ws://157.173.101.159:9001"  # WebSocket connection
TOPICS = ["/work_group_01/room_temp/temperature", "/work_group_01/room_temp/humidity"]

latest_data = {"temperature": None, "humidity": None}

def execute_query(query, params=(), fetch=False):
    with sqlite3.connect("weather.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if fetch:
            return cursor.fetchall()
        return []

def on_message(client, userdata, msg):
    global latest_data
    payload = msg.payload.decode("utf-8")
    print(f"Received {msg.topic}: {payload}")

    if "temperature" in msg.topic:
        latest_data["temperature"] = float(payload)
    elif "humidity" in msg.topic:
        latest_data["humidity"] = float(payload)

    if latest_data["temperature"] is not None and latest_data["humidity"] is not None:
        execute_query("INSERT INTO weather (temperature, humidity) VALUES (?, ?)",
                      (latest_data["temperature"], latest_data["humidity"]))
        latest_data["temperature"] = None
        latest_data["humidity"] = None

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.ws_set_options({'transport': 'websockets'})
mqtt_client.connect("157.173.101.159", 9001, 60)
mqtt_client.subscribe([(t, 0) for t in TOPICS])
mqtt_client.loop_start()

@app.get("/data")
def get_data():
    rows = execute_query("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 50", fetch=True)
    return [{"id": row[0], "temperature": row[1], "humidity": row[2], "timestamp": row[3]} for row in rows]

@app.get("/average_data")
def get_average_data():
    five_minutes_ago = datetime.now() - timedelta(minutes=5)
    rows = execute_query("""
        SELECT AVG(temperature), AVG(humidity)
        FROM weather
        WHERE timestamp >= ?
    """, (five_minutes_ago,), fetch=True)

    if rows:
        return {
            "temperature": rows[0][0] if rows[0][0] is not None else 0,
            "humidity": rows[0][1] if rows[0][1] is not None else 0
        }
    return {"temperature": 0, "humidity": 0}

@app.get("/")
def serve_index():
    if os.path.exists(index_file_path):
        with open(index_file_path, "r") as file:
            return file.read()
    return {"error": "index.html file not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
