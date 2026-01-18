# 功能：ROS2订阅节点 - 接收Fashion MNIST检测结果并打印
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# ROS2订阅话题名称（必须和发布节点一致）
TOPIC_NAME = "fashion_mnist_detection"

class YoloDetectionSubscriber(Node):
    def __init__(self):
        # 初始化ROS2节点，节点名：yolo_detection_sub
        super().__init__('yolo_detection_sub')
        # 创建订阅者，订阅std_msgs/String类型消息，话题名：fashion_mnist_detection
        self.subscription = self.create_subscription(
            String,
            TOPIC_NAME,
            self.listener_callback,  # 收到消息后的回调函数
            10  # 队列大小
        )
        self.subscription  # 防止未使用变量警告
        self.get_logger().info("订阅节点已启动，等待检测结果...")

    def listener_callback(self, msg):
        # 回调函数：收到消息后打印
        self.get_logger().info(f"\n收到检测结果：\n{msg.data}")

def main(args=None):
    # 初始化ROS2
    rclpy.init(args=args)
    # 创建订阅节点实例
    subscriber_node = YoloDetectionSubscriber()
    # 自旋节点
    rclpy.spin(subscriber_node)
    # 销毁节点
    subscriber_node.destroy_node()
    # 关闭ROS2
    rclpy.shutdown()

if __name__ == '__main__':
    main()
