import time
import threading
import importlib
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- SIMULATION HARDWARE CHECK ---
try:
    importlib.import_module("board")
    PCA9685 = importlib.import_module("adafruit_pca9685").PCA9685
    GPIO = importlib.import_module("RPi.GPIO")
    HARDWARE_AVAILABLE = True
except (ImportError, NotImplementedError, ModuleNotFoundError):
    print("--- RUNNING IN SIMULATION MODE (No Pi hardware detected) ---")
    HARDWARE_AVAILABLE = False

# Global State Variables
last_heartbeat_time = time.time()

def set_pwm_pulse(channel, microseconds):
    if not HARDWARE_AVAILABLE:
        print(f"[SIMULATION] PWM Channel {channel} set to {microseconds}us")
        return
    # Real Pi hardware code would go here

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected to ROV dashboard.")

@socketio.on('heartbeat')
def handle_heartbeat():
    global last_heartbeat_time
    last_heartbeat_time = time.time()

@socketio.on('thruster_vector')
def handle_thrusters(data):
    surge = data.get('surge', 0.0)
    heave = data.get('heave', 0.0)
    yaw = data.get('yaw', 0.0)
    print(f"[THRUSTERS] Surge: {surge}, Heave: {heave}, Yaw: {yaw}")

# Background monitoring loop (Simulating IMU Sensors & Leak Detector)
def background_monitor():
    global last_heartbeat_time
    while True:
        time.sleep(0.5)

        telemetry = {
            'leak': False,          # Change to True to test leak warning UI!
            'depth': 0.42,          # IMU / Depth Sensor Data
            'pitch': 1.2,           # IMU Pitch
            'roll': -0.5,           # IMU Roll
            'heading': 120.0        # IMU Heading/Yaw
        }
        socketio.emit('telemetry_data', telemetry)

if __name__ == '__main__':
    monitor_thread = threading.Thread(target=background_monitor, daemon=True)
    monitor_thread.start()
    print("Starting local ROV server at http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)