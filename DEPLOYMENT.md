# ChinaOrUS 部署文档

## 端口配置

- **Frontend (前端)**: 5173
- **Backend API (后端)**: 8080

## Docker 管理

### 启动服务
```bash
./manage.sh start
# 或
docker-compose up -d
```

### 停止服务
```bash
./manage.sh stop
# 或
docker-compose down
```

### 查看日志
```bash
./manage.sh logs
# 或
docker-compose logs -f
```

### 查看状态
```bash
./manage.sh status
# 或
docker-compose ps
```

### 重新构建
```bash
./manage.sh rebuild
# 或
docker-compose up -d --build
```

## EC2 Security Group 配置

需要在 AWS EC2 Security Group 中开放以下端口：

1. **5173** (TCP) - 前端访问
2. **8080** (TCP) - 后端 API（可选，如果前端通过 nginx 代理则不需要对外开放）

## Cloudflare DNS 配置

### 步骤 1: 登录 Cloudflare
1. 访问 https://dash.cloudflare.com/
2. 选择你的域名 `chinaorus.com`

### 步骤 2: 添加 A 记录
1. 点击 "DNS" 标签
2. 点击 "Add record" 按钮
3. 配置如下：
   - **Type**: A
   - **Name**: @ (根域名) 或 www (子域名)
   - **IPv4 address**: [你的 EC2 公网 IP]
   - **Proxy status**:
     - 如果需要 Cloudflare CDN 加速和 DDoS 保护，选择 "Proxied" (橙色云朵)
     - 如果只需要 DNS 解析，选择 "DNS only" (灰色云朵)
   - **TTL**: Auto

4. 点击 "Save"

### 步骤 3: SSL/TLS 配置（如果使用 Cloudflare Proxy）
1. 点击 "SSL/TLS" 标签
2. 选择加密模式：
   - **Flexible**: Cloudflare 到用户之间使用 HTTPS，Cloudflare 到服务器使用 HTTP
   - **Full**: 需要在服务器上配置自签名证书
   - **Full (strict)**: 需要在服务器上配置有效的 SSL 证书

推荐使用 "Flexible" 模式以快速上线。

### 步骤 4: 配置 Nginx 反向代理（推荐）

为了更好的生产环境配置，建议使用 Nginx 作为反向代理：

```nginx
server {
    listen 80;
    server_name chinaorus.com www.chinaorus.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 访问方式

配置完成后，可以通过以下方式访问：

1. **直接访问**:
   - http://[EC2-IP]:5173 (前端)
   - http://[EC2-IP]:8080 (后端 API)

2. **域名访问**（DNS 配置生效后）:
   - http://chinaorus.com (前端)
   - http://chinaorus.com/api (后端 API)

## 数据持久化

数据库文件保存在 `./backend/decision_matrix.db`，已通过 Docker volume 挂载，容器重启不会丢失数据。

## 更新应用

1. 拉取最新代码
```bash
cd /home/ubuntu/code/ChinaOrUS
git pull
```

2. 重新构建并启动
```bash
./manage.sh rebuild
```

## 故障排查

### 查看容器日志
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 检查端口占用
```bash
netstat -tlnp | grep -E '5173|8080'
```

### 重启服务
```bash
./manage.sh restart
```
