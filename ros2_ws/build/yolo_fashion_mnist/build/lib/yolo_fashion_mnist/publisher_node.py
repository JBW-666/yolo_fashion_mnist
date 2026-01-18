# 功能：ROS2发布节点 - 加载YOLOv8模型推理Fashion MNIST图片，发布类别+准确度
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ultralytics import YOLO
import os

# ====================== 核心配置（无需修改，已适配jbw用户名） ======================
USER_NAME = "jbw"
ROOT_DIR = f"/home/{USER_NAME}/yolo_fashion_mnist"
# 训练好的YOLOv8模型权重路径
MODEL_PATH = f"{ROOT_DIR}/runs/detect/train/weights/best.pt"
# 要推理的测试图片路径（选训练集中的一张示例）
TEST_IMG_PATH = f"{ROOT_DIR}/yolo_dataset/images/train/67.jpg"
# ROS2发布话题名称
TOPIC_NAME = "fashion_mnist_detection"
# Fashion MNIST类别名称（和训练时一致）
CLASS_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]
IMG_SIZE = 128  # 和训练/生成数据集时的尺寸一致

class YoloDetectionPublisher(Node):
    def __init__(self):
        # 初始化ROS2节点，节点名：yolo_detection_pub
        super().__init__('yolo_detection_pub')
        # 创建发布者，发布std_msgs/String类型消息，话题名：fashion_mnist_detection，队列大小10
        self.publisher_ = self.create_publisher(String, TOPIC_NAME, 10)
        # 加载YOLOv8模型
        self.model = YOLO(MODEL_PATH)
        self.get_logger().info("YOLOv8模型加载完成！")
        # 定时推理并发布（每2秒发布一次，可改）
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        # 1. 模型推理
        results = self.model.predict(TEST_IMG_PATH, imgsz=IMG_SIZE)
        res = results[0]  # 取第一张图片的推理结果

        # 2. 解析推理结果（类别+准确度）
        detection_msg = ""
        for idx, box in enumerate(res.boxes):
            cls_idx = int(box.cls[0])  # 类别索引
            confidence = box.conf[0].item()  # 准确度（0-1）
            cls_name = CLASS_NAMES[cls_idx]
            # 拼接单条检测结果（格式："目标1：T-shirt/top | 准确度：0.9876"）
            detection_msg += f"目标{idx+1}：{cls_name} | 准确度：{confidence:.4f}\n"

        # 3. 发布消息
        msg = String()
        msg.data = detection_msg if detection_msg else "未检测到目标"
        self.publisher_.publish(msg)
        self.get_logger().info(f"发布检测结果：\n{msg.data}")

def main(args=None):
    # 初始化ROS2
    rclpy.init(args=args)
    # 创建发布节点实例
    publisher_node = YoloDetectionPublisher()
    # 自旋节点（保持节点运行）
    rclpy.spin(publisher_node)
    # 销毁节点
    publisher_node.destroy_node()
    # 关闭ROS2
    rclpy.shutdown()

if __name__ == '__main__':
    main()
