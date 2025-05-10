from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bno055_driver',
            executable='bno055_node',
            name='bno055_node',
            output='screen',
            parameters=[],
        ),
    ])


# ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 base_link imu_link