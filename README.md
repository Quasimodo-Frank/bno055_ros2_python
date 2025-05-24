# bno055_ros2_python
the bno055 IMU ROS2 driver in Python

## Requirement
the `adafruit-circuitpython-bno055` package is needed

```bash
pip install adafruit-circuitpython-bno055
```

## how to build

```bash
colcon build --packages-select bno055_driver
source install/setup.bash
ros2 run bno055_driver bno055_node
```
you will need to run the below to make rviz2 work

'''bash
ros2 run tf2_ros static_transform_publisher  args='0 0 0 0 0 0 1 base_link imu_link'
'''


## how to run

The `full_launch.py` will launch the rivz2 automatically

```bash
ros2 launch bno055_driver full_launch.py
```

## package 

```
bno055_driver/
├── bno055_driver/
│   ├── __init__.py
│   └── bno055_node.py
├── launch/
│   ├── bno055_launch.py
│   └── full_launch.py
├── rviz/
│   └── bno055_visualization.rviz
├── config/
│   └── bno055_params.yaml
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── bno055_driver
└── test/
    └── test_bno055_driver.py
```

## to make the python driver work in the venv under docker

add the below lines to `setup.cfg`

```
[build_scripts]
executable = /usr/bin/env python3
```