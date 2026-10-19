# Underwater ROV

*The main aim of this project is to design, assemble, and program a compact, neutrally buoyant tethered Remotely Operated Vehicle (ROV) capable of underwater navigation, real-time video streaming, and object retrieval in a controlled aquatic environment.*

<img width="896" height="1195" alt="Gemini_Generated_Image_og124hog124hog12" src="https://github.com/user-attachments/assets/a637dcd0-7245-4f67-a482-8995f6e3cb93" />


## Real World Applications:
**1. Underwater Infrastructure & Pipeline Inspection**
- The Application: Inspecting underwater structures such as dam walls, bridge pilings, port jetties, and subsea oil or gas pipelines for structural cracks, corrosion, and erosion.
-	Why an ROV is used: It avoids sending human divers into hazardous, deep, or turbid conditions. Equipping the ROV with live camera feeds and light arrays allows engineers topside to assess structural integrity without dewatering structures or stopping operations.

**2. Marine Environmental Monitoring & Ecological Sampling**
- The Application: Surveying marine ecosystems and aquatic animals (like coral reefs and benthic floors), tracking microplastic pollution, and gathering water-column data (temperature, depth, turbidity).
- Why an ROV is used: Researchers can deploy an ROV with a robotic manipulator arm to collect sediment samples or soft corals gently without disturbing the surrounding habitat or requiring human physical entry into deep ecosystems.

**3. Search, Rescue, & Object Recovery (SAR)**
- The Application: Locating submerged vehicles, debris, lost equipment, or historical artifacts in lakes, rivers, and coastal areas.
-	Why an ROV is used: High-risk waters with low visibility or toxic contamination make diver deployment unsafe. An ROV with multi-thruster control and a mechanical gripper can locate targets visually and latch onto objects to pull them to the surface.


## COMPONENTS USED:
### Section 1: Main Control & Communication
-	Raspberry Pi 5 (4GB SBC): Central mission computer. Receives topside commands, executes real-time control algorithms, processes sensor readings, and encodes/streams low-latency video feed.
-	PCA9685 16-Channel 12-Bit PWM Driver: I²C-bus expansion module used to generate precise pulse-width modulation (PWM) control signals for all 4 thruster ESCs, 4 robotic arm servos, and lighting MOSFETs.
-	BSS138 I²C Logic Level Converter: Bi-directional voltage translator matching the 3.3V logic signals of the Raspberry Pi to 5V-tolerant sensor ICs and drivers.
- 10m Flexible Ethernet Tether Cable & IP68 Bulkhead Connector: Heavy-duty, high-bandwidth physical communication link between the surface workstation and subsea enclosure.

### Section 2: Underwater Propulsion
-	12V Waterproof Brushless Thrusters (x4): Primary mobility mechanism configured vectorially to provide multi-DOF positioning (surge, sway, yaw, and heave).
-	Bidirectional Electronic Speed Controllers (ESCs) (x4): High-current motor drivers that accept PWM inputs to regulate motor speed and rapidly reverse brushless thruster rotation.

### Section 3: Manipulator Arm Electronics
-	70KG IP68 Brushless Digital Servos (270° Range) (x4): High-torque, fully submerged waterproof actuators responsible for multi-axis movement of the robotic manipulator arm.
-	High-Current Regulated 7.4V Servo BEC (28A Peak): Dedicated step-down voltage regulator supplying continuous high current to prevent brownouts on the main controller during high-load arm manipulation.

### Section 4: Vision & Auxiliary Lighting
-	CADDX Ratel 2 Analog FPV Camera + USB CVBS Capture Card: High-sensitivity visual navigation system capturing real-time low-light video fed directly to the topside station.

### Section 5: Telemetry & Failsafe Sensors
-	Waterproof I²C Depth / Pressure Sensor: High-precision pressure transducer used in closed-loop depth-holding navigation algorithms.
-	MPU6050 6-DOF IMU: Combined 3-axis accelerometer and 3-axis gyroscope used for attitude tracking, vehicle dynamic stabilization, and orientation feedback.
-	LM393 Water-Leak Sensor Probe: Internal humidity/water-sensing trace module placed inside the lower electronics enclosure to sound an emergency alert upon hull compromise.

### Section 6: Power Distribution & Safety
-	12V Main Battery Pack & Fused Distribution Block: High-capacity power source providing isolated current rails to thrusters, logic systems, and high-power servos through branch protection fuses.
-	5.1V / 5A DC-DC Buck Regulator: Step-down power module providing high-efficiency, ripple-free power to the Raspberry Pi 5.
-	Master Power Disconnect & Hardware Interlock: Main physical cut-off switch allowing complete power isolation during servicing and tether handling.

## Methodology:
### 1. Cut and Assemble the PVC Frame:
Use PVC pipes and elbows to build an open-frame chassis (typically a rectangular or cat-like catamaran frame) that will house your buoyancy, electronics cylinder, thrusters, and manipulator arm. Drill drainage and flooding holes into structural non-pressure PVC pipes so the frame doesn't trap unwanted buoyant air pockets underwater.

*Verification: Submerge the empty PVC frame in a tub of water to ensure it sinks freely and stays balanced without structural twists.*

### 2.Prepare the Watertight Pressure Hull:
Take a thick PVC or acrylic pipe section with end caps to serve as your main electronics housing. Drill precise holes in one end cap to mount the waterproof Ethernet bulkhead connector and cable penetrators/glands for your thruster and sensor wires. Apply marine-grade sealant or O-rings to every entry point.

*Verification: Seal the empty hull completely, submerge it in water for 15 minutes, and check the inside for any signs of moisture leakage.*

### 3.Install Internal Core Electronics:
Mount your Raspberry Pi 5, PCA9685 PWM driver, BSS138 logic level converter, and power distribution components securely inside the dry pressure hull. Connect the 5.1V buck regulator to the Raspberry Pi and wire the PCA9685 to the Pi's I²C pins.

*Verification: Power up the internal electronics on your workbench to verify that the Raspberry Pi boots successfully and detects the I²C devices.*

### 4.Mount Thrusters and Manipulator Arm:
Secure your 4 waterproof brushless thrusters to the exterior of the PVC frame in a vector configuration (for surge, sway, and heave control). Route their power cables through the hull penetrators to connect to the bidirectional ESCs inside, and mount the 70KG IP68 servos onto the front of the frame for the robotic arm.

*Verification: Run a dry diagnostic test script to ensure every thruster spins cleanly in response to commands and the servos move smoothly.*

### 5.Run Tether and Final Sealing:
Connect the 10-meter flexible Ethernet tether through the waterproof bulkhead connector into the Raspberry Pi. Seal the hull end caps tightly, ensuring all O-rings are compressed evenly. Connect the topside end to your computer or control station running the Logitech F310 gamepad.

*Verification: Test the full communication link and camera stream over the tether before deploying the ROV into shallow water.*

<img width="942" height="1280" alt="IMG-20261013-WA0002" src="https://github.com/user-attachments/assets/bc79679e-8df5-473e-9314-480e1107ce19" />

<img width="1536" height="1024" alt="circuit_diagram" src="https://github.com/user-attachments/assets/7c728d2c-177f-4745-a814-d56bee7480bd" />

