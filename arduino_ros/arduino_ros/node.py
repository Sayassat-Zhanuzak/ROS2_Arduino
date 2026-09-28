import rclpy
from rclpy.node import Node
import serial
import time
from std_msgs.msg import Int32

class Arduino_ROS2:
    def __init__(self):
        self.arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        time.sleep(2)

    def read_line(self):
        return self.arduino.readline().decode('utf-8').strip()
    
    def write_data(self, data):
        return self.arduino.write(data.encode('utf-8'))


class LDR_node(Node):
    def __init__(self, serial_manager):
        super().__init__('LDR_node')        
        self.serial_manager = serial_manager
        self.publisher_ = self.create_publisher(Int32, 'light', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.get_logger().info('LDR node has started!')

    def timer_callback(self):
        line = self.serial_manager.read_line()
        s1, s2 = line.split(',')
        msg = Int32()
        msg.data = int(s1) - int(s2)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Light: {msg.data}')


class Servo_node(Node):
    def __init__(self, serial_manager):
        self.serial_manager = serial_manager
        super().__init__('servo_node')
        self.get_logger().info('Servo node is active!')
        self.subscription_ = self.create_subscription(Int32, 'light', self.listener_callback, 10)

    def listener_callback(self, msg):
        light = msg.data
        angle = int(90 + light*180/2046)
        self.get_logger().info(f'Computed angle: {angle}')
        data_to_send = f'{angle}\n'
        self.serial_manager.write_data(data_to_send)


def main(args = None):
    rclpy.init(args=args)
    serial_manager = Arduino_ROS2()
    ldr_node = LDR_node(serial_manager)
    servo_node = Servo_node(serial_manager)
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(ldr_node)
    executor.add_node(servo_node)
    executor.spin()
    rclpy.shutdown()