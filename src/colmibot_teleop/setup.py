from setuptools import find_packages, setup

package_name = 'colmibot_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/launch', ['launch/turtle_joy.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vick',
    maintainer_email='victor.itam.mx@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['joy_turtle_controller.py = colmibot_teleop.joy_turtle_controller:main',
        ],
    },
)
