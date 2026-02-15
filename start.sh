#!/bin/bash

echo "Building and starting ChinaOrUS application..."

# 停止并删除旧容器
docker-compose down

# 构建并启动容器
docker-compose up -d --build

# 显示容器状态
echo ""
echo "Containers status:"
docker-compose ps

echo ""
echo "Application is starting..."
echo "Frontend: http://your-server:5173"
echo "Backend API: http://your-server:8080"
echo ""
echo "View logs with: docker-compose logs -f"
