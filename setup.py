from setuptools import find_packages, setup

package_name = 'gaze_object'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pcsukhyun',
    maintainer_email='90556528+LSH1218@users.noreply.github.com',
    description='Turtlesim nodes that gaze at, approach and stop near a target (ROS 2 Jazzy study)',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gaze_turtle = gaze_object.gaze_turtle:main',
            'smooth_turtle = gaze_object.smooth_turtle:main',
        ],
    },
)
