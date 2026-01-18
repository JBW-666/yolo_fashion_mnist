from setuptools import find_packages, setup

package_name = 'yolo_fashion_mnist'

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
    maintainer='jbw',
    maintainer_email='jbw@todo.todo',
    description='ROS2 node for YOLOv8 Fashion MNIST detection',
    license='Apache-2.0',
    tests_require=['pytest'],
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'yolo_pub = yolo_fashion_mnist.publisher_node:main',
            'yolo_sub = yolo_fashion_mnist.subscriber_node:main',
        ],
    },
)
