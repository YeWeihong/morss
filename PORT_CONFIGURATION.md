# Docker 端口配置说明

## 问题

**Q: 这个项目部署到 Docker 的端口一定是 8000 吗？**

A: 不是的。默认端口是 8000，但你可以轻松修改为任何你想要的端口。

**Q: 如果我想修改占用的端口该怎么修改？比如我现在想修改使用 18000 的端口**

A: 有多种方法可以修改端口，下面详细说明。

---

## 理解 Docker 端口映射

Docker 端口配置格式为：`主机端口:容器端口`

- **主机端口**（冒号前）：你在主机上访问的端口
- **容器端口**（冒号后）：容器内部应用监听的端口

例如：`18000:8000` 表示：
- 主机的 18000 端口映射到容器的 8000 端口
- 你通过 `http://localhost:18000` 访问服务
- 容器内部应用仍然在 8000 端口监听

---

## 修改端口的方法

### 方法一：使用环境变量（推荐）

最简单的方法，不需要修改任何配置文件。

```bash
# 设置环境变量并启动
HOST_PORT=18000 docker compose up -d

# 访问服务
# 浏览器打开：http://localhost:18000
```

或者创建 `.env` 文件：

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，修改 HOST_PORT 的值
# HOST_PORT=18000

# 启动服务
docker compose up -d

# 访问服务
# 浏览器打开：http://localhost:18000
```

### 方法二：修改 docker-compose.yml

直接编辑 `docker-compose.yml` 文件中的 `ports` 配置：

```yaml
services:
  morss:
    image: pictuga/morss
    container_name: morss
    ports:
      - "18000:8000"  # 修改这里的主机端口（冒号前的数字）
```

然后启动：

```bash
docker compose up -d

# 访问服务
# 浏览器打开：http://localhost:18000
```

### 方法三：直接使用 docker run

不使用 docker-compose，直接运行容器：

```bash
# 使用官方镜像
docker run -d -p 18000:8000 --name morss pictuga/morss

# 或使用本地构建的镜像
docker run -d -p 18000:8000 --name morss morss:custom

# 访问服务
# 浏览器打开：http://localhost:18000
```

---

## 完整示例：使用 18000 端口

### 示例 1：快速启动（使用环境变量）

```bash
# 克隆仓库
git clone https://github.com/YeWeihong/morss.git
cd morss

# 使用 18000 端口启动
HOST_PORT=18000 docker compose up -d

# 查看日志
docker compose logs -f

# 测试访问
curl http://localhost:18000/

# 停止服务
docker compose down
```

### 示例 2：使用 .env 文件

```bash
# 克隆仓库
git clone https://github.com/YeWeihong/morss.git
cd morss

# 创建配置文件
cp .env.example .env

# 编辑 .env 文件
# 修改这一行：HOST_PORT=18000
nano .env

# 启动服务
docker compose up -d

# 访问：http://localhost:18000/
```

### 示例 3：不使用 docker-compose

```bash
# 直接运行容器
docker run -d \
  -p 18000:8000 \
  --name morss \
  -e CACHE=diskcache \
  -e DISKCACHE_DIR=/cache \
  -v ./morss-cache:/cache \
  pictuga/morss

# 查看日志
docker logs -f morss

# 访问：http://localhost:18000/

# 停止容器
docker stop morss
docker rm morss
```

---

## 常见问题

### Q1: 我可以同时运行多个 Morss 实例吗？

可以！只需要使用不同的主机端口和容器名称：

```bash
# 第一个实例（端口 8000）
docker run -d -p 8000:8000 --name morss-1 pictuga/morss

# 第二个实例（端口 18000）
docker run -d -p 18000:8000 --name morss-2 pictuga/morss

# 第三个实例（端口 28000）
docker run -d -p 28000:8000 --name morss-3 pictuga/morss
```

### Q2: 如何修改容器内部端口（而不是主机端口）？

通常不需要修改容器内部端口，但如果需要，可以设置 `PORT` 环境变量：

```bash
docker run -d \
  -p 18000:9000 \
  -e PORT=9000 \
  --name morss \
  pictuga/morss
```

注意：这种情况下端口映射要改为 `18000:9000`（主机端口:容器内部端口）

### Q3: 端口被占用怎么办？

如果端口已被其他程序占用，选择一个不同的端口：

```bash
# 检查端口占用情况
netstat -tlnp | grep 18000
# 或
lsof -i :18000

# 选择一个未被占用的端口
HOST_PORT=19000 docker compose up -d
```

### Q4: 修改端口后无法访问怎么办？

检查以下几点：

1. 确认容器正在运行：
   ```bash
   docker ps | grep morss
   ```

2. 检查端口映射是否正确：
   ```bash
   docker port morss
   ```

3. 检查防火墙设置：
   ```bash
   # 允许端口通过防火墙（如果使用 ufw）
   sudo ufw allow 18000
   
   # 或使用 firewalld
   sudo firewall-cmd --permanent --add-port=18000/tcp
   sudo firewall-cmd --reload
   ```

4. 查看容器日志：
   ```bash
   docker logs morss
   ```

---

## 总结

- **默认端口**：8000
- **推荐修改方法**：使用 `HOST_PORT` 环境变量
- **端口格式**：`主机端口:容器端口`
- **示例**：使用 18000 端口 → `HOST_PORT=18000 docker compose up -d`

**重要**：修改的是**主机端口**（对外访问的端口），容器内部默认使用 8000 端口，通常不需要修改。
