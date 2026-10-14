from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        #el simulador, viene con la instalacion de ROS
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            output='screen'
        ),

        #lee el control y publica su estado en /joy
        #deadzone define que tan lejos del centro empieza a contar
        #autorepeat_rate hace que republique 20 veces por segundo aunque
        #no haya cambios, si no la tortuga se frenaria sola al dejar el
        #stick quieto porque turtlesim para si no recibe comandos
        Node(
            package='joy',
            executable='joy_node',
            parameters=[{
                'deadzone': 0.1,
                'autorepeat_rate': 20.0,
            }],
            output='screen'
        ),

        #convierte el estado del control en velocidades
        Node(
            package='colmibot_teleop',
            executable='joy_turtle_controller.py',
            output='screen'
        ),
    ])
