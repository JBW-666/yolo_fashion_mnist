# ROS2发布节点：YOLOv8推理Fashion MNIST并随机发布不同图片的结果
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ultralytics import YOLO
import os
import random  # 新增：导入随机模块

# 核心配置
USER_NAME = "jbw"
ROOT_DIR = f"/home/{USER_NAME}/yolo_fashion_mnist"
MODEL_PATH = f"{ROOT_DIR}/runs/weights/best.pt"  # 训练好的模型

IMG_ROOT_DIR = f"{ROOT_DIR}/yolo_dataset/images"  # 所有图片的根目录
TOPIC_NAME = "fashion_mnist_detection"  # 发布话题名
CLASS_NAMES = [  # 类别映射（和训练一致）
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]
IMG_SIZE = 128  # 和数据集/训练尺寸一致


def get_all_image_paths(img_root):
    """遍历指定目录下所有.jpg图片，返回路径列表"""
    img_paths = []
    # 遍历train和val两个子目录
    for sub_dir in ["train", "val"]:
        dir_path = os.path.join(img_root, sub_dir)
        # 检查目录是否存在
        if not os.path.exists(dir_path):
            continue
        # 遍历目录里的所有文件
        for file_name in os.listdir(dir_path):
            # 只保留.jpg文件
            if file_name.endswith(".jpg"):
                full_path = os.path.join(dir_path, file_name)
                img_paths.append(full_path)
    return img_paths

class YoloPublisher(Node):
    def __init__(self):
        super().__init__('yolo_detection_pub')  # 节点名
        self.pub = self.create_publisher(String, TOPIC_NAME, 10)  # 创建发布者
        self.model = YOLO(MODEL_PATH)  # 加载YOLO模型
        
        # 新增：获取所有图片路径列表
        self.img_paths = get_all_image_paths(IMG_ROOT_DIR)
        # 容错：如果没有找到图片，提示并退出
        if not self.img_paths:
            self.get_logger().error("未找到任何.jpg图片！请检查IMG_ROOT_DIR路径")
            rclpy.shutdown()
            return
        
        self.get_logger().info(f"YOLOv8模型加载完成！共找到{len(self.img_paths)}张图片")
        # 每2秒随机选一张图片推理并发布（可修改2.0调整频率）
        self.timer = self.create_timer(2.0, self.publish_result)

    def publish_result(self):
        # 新增：随机选一张图片
        test_img_path = random.choice(self.img_paths)
        
        # 模型推理
        results = self.model.predict(test_img_path, imgsz=IMG_SIZE)
        res = results[0]
        
        # 解析结果（类别+准确度）
        msg_content = f"检测图片：{os.path.basename(test_img_path)}\n"  # 新增：显示当前检测的图片名
        for idx, box in enumerate(res.boxes):
            cls_name = CLASS_NAMES[int(box.cls[0])]
            confidence = box.conf[0].item()
            msg_content += f"目标{idx+1}：{cls_name} | 准确度：{confidence:.4f}\n"
        
        # 发布消息
        msg = String()
        msg.data = msg_content if msg_content else "未检测到目标"
        self.pub.publish(msg)
        self.get_logger().info(f"发布结果：\n{msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = YoloPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
