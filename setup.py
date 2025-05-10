from setuptools import setup

package_name = 'bno055_driver'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/bno055_launch.py', 'launch/full_launch.py']),
        ('share/' + package_name + '/resource', ['resource/bno055_driver']),
    ],
    install_requires=['setuptools', 'adafruit-circuitpython-bno055'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='ROS2 driver for the BNO055 IMU',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bno055_node = bno055_driver.bno055_node:main',
        ],
    },
)