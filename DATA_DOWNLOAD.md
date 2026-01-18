# 数据集和模型文件下载指南

本项目的大文件（数据集、模型权重）存储在 GitHub Releases 中。

## 下载方式

### 方式1：手动下载（推荐）

访问 GitHub Releases 页面下载文件：
```
https://github.com/JBW-666/yolo_fashion_mnist/releases
```

可用文件：
- `yolo_dataset.tar.gz` (2.4M) - YOLO格式的数据集
- `raw_data.tar.gz` (30M) - 原始Fashion MNIST数据
- `models.tar.gz` (43M) - 训练好的模型和权重

### 方式2：自动脚本下载

```bash
#!/bin/bash
cd /path/to/yolo_fashion_mnist

# 下载数据集
wget https://github.com/JBW-666/yolo_fashion_mnist/releases/download/v1.0/yolo_dataset.tar.gz
tar -xzf yolo_dataset.tar.gz

# 下载原始数据
wget https://github.com/JBW-666/yolo_fashion_mnist/releases/download/v1.0/raw_data.tar.gz
tar -xzf raw_data.tar.gz

# 下载模型
wget https://github.com/JBW-666/yolo_fashion_mnist/releases/download/v1.0/models.tar.gz
tar -xzf models.tar.gz
```

## 文件说明

### yolo_dataset.tar.gz
- YOLO8格式的标注数据
- 包含 train 和 val 两个子集
- labels/ 目录下为.txt格式的标注文件

### raw_data.tar.gz  
- Fashion MNIST 原始数据集
- 包含训练集和测试集的原始图像数据

### models.tar.gz
- 预训练的YOLOv8n模型
- 训练结果和权重文件
- runs/ 目录下为训练日志

## 项目结构

```
yolo_fashion_mnist/
├── fashion_mnist.yaml      # YOLO数据集配置
├── generate_dataset.ipynb  # 数据集生成脚本
├── train_yolov8.ipynb      # 模型训练脚本
├── yolo_dataset/           # YOLO格式数据集（下载后）
├── raw_data/               # 原始数据（下载后）
├── runs/                   # 训练结果（下载后）
└── ros2_ws/                # ROS2工作空间
```

## 环境配置

1. 克隆仓库：
```bash
git clone https://github.com/JBW-666/yolo_fashion_mnist.git
cd yolo_fashion_mnist
```

2. 下载数据和模型（见上面的脚本）

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行训练或推理：
```bash
jupyter notebook train_yolov8.ipynb
```
