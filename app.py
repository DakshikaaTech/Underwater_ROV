import time
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- SIMULATION HARDWARE CHECK ---
try:
    import board
    import busio
    from adafruit_pca9685 import PCA9685
    import RPi.GPIO as GPIO
    HARDWARE_AVAILABLE = True
except (ImportError, NotImplementedError):
    print("--- RUNNING IN SIMULATION MODE (No Pi hardware detected) ---")
    HARDWARE_AVAILABLE = False

# Global State & Safety Variables
last_heartbeat_time = time.time()
ROV_ARMED = False

def set_pwm_pulse(channel, microseconds):
    if not HARDWARE_AVAILABLE:
        print(f"[SIMULATION] PWM Channel {channel} set to {microseconds}us")
        return
    # Real Pi hardware code would go here

def arm_escs():
    print("Arming ESCs (Simulation)...")
    time.sleep(1)
    print("ESCs Armed.")

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

@socketio.on('set_arm_state')
def handle_arm_state(data):
    global ROV_ARMED
    ROV_ARMED = data.get('armed', False)
    if ROV_ARMED:
        arm_escs()
    else:
        print("ROV Disarmed.")

@socketio.on('thruster_vector')
def handle_thrusters(data):
    if not ROV_ARMED:
        return
    surge = data.get('surge', 0.0)
    heave = data.get('heave', 0.0)
    yaw = data.get('yaw', 0.0)
    print(f"[THRUSTERS] Surge: {surge}, Heave: {heave}, Yaw: {yaw}")

@socketio.on('servo_command')
def handle_servo(data):
    servo_id = data.get('id', 0)
    angle = data.get('angle', 90)
    print(f"[SERVO] Servo {servo_id} moved to {angle}°")

# Background monitoring loop (simulates telemetry & safety checks)
def background_monitor():
    global last_heartbeat_time, ROV_ARMED
    while True:
        time.sleep(0.5)
        if ROV_ARMED and (time.time() - last_heartbeat_time > 1.5):
            print("SAFETY WARNING: Heartbeat lost! Disarming ROV.")
            ROV_ARMED = False

        telemetry = {
            'armed': ROV_ARMED,
            'leak': False,          # Change to True to test leak warning UI!
            'depth': 0.42,
            'pitch': 1.2,
            'roll': -0.5,
            'heading': 120.0
        }
        socketio.emit('telemetry_data', telemetry)

if __name__ == '__main__':
    monitor_thread = threading.Thread(target=background_monitor, daemon=True)
    monitor_thread.start()
    print("Starting local ROV server at http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)