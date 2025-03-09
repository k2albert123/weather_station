# weather_station

to run this project you have to first get its dependencies
this project has javascript node sever and a python sever which run the same way but separately
1. Weather Station (MQTT WebSockets) with python
This project is a weather station that displays live temperature and humidity data using MQTT over WebSockets. It visualizes the data in real-time on a webpage using Chart.js and allows users to see both the current readings and historical data.

Prerequisites
Before running the project, ensure you have the following installed:

Python 3.7 or higher
pip (Python's package installer)

Dependencies
To install the required Python dependencies, run the following command:
pip install -r requirements.txt

If requirements.txt is not present, you can manually install these packages:

fastapi
uvicorn
sqlite3 (for database interaction, if needed)

You can install them via:
pip install fastapi uvicorn

Running the Project
1. Clone the Repository
First, clone the project repository to your local machine.
git clone <repository_url>
cd <project_directory>

2. Start the Server
Run the following command to start the FastAPI server:

python server.py

By default, the server will start on http://127.0.0.1:8000.

3. Access the Web Interface
Open your browser and navigate to:
http://127.0.0.1:8000

You should see the live weather data dashboard, which updates every 5 seconds with new temperature and humidity values.

TROUBLESHOOTING

If you see a Directory 'static' does not exist error, make sure the static/ directory exists or remove the static files section from server.py if not needed.
Ensure that the server is running on the correct port (by default 127.0.0.1:8000).
If data is not displaying properly, check your network connection and the browser console for any errors.
License
This project is licensed under the MIT License - see the LICENSE file for details.




2. USING NODE.JS(EXPRESS)

1. Clone the Repository
First, clone the project repository to your local machine.
git clone <repository_url>
cd <project_directory>
    cd <javascript_one>
    Install node.js
    run npm install express sqlite3 mqtt cors
    run node server.js
    Access the Web Interface
        Open your browser and navigate to:
        http://127.0.0.1:8000