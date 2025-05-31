# bno055_driver/bno055_driver/bno055_node.py
#from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import board

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
#import board
#import busio
#import adafruit_bno055
from geometry_msgs.msg import Quaternion
import math

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path


# Function to convert Euler angles (roll, pitch, yaw) to quaternion

def euler_to_quaternion(roll, pitch, yaw):
    """Convert Euler angles to quaternion."""
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    return Quaternion(
        x = sr * cp * cy - cr * sp * sy,
        y = cr * sp * cy + sr * cp * sy,
        z = cr * cp * sy - sr * sp * cy,
        w = cr * cp * cy + sr * sp * sy,
    )

class BNO055Node(Node):
    def __init__(self):
        super().__init__('bno055_node')
        self.publisher_ = self.create_publisher(Imu, 'imu/data_raw', 10)
        self.mag_publisher_ = self.create_publisher(MagneticField, 'imu/mag', 10)
        self.path_pub = self.create_publisher(Path, 'imu/path', 10)

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.path_msg = Path()
        self.path_msg.header.frame_id = 'imu_link'


        #i2c = busio.I2C(board.SCL, board.SDA)
        #self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        i2c = board.I2C()  # Device is /dev/i2c-1
        self.sensor = adafruit_bno055.BNO055_I2C(i2c,0x29)


    def timer_callback(self):
        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'imu_link'

        euler = self.sensor.euler  # (heading, roll, pitch)
        gyro = self.sensor.gyro    # (x, y, z) rad/s
        accel = self.sensor.acceleration  # (x, y, z) m/s^2

        if euler and gyro and accel:
            roll = math.radians(euler[1])
            pitch = math.radians(euler[2])
            yaw = math.radians(euler[0])

            quat = euler_to_quaternion(roll, pitch, yaw)
            imu_msg.orientation = quat

            imu_msg.angular_velocity.x = gyro[0]
            imu_msg.angular_velocity.y = gyro[1]
            imu_msg.angular_velocity.z = gyro[2]

            imu_msg.linear_acceleration.x = accel[0]
            imu_msg.linear_acceleration.y = accel[1]
            imu_msg.linear_acceleration.z = accel[2]

            self.publisher_.publish(imu_msg)


        mag = self.sensor.magnetic  # (x, y, z) in microteslas
        mag_msg = MagneticField()
        mag_msg.header.stamp = self.get_clock().now().to_msg()
        mag_msg.header.frame_id = 'imu_link'

        if mag:
            mag_msg.magnetic_field.x = mag[0] * 1e-6  # convert µT to Tesla
            mag_msg.magnetic_field.y = mag[1] * 1e-6
            mag_msg.magnetic_field.z = mag[2] * 1e-6
            
            self.mag_publisher_.publish(mag_msg)

        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = 'imu_link'

        # For now, just append static/dummy positions or update as needed
        # Replace these with actual integration if available
        pose.pose.position.x = len(self.path_msg.poses) * 0.05  # simulate forward movement
        pose.pose.position.y = 0.0
        pose.pose.position.z = 0.0

        # Use IMU orientation
        pose.pose.orientation = imu_msg.orientation

        self.path_msg.poses.append(pose)
        self.path_msg.header.stamp = pose.header.stamp
        self.path_pub.publish(self.path_msg)


def main(args=None):
    rclpy.init(args=args)
    node = BNO055Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
