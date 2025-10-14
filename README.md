## 🚀 DNS 一致性检查工具 (Docker 部署)

这是一个基于 Flask 和 Gunicorn 构建的 DNS 解析一致性检查工具。它允许用户输入一个域名和一组 DNS 服务器 IP 地址，然后并发查询这些服务器的 A 记录，并对比结果以发现不一致的解析情况。

**核心特性：**

- **客户端存储：** DNS 服务器列表配置保存在浏览器本地（LocalStorage），确保每个用户配置独立。
    
- **多列表管理：** 支持保存和切换多个自定义 DNS 服务器 IP 列表。
    
- **生产部署：** 使用 Gunicorn 和 Nginx（在同一个 Docker 容器内通过 Supervisor 管理）进行生产部署。
    

### 📋 技术栈

- **后端框架:** Python / Flask
    
- **DNS 库:** dnspython
    
- **WSGI 服务器:** Gunicorn
    
- **反向代理/Web Server:** Nginx
    
- **容器化:** Docker
    
- **进程管理:** Supervisor (用于单容器运行 Nginx 和 Gunicorn)
    
- **配置存储:** 浏览器 LocalStorage
    

---

### 📦 部署指南（推荐使用 Docker）

最简单和推荐的部署方式是使用 Docker 容器，它将应用程序、Nginx 和所有依赖项都封装在一个可移植的镜像中。

**镜像名称:** `gujian803/dns-checker:latest

#### 1. 使用 Docker 命令一键部署

运行以下命令，即可在宿主机的 **8095** 端口启动服务：

Bash

```
docker run -d \
    --restart=always \
    -p 8095:8095 \
    --name dns-checker-app \
    gujian803/dns-checker:latest
```

#### 2. 访问应用

如果您的服务器 IP 是 `192.168.1.10`，则通过浏览器访问：

```
http://192.168.1.10:8095
```

