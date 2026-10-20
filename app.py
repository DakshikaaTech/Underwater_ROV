import time
import importlib
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- HYBRID HARDWARE & SIMULATION DETECTION ---
try:
    board = importlib.import_module("board")
    PCA9685 = importlib.import_module("adafruit_pca9685").PCA9685
    GPIO = importlib.import_module("RPi.GPIO")
    busio = importlib.import_module("busio")
    
    # Initialize real hardware if on Raspberry Pi
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
    HARDWARE_AVAILABLE = True
    print("--- LIVE HARDWARE MODE: Raspberry Pi & PCA9685 Detected ---")
    
except (ImportError, NotImplementedError, ModuleNotFoundError):
    HARDWARE_AVAILABLE = False
    print("--- SIMULATION MODE: Running on PC (Printing PWM values to terminal) ---")

def set_pwm_pulse(channel, microseconds):
    """
    Hybrid PWM handler: Sends pulses to real hardware if available, 
    otherwise logs simulation feedback to the terminal.
    """
    if not HARDWARE_AVAILABLE:
        print(f"  -> [SIMULATION] PCA9685 Channel {channel} set to {microseconds}us")
        return
    
    # Real Pi Hardware Execution
    duty_cycle = int((microseconds / 20000.0) * 0xFFFF)
    pca.channels[channel].duty_cycle = duty_cycle

def map_vector_to_pwm(surge, heave, yaw):
    """
    Mixes Surge, Heave, and Yaw vectors into 3 individual thruster signals,
    then converts them to microsecond PWM values (1000us to 2000us).
    """
    # 1. Thruster Mixing Logic for 3 Thrusters (Left, Right, Vertical)
    left_power = max(-1.0, min(1.0, surge + yaw))
    right_power = max(-1.0, min(1.0, surge - yaw))
    vertical_power = max(-1.0, min(1.0, heave))
    
    # 2. Convert normalized [-1, 1] range to Microseconds [1000, 2000] (1500 is stop)
    left_us = int(1500 + (left_power * 500))
    right_us = int(1500 + (right_power * 500))
    vertical_us = int(1500 + (vertical_power * 500))
    
    return left_us, right_us, vertical_us

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected to ROV dashboard.")

@socketio.on('heartbeat')
def handle_heartbeat():
    pass

@socketio.on('thruster_vector')
def handle_thrusters(data):
    surge = data.get('surge', 0.0)
    heave = data.get('heave', 0.0)
    yaw = data.get('yaw', 0.0)
    
    # Calculate microsecond pulses for your 3 thrusters
    left_us, right_us, vertical_us = map_vector_to_pwm(surge, heave, yaw)
    
    # Dual-print debugging showing both raw inputs and computed microsecond outputs
    print(f"[INPUTS] Surge: {surge:+.2f} | Heave: {heave:+.2f} | Yaw: {yaw:+.2f}")
    
    # Send to simulation / physical channels (Channel 0: Left, 1: Right, 2: Vertical)
    set_pwm_pulse(channel=0, microseconds=left_us)
    set_pwm_pulse(channel=1, microseconds=right_us)
    set_pwm_pulse(channel=2, microseconds=vertical_us)

# Background monitoring loop (Simulating IMU Sensors & Leak Detector)
def background_monitor():
    while True:
        time.sleep(0.5)

        # Hybrid Telemetry Data (Hook up real physical sensors here when ready)
        telemetry = {
            'leak': False,          # Toggle to True to test warning banner state
            'depth': 0.42,          # Depth Sensor Simulation/Read
            'pitch': 1.2,           # IMU Pitch
            'roll': -0.5,           # IMU Roll
            'heading': 120.0        # IMU Heading/Yaw
        }
        socketio.emit('telemetry_data', telemetry)

if __name__ == '__main__':
    socketio.start_background_task(background_monitor)
    print("Starting hybrid ROV server at http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)