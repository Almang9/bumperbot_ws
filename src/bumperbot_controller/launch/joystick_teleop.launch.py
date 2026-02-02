import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node


def generate_launch_description():
    bumperbot_controller_pkg = get_package_share_directory("bumperbot_controller")

    use_sim_time_arg = DeclareLaunchArgument(
        name="use_sim_time", default_value="True", description="Use simulated time"
    )
    joystick_teleop_node = Node(
        package="joy",
        executable="joy_node",
        name="joystick",
        parameters=[
            os.path.join(
                get_package_share_directory("bumperbot_controller"),
                "config",
                "joy_config.yaml",
            )
        ],
    )
    joy_teleop = Node(
        package="joy_teleop",
        executable="joy_teleop",
        parameters=[
            os.path.join(
                get_package_share_directory("bumperbot_controller"),
                "config",
                "joy_teleop.yaml",
            )
        ],
    )

    return LaunchDescription([use_sim_time_arg, joystick_teleop_node, joy_teleop])
