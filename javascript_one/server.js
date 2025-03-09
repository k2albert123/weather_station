const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
const mqtt = require("mqtt");

const app = express();
const PORT = 3000;
app.use(cors());
app.use(express.json());

// Connect to SQLite Database
const db = new sqlite3.Database("./weather.db", (err) => {
    if (err) console.error(err.message);
    else console.log("Connected to SQLite database.");
});

// Create table if it doesn't exist
db.run(`
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
`);

// MQTT Connection
const mqttClient = mqtt.connect("ws://157.173.101.159:9001");

mqttClient.on("connect", () => {
    console.log("Connected to MQTT Broker");
    mqttClient.subscribe("/work_group_01/room_temp/temperature");
    mqttClient.subscribe("/work_group_01/room_temp/humidity");
});

let latestData = { temperature: null, humidity: null };

mqttClient.on("message", (topic, message) => {
    console.log(`Received: ${topic} → ${message.toString()}`);
    
    if (topic.includes("temperature")) {
        latestData.temperature = parseFloat(message.toString());
    } else if (topic.includes("humidity")) {
        latestData.humidity = parseFloat(message.toString());
    }

    if (latestData.temperature !== null && latestData.humidity !== null) {
        db.run(
            "INSERT INTO weather (temperature, humidity) VALUES (?, ?)",
            [latestData.temperature, latestData.humidity],
            (err) => {
                if (err) console.error(err.message);
                else console.log("Data saved to database.");
            }
        );
        latestData = { temperature: null, humidity: null };
    }
});

// API to Get Data
app.get("/data", (req, res) => {
    db.all("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 50", [], (err, rows) => {
        if (err) res.status(500).json({ error: err.message });
        else res.json(rows);
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
