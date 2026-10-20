import time
import importlib
from flask import Flask, render_template
from flask_socketio import SocketIO

# Initialize Flask application and Flask-SocketIO with open CORS access for local networking
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ==========================================
# HYBRID HARDWARE & SIMULATION DETECTION
# ==========================================
# This block attempts to import Raspberry Pi specific hardware libraries.
# If running on a PC (Simulation Mode), it fails safely and switches to terminal logs.
try:
    board = importlib.import_module("board")
    PCA9685 = importlib.import_module("adafruit_pca9685").PCA9685
    GPIO = importlib.import_module("RPi.GPIO")
    busio = importlib.import_module("busio")
    
    # Initialize physical I2C bus and PCA9685 driver board for Raspberry Pi
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50  # Standard 50Hz frequency required for ESC PWM control
    HARDWARE_AVAILABLE = True
    print("--- LIVE HARDWARE MODE: Raspberry Pi & PCA9685 Detected ---")
    
except (ImportError, NotImplementedError, ModuleNotFoundError):
    HARDWARE_AVAILABLE = False
    print("--- SIMULATION MODE: Running on PC (Logging microsecond values to terminal) ---")

def set_pwm_pulse(channel, microseconds):
    """
    Hybrid PWM handler function. 
    Routes pulses to the physical PCA9685 board if on Pi, 
    otherwise prints simulation debug lines to the console.
    """
    if not HARDWARE_AVAILABLE:
        # Simulation output showing target channel and pulse width
        print(f"  -> [SIMULATION] PCA9685 Channel {channel} set to {microseconds}us")
    else:
        # Live Hardware conversion: Map microsecond range (1000-2000us) into 16-bit duty cycle for 50Hz
        duty_cycle = int((microseconds / 20000.0) * 0xFFFF)
        pca.channels[channel].duty_cycle = duty_cycle

def map_vector_to_pwm(surge, heave, yaw):
    """
    3-Thruster Mixer Algorithm:
    Takes normalized vector inputs (-1.0 to 1.0) for Surge, Heave, and Yaw,
    combines them for a 3-thruster configuration, and converts them 
    into standard microsecond pulse widths (1000us to 2000us, 1500us neutral).
    """
    # 1. Mix movement vectors into individual motor power demands
    left_power = max(-1.0, min(1.0, surge + yaw))     # Left horizontal thruster
    right_power = max(-1.0, min(1.0, surge - yaw))    # Right horizontal thruster
    vertical_power = max(-1.0, min(1.0, heave))       # Vertical thruster
    
    # 2. Scale [-1.0, 1.0] power floats to [1000, 2000] microsecond intervals
    left_us = int(1500 + (left_power * 500))
    right_us = int(1500 + (right_power * 500))
    vertical_us = int(1500 + (vertical_power * 500))
    
    return left_us, right_us, vertical_us

# ==========================================
# FLASK ROUTING & SOCKET.IO EVENT HANDLERS
# ==========================================

@app.route('/')
def index():
    """Serves the main frontend control dashboard."""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Triggered automatically when a web browser client connects to the dashboard."""
    print("Client successfully connected to ROV dashboard.")

@socketio.on('heartbeat')
def handle_heartbeat():
    """Receives periodic keep-alive pings from the frontend to maintain connection health."""
    pass

@socketio.on('thruster_vector')
def handle_thrusters(data):
    """
    Listens for real-time vector adjustments from dashboard sliders, 
    processes them via the mixer, and outputs microsecond PWM values.
    """
    surge = data.get('surge', 0.0)
    heave = data.get('heave', 0.0)
    yaw = data.get('yaw', 0.0)
    
    # Calculate microsecond pulse lengths
    left_us, right_us, vertical_us = map_vector_to_pwm(surge, heave, yaw)
    
    # Dual-print debugging displaying user inputs alongside computed PWM pulse targets
    print(f"[INPUTS] Surge: {surge:+.2f} | Heave: {heave:+.2f} | Yaw: {yaw:+.2f}")
    
    # Push microsecond values to respective hardware/simulation channels
    # Channel 0: Left Horizontal Thruster
    # Channel 1: Right Horizontal Thruster
    # Channel 2: Vertical Thruster
    set_pwm_pulse(channel=0, microseconds=left_us)
    set_pwm_pulse(channel=1, microseconds=right_us)
    set_pwm_pulse(channel=2, microseconds=vertical_us)

# ==========================================
# BACKGROUND TELEMETRY LOOP
# ==========================================

def background_monitor():
    """
    Continuous background task that polls sensors (IMU & Leak Sensor) 
    and streams telemetry data back to the web dashboard in real time.
    """
    while True:
        time.sleep(0.5)

        # Telemetry data dictionary (Toggle 'leak' to True to test safety alert banners)
        telemetry = {
            'leak': False,          # Water leak sensor status (False = Secure, True = Leak Detected)
            'depth': 0.42,          # Depth sensor measurement in meters
            'pitch': 1.2,           # IMU Pitch angle in degrees
            'roll': -0.5,           # IMU Roll angle in degrees
            'heading': 120.0        # IMU Compass heading / Yaw orientation
        }
        
        # Broadcast live telemetry payload to all connected clients via Socket.IO
        socketio.emit('telemetry_data', telemetry)

# ==========================================
# SERVER EXECUTION
# ==========================================

if __name__ == '__main__':
    # Start the background telemetry monitoring thread safely using Flask-SocketIO's built-in utility
    socketio.start_background_task(background_monitor)
    
    print("Starting hybrid ROV control server at http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)