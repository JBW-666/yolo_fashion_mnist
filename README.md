# 🎯 YOLO Fashion MNIST - YOLOv8 目标检测项目

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?logo=PyTorch&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Latest-brightgreen)
![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)

[English](README_en.md) | [中文](README.md)

</div>

## 📋 项目概述

本项目使用 **YOLOv8** 对 **Fashion MNIST** 数据集进行目标检测模型的训练和部署。结合 **ROS2** 框架实现实时目标检测和发布订阅机制。

### 主要特性

- ✅ Fashion MNIST 数据到 YOLO 格式的自动转换
- ✅ YOLOv8 模型的训练、评估和推理
- ✅ ROS2 节点实现实时推理发布
- ✅ 预训练模型和完整数据集
- ✅ Jupyter Notebook 交互式教程

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/JBW-666/yolo_fashion_mnist.git
cd yolo_fashion_mnist
```

### 2. 下载数据和模型（必要）

> 数据集和模型权重存储在 GitHub Release 中

**方式 A：自动下载**

```bash
# 下载所有数据和模型
wget https://github.com/JBW-666/yolo_fashion_mnist/releases/download/v1.0/yolo_dataset.tar.gz
wget https://github.com/JBW-666/yolo_fashion_mnist/releases/download/v1.0/raw_data.tar.gz
wget https://github.com/JBW-666/yolo_fashion_mnist/releases/download/v1.0/models.tar.gz

# 解压
tar -xzf yolo_dataset.tar.gz
tar -xzf raw_data.tar.gz
tar -xzf models.tar.gz
```

**方式 B：手动下载**

访问 Release 页面下载：https://github.com/JBW-666/yolo_fashion_mnist/releases/tag/v1.0

更多详情见 [数据下载指南](DATA_DOWNLOAD.md)

### 3. 环境配置

```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 4. 运行项目

```bash
# 查看数据集生成过程
jupyter notebook generate_dataset.ipynb

# 运行模型训练
jupyter notebook train_yolov8.ipynb

# 启动 ROS2 推理节点
source ros2_ws/install/setup.bash
ros2 run yolo_fashion_mnist yolo_pub
```

## 📁 项目结构

```
yolo_fashion_mnist/
├── README.md                      # 项目说明（本文件）
├── DATA_DOWNLOAD.md              # 数据下载指南
├── UPLOAD_SUMMARY.md             # 上传总结
├── fashion_mnist.yaml            # YOLO 配置文件
│
├── 📓 Jupyter Notebooks
├── generate_dataset.ipynb        # 数据集生成与转换
├── train_yolov8.ipynb            # 模型训练脚本
│
├── 📦 数据目录（下载后）
├── yolo_dataset/                 # YOLO格式数据集
│   ├── images/
│   │   ├── train/               # 训练图像
│   │   └── val/                 # 验证图像
│   └── labels/
│       ├── train/               # 训练标注
│       └── val/                 # 验证标注
├── raw_data/                     # 原始Fashion MNIST数据
├── runs/                         # 训练结果和权重
│
└── 🤖 ROS2 工作空间
    └── ros2_ws/
        ├── src/
        │   └── yolo_fashion_mnist/  # ROS2 包源码
        ├── build/                    # 编译产物
        ├── install/                  # 安装文件
        └── log/                      # 编译日志
```

## 🛠️ 功能模块

### 1. 数据集生成 (`generate_dataset.ipynb`)

自动将 Fashion MNIST 原始数据转换为 YOLO 格式：

```
Features:
- 下载 Fashion MNIST 数据
- 转换为 YOLO 标准格式
- 划分训练/验证集
- 生成数据集配置文件
```

### 2. 模型训练 (`train_yolov8.ipynb`)

使用 YOLOv8 训练目标检测模型：

```
Features:
- 模型选择（YOLOv8n/s/m/l/x）
- 参数微调
- 实时训练监控
- 模型验证和评估
- 权重保存和导出
```

### 3. ROS2 推理节点

实时推理和数据发布：

**Publisher 节点** (`publisher_node.py`)
- 读取本地图像或摄像头
- 运行 YOLO 推理
- 发布检测结果

**Subscriber 节点** (`subscriber_node.py`)
- 订阅推理结果
- 处理检测结果
- 可视化或记录

使用方法：
```bash
# 启动发布者
ros2 run yolo_fashion_mnist yolo_pub

# 启动订阅者（另一个终端）
ros2 run yolo_fashion_mnist yolo_sub
```

## 📊 数据集统计

| 指标 | 值 |
|------|-----|
| 类别数 | 10 (0-9) |
| 训练样本 | ~1000 |
| 验证样本 | ~200 |
| 图像分辨率 | 28×28px |
| 注释格式 | YOLO (txt) |

## 🎓 使用示例

### 推理单张图像

```python
from ultralytics import YOLO

# 加载模型
model = YOLO('runs/weights/best.pt')

# 推理
results = model.predict('path/to/image.jpg')

# 获取检测结果
for r in results:
    print(r.boxes)  # 包含坐标、置信度等信息
```

### 批量推理

```python
# 推理文件夹中的所有图像
results = model.predict('yolo_dataset/images/val/')
```

### 导出模型

```python
# 导出为 ONNX 格式
model.export(format='onnx')

# 导出为 TensorRT 格式
model.export(format='engine')
```

## 📈 训练结果

训练完成后，结果保存在 `runs/` 目录：

```
runs/
├── weights/
│   ├── best.pt      # 最佳模型
│   ├── last.pt      # 最后一个 epoch 的模型
│   └── epoch*.pt    # 各 epoch 的模型
├── results.csv      # 训练指标 CSV
├── args.yaml        # 训练参数
└── [其他可视化文件]
```

关键指标：
- **mAP@0.5**: 平均精度 (IoU=0.5)
- **Precision**: 精确率
- **Recall**: 召回率
- **F1-Score**: F1 分数

## 🔧 配置文件

### `fashion_mnist.yaml`

YOLO 数据集配置：

```yaml
path: /path/to/yolo_dataset
train: images/train
val: images/val

nc: 10  # 类别数
names: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
```

## 📝 依赖项

- Python 3.8+
- PyTorch 1.9+
- ultralytics (YOLOv8)
- ROS2 Humble
- numpy, pandas, matplotlib 等

详见 `requirements.txt`

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

- GitHub: [@JBW-666](https://github.com/JBW-666)
- Issues: [GitHub Issues](https://github.com/JBW-666/yolo_fashion_mnist/issues)

## 📚 参考资源

- [YOLOv8 官方文档](https://docs.ultralytics.com/)
- [Fashion MNIST 数据集](https://github.com/zalandoresearch/fashion-mnist)
- [ROS2 官方文档](https://docs.ros.org/en/humble/)

---

**项目更新时间**: 2026-01-18

**版本**: v1.0

**状态**: ✅ Active

<div align="center">

⭐ 如果这个项目对你有帮助，请给个 Star！

</div>
