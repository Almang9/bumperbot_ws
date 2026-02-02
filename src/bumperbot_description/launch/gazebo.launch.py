import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    bumperbot_description_dir = get_package_share_directory("bumperbot_description")
    ros_distro = os.environ["ROS_DISTRO"]
    is_ignition = "True" if ros_distro == "humble" else "False"

    model_args = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            bumperbot_description_dir, "urdf", "bumperbot.urdf.xacro"
        ),
        description="Absolute Path to the Robot URDF File",
    )

    robot_description = ParameterValue(
        Command(
            ["xacro ", LaunchConfiguration("model"), " is_ignition:=", is_ignition]
        ),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(bumperbot_description_dir).parent.resolve())],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("ros_gz_sim"), "launch"),
                "/gz_sim.launch.py",
            ]
        ),
        launch_arguments=[("gz_args", [" -v 4", " -r", " empty.sdf"])],
    )
    world_name = "empty"
    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_gz_bridge",
        output="screen",
        arguments=[
            # Define the bridge for the namespaced clock
            f"/world/{world_name}/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"
        ],
        remappings=[
            # Remap the namespaced topic to the global /clock topic
            (f"/world/{world_name}/clock", "/clock")
        ],
    )
    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description", "-name", "bumperbot"],
    )

    return LaunchDescription(
        [
            model_args,
            robot_state_publisher_node,
            gazebo_resource_path,
            gazebo,
            gz_spawn_entity,
            gz_ros2_bridge,
        ]
    )
