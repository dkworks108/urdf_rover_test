import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    urdf_path = os.path.join(pkg_dir, 'urdf', 'robot.urdf')
    rviz_config = os.path.join(pkg_dir, 'config', 'rviz.rviz')
    rviz_args = ['-d', rviz_config] if os.path.exists(rviz_config) else []

    with open(urdf_path, 'r') as f:
        robot_desc = f.read()

    # resolve package:// mesh paths for RViz resource retriever without editing original urdf
    robot_desc = robot_desc.replace('package://05_planetary_rover/', f'file://{pkg_dir}/')

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=rviz_args
        )
    ])
