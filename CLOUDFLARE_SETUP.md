# Cloudflare DNS 配置指南 - chinaorus.com

## 服务器信息

- **EC2 公网 IP**: `18.219.201.185`
- **前端端口**: `5173`
- **后端端口**: `8080`

---

## 第一步：在 EC2 Security Group 开放端口

在 AWS EC2 控制台中，为你的实例的 Security Group 添加以下入站规则：

| 类型 | 协议 | 端口范围 | 源 | 描述 |
|------|------|----------|-----|------|
| Custom TCP | TCP | 5173 | 0.0.0.0/0 | Frontend |
| Custom TCP | TCP | 8080 | 0.0.0.0/0 | Backend API |

**注意**：如果你已经配置了 Nginx 反向代理在 80/443 端口，则只需开放 80 和 443 端口即可。

---

## 第二步：Cloudflare DNS 配置

### 方式一：快速配置（推荐）

1. 登录 Cloudflare Dashboard: https://dash.cloudflare.com/
2. 选择域名 `chinaorus.com`
3. 点击左侧菜单 "DNS" → "Records"
4. 点击 "Add record" 按钮
5. 填写以下信息：

**主域名配置：**
```
Type: A
Name: @
IPv4 address: 18.219.201.185
Proxy status: Proxied (橙色云朵图标)
TTL: Auto
```

**www 子域名配置（可选）：**
```
Type: A
Name: www
IPv4 address: 18.219.201.185
Proxy status: Proxied (橙色云朵图标)
TTL: Auto
```

6. 点击 "Save"

### 方式二：仅 DNS 解析（无 CDN）

如果你不需要 Cloudflare 的 CDN 和 DDoS 保护，可以设置为 "DNS only"：

```
Type: A
Name: @
IPv4 address: 18.219.201.185
Proxy status: DNS only (灰色云朵图标)
TTL: Auto
```

---

## 第三步：SSL/TLS 配置

### 如果选择了 "Proxied" 模式：

1. 在 Cloudflare Dashboard 中，点击 "SSL/TLS"
2. 选择加密模式：

**快速上线（推荐）：**
- 选择 "Flexible" - 访客到 Cloudflare 使用 HTTPS，Cloudflare 到你的服务器使用 HTTP
- 优点：无需在服务器配置 SSL 证书
- 缺点：服务器到 Cloudflare 之间是 HTTP（但通常安全）

**更安全的配置（需要服务器 SSL）：**
- 选择 "Full (strict)" - 全程 HTTPS 加密
- 需要在你的服务器上配置有效的 SSL 证书（可使用 Let's Encrypt）

3. 保存设置

---

## 第四步：配置端口重定向（重要）

由于你的应用运行在 5173 端口，但用户访问域名默认使用 80/443 端口，你需要：

### 选项 A：修改 Docker 配置（简单）

编辑 `docker-compose.yml`，将前端端口改为 80：

```yaml
  frontend:
    ports:
      - "80:5173"  # 改为 80 端口
```

然后重启：
```bash
./manage.sh rebuild
```

**Security Group 需要开放**：80 端口

### 选项 B：使用 Nginx 反向代理（推荐）

在 EC2 上配置 Nginx 作为反向代理（假设你已经安装了 Nginx）：

1. 创建配置文件 `/etc/nginx/sites-available/chinaorus.com`：

```nginx
server {
    listen 80;
    server_name chinaorus.com www.chinaorus.com;

    # 前端
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
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

2. 启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/chinaorus.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Security Group 需要开放**：80 和 443 端口（5173 和 8080 可以关闭）

---

## 第五步：验证配置

### 1. 测试直接 IP 访问（在配置 DNS 之前）

```bash
# 测试前端
curl http://18.219.201.185:5173

# 测试后端 API
curl http://18.219.201.185:8080/api/questions
```

### 2. 等待 DNS 生效

DNS 传播通常需要几分钟到 48 小时，可以使用以下工具检查：

- https://dnschecker.org/
- 在终端执行：`nslookup chinaorus.com`

### 3. 测试域名访问

DNS 生效后，访问：

- **前端**: https://chinaorus.com (如果使用 Cloudflare Proxied)
- **前端**: http://chinaorus.com (如果使用 DNS only)
- **API**: https://chinaorus.com/api/questions

---

## 故障排查

### DNS 未生效
- 检查 Cloudflare DNS 记录是否正确添加
- 使用 `dig chinaorus.com` 或 `nslookup chinaorus.com` 检查 DNS 解析
- 清除浏览器缓存或使用隐私模式

### 无法访问（DNS 已生效）
- 检查 EC2 Security Group 是否开放了相应端口
- 检查 Docker 容器是否正常运行：`docker-compose ps`
- 查看日志：`docker-compose logs -f`

### SSL 证书错误
- 如果使用 Cloudflare "Flexible" 模式，确保 SSL/TLS 设置正确
- 如果使用 "Full (strict)" 模式，确保服务器上有有效的 SSL 证书

### 端口无法访问
```bash
# 检查端口是否在监听
sudo netstat -tlnp | grep -E '80|443|5173|8080'

# 检查防火墙
sudo ufw status
```

---

## 推荐配置总结

**最简单的配置（5分钟上线）：**
1. EC2 Security Group 开放 5173 端口
2. Cloudflare 添加 A 记录指向 `18.219.201.185`，选择 "DNS only"
3. 访问 `http://chinaorus.com:5173`

**推荐的生产配置（专业）：**
1. EC2 Security Group 开放 80 和 443 端口
2. 配置 Nginx 反向代理
3. Cloudflare 添加 A 记录，选择 "Proxied"
4. SSL/TLS 选择 "Flexible"
5. 访问 `https://chinaorus.com`

---

## 需要帮助？

如果遇到问题，可以：
1. 查看容器日志：`./manage.sh logs`
2. 检查容器状态：`./manage.sh status`
3. 重启服务：`./manage.sh restart`
