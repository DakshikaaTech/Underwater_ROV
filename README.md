
# Underwater ROV Control Stack (3-DOF, 3-Thruster Hybrid Architecture)
*A robust, real-time web-based control stack and telemetry dashboard designed for a 3-Degree-of-Freedom (3-DOF) underwater Remotely Operated Vehicle (ROV).*

The application translates normalized vector commands (Surge, Heave, Yaw) into precise microsecond PWM pulse widths for Electronic Speed Controllers (ESCs) and Brushless DC (BLDC) thrusters. It features a hybrid execution engine that allows seamless testing via desktop simulation or direct deployment on a Raspberry Pi with a PCA9685 PWM board.

## System Architecture & Features
- **Hybrid Execution Environment**: Automatically checks for Raspberry Pi GPIO and I2C libraries upon startup. If running locally on a PC, it defaults to a safe simulation mode, logging microsecond targets to the console. On a Raspberry Pi, it initializes live hardware controls.

- **3-Thruster Mixing Algorithm**: Efficiently computes dual-horizontal thruster mixing (combining Surge and Yaw via differential thrust) alongside an independent vertical thruster channel (Heave).

- **Real-Time Web Telemetry**: Leverages Flask-SocketIO for bidirectional, low-latency communication, streaming background sensor loops (IMU attitude metrics and water leak alerts) directly to the UI.

- **Safety Alert System**: Dedicated UI status banner that instantly toggles between a secure green state ("Dry & Secure") and a flashing critical red warning upon water leak detection.

<img width="959" height="474" alt="dashboard" src="https://github.com/user-attachments/assets/1319d8bb-0448-40f2-ac88-98a0b6877dec" />


