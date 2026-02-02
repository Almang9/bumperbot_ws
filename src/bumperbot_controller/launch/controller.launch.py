from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value="true",
        description="Whether to use the Python controller",
    )

    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius", default_value="0.033", description="Radius of the wheels"
    )
    wheel_separation_arg = DeclareLaunchArgument(
        "wheel_separation",
        default_value="0.17",
        description="Separation between wheels",
    )

    use_simple_controller_arg = DeclareLaunchArgument(
        "use_simple_controller",
        default_value="True",
        description="Whether to use the simple controller",
    )

    use_python = LaunchConfiguration("use_python")
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")
    use_simple_controller = LaunchConfiguration("use_simple_controller")
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        parameters=[{"use_sim_time": True}],
    )
    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "bumperbot_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        parameters=[{"use_sim_time": True}],
        condition=UnlessCondition(use_simple_controller),
    )

    simple_controlller = GroupAction(
        condition=IfCondition(use_simple_controller),
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "simple_velocity_controller",
                    "--controller-manager",
                    "/controller_manager",
                ],
                parameters=[{"use_sim_time": True}],
            ),
            Node(
                package="bumperbot_controller",
                executable="simple_controller.py",
                name="simple_velocity_controller",
                parameters=[
                    {"wheel_radius": wheel_radius},
                    {"wheel_separation": wheel_separation},
                    {"use_sim_time": True},
                ],
                condition=IfCondition(use_python),
            ),
            Node(
                package="bumperbot_controller",
                executable="simple_controller",
                name="simple_velocity_controller",
                parameters=[
                    {"wheel_radius": wheel_radius},
                    {"wheel_separation": wheel_separation},
                    {"use_sim_time": True},
                ],
                condition=UnlessCondition(use_python),
            ),
        ],
    )

    return LaunchDescription(
        [
            use_python_arg,
            wheel_radius_arg,
            wheel_separation_arg,
            use_simple_controller_arg,
            joint_state_broadcaster_spawner,
            wheel_controller_spawner,
            simple_controlller,
        ]
    )
