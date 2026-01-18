import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/jbw/yolo_fashion_mnist/ros2_ws/install/yolo_fashion_mnist'
