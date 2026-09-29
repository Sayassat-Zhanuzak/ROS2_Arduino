# Arduino ROS 2 Light Tracking System

A simple **ROS 2 + Arduino** project that uses two LDR sensors to detect the direction of a light source and rotate a servo motor toward it.

## How It Works

```text
LDR 1 ─┐
       ├──> Arduino ──Serial──> LDR Node
LDR 2 ─┘                         │
                                │ /light
                                ▼
                           Servo Node
                                │
                              Serial
                                ▼
                             Arduino
                                │
                                ▼
                              Servo
```

The Arduino reads both LDR values and sends them to ROS 2.  
The `LDR_node` calculates the difference between the sensors and publishes it on the `/light` topic.  
The `servo_node` converts this value into a servo angle and sends it back to the Arduino.

## Hardware

- Arduino
- 2 × LDR
- Servo motor
- Breadboard and jumper wires

### Connections

| Component | Pin |
|---|---|
| LDR 1 | A0 |
| LDR 2 | A1 |
| Servo signal | D9 |

## Software

- Ubuntu
- ROS 2
- Python 3
- Arduino IDE
- `rclpy`
- `pyserial`

## ROS 2 Package

Package name:

```text
arduino_ros
```

Nodes:

```text
LDR_node
servo_node
```

Topic:

```text
/light
```

Message type:

```text
std_msgs/Int32
```

## Installation

Install the Python serial library:

```bash
pip3 install pyserial
```

Build the ROS 2 package:

```bash
cd ~/ros2_ws
colcon build --packages-select arduino_ros
source install/setup.bash
```

Make sure the Arduino is connected and available at:

```text
/dev/ttyUSB0
```

If necessary, change the port in `node.py`.

## Run

Upload the Arduino code using Arduino IDE, then run:

```bash
source ~/ros2_ws/install/setup.bash
ros2 run arduino_ros nodes
```

To monitor the light difference:

```bash
ros2 topic echo /light
```

## Result

The servo automatically rotates toward the side receiving more light.
