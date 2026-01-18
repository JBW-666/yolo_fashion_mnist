#!/bin/bash

# GitHub Release 上传脚本
# 使用方式: bash upload_to_release.sh <github_token> <tag_name>

GITHUB_TOKEN=$1
TAG_NAME=${2:-v1.0}
OWNER="JBW-666"
REPO="yolo_fashion_mnist"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "使用方式: bash upload_to_release.sh <github_token> [tag_name]"
    echo "github_token 可从 https://github.com/settings/tokens 获取"
    exit 1
fi

echo "准备上传文件到 Release: $TAG_NAME"

# 检查文件
echo "检查压缩文件..."
ls -lh yolo_dataset.tar.gz raw_data.tar.gz models.tar.gz 2>/dev/null

# 创建 Release（如果不存在）
echo "创建或更新 Release: $TAG_NAME"
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d "{
    \"tag_name\": \"$TAG_NAME\",
    \"name\": \"Dataset and Models - $TAG_NAME\",
    \"body\": \"Complete dataset and pre-trained models for YOLO Fashion MNIST project.\",
    \"draft\": false,
    \"prerelease\": false
  }" 2>/dev/null

echo "Release 创建/更新完成"

# 上传文件函数
upload_file() {
    local file=$1
    echo "上传文件: $file"
    
    UPLOAD_URL=$(curl -s \
      -H "Authorization: token $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/repos/$OWNER/$REPO/releases/tags/$TAG_NAME | \
      grep '"upload_url"' | sed -E 's/.*"([^"]+)".*/\1/' | sed 's/{?name,label}//')
    
    if [ -z "$UPLOAD_URL" ]; then
        echo "错误: 无法获取上传 URL"
        return 1
    fi
    
    curl -X POST \
      -H "Authorization: token $GITHUB_TOKEN" \
      -H "Content-Type: application/gzip" \
      --data-binary @"$file" \
      "${UPLOAD_URL}?name=$(basename $file)" \
      --progress-bar
    
    echo "文件 $file 上传完成"
}

# 上传所有文件
for file in yolo_dataset.tar.gz raw_data.tar.gz models.tar.gz; do
    if [ -f "$file" ]; then
        upload_file "$file"
    else
        echo "警告: 文件 $file 不存在"
    fi
done

echo ""
echo "上传完成！"
echo "下载地址: https://github.com/$OWNER/$REPO/releases/tag/$TAG_NAME"
