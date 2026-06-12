# GitHub Actions 自动构建部署指南

## 自动构建已配置完成

GitHub Actions 工作流文件已创建在 `.github/workflows/docker-build.yml`

## 启用自动构建的步骤

### 步骤 1：在 GitHub 启用 Actions

1. 访问 https://github.com/guifengxiaoyan/DockerAutoBaomiGuan/actions
2. 如果是第一次使用，会看到提示信息
3. 点击 **"I understand my workflows, go ahead and enable them"** 按钮

### 步骤 2：验证配置

Actions 启用后，每次 push 到 master 分支都会自动触发构建。

### 步骤 3：手动触发一次构建（可选）

1. 访问 https://github.com/guifengxiaoyan/DockerAutoBaomiGuan/actions/workflows/docker-build.yml
2. 点击右侧的 **"Run workflow"** 按钮
3. 选择 `master` 分支
4. 点击 **"Run workflow"**

### 步骤 4：查看构建进度

- 在 Actions 页面可以看到构建状态
- 成功构建后会看到绿色的 ✅
- 点击任务可以查看详细的构建日志

### 步骤 5：查看 Docker Hub 镜像

构建成功后，镜像会自动推送到 Docker Hub：
https://hub.docker.com/r/guifengxiaoyan/autobaomiguan

## 飞牛 NAS 使用方法

### 方式 1：Docker 管理器（推荐）

1. 打开飞牛 NAS **Docker 管理器**
2. 在镜像仓库中搜索：`guifengxiaoyan/autobaomiguan`
3. 点击 **下载** 按钮
4. 标签选择：`latest`
5. 下载完成后创建容器：
   - 容器名称：`autobaomiguan`
   - 端口映射：本机 `3000` → 容器 `3000`
   - 网络模式：`bridge`
   - 重启策略：`除非手动停止，否则自动重启`
6. 启动容器
7. 访问：`http://你的NAS IP:3000`

### 方式 2：命令行

```bash
docker run -d \
  --name autobaomiguan \
  -p 3000:3000 \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  guifengxiaoyan/autobaomiguan:latest
```

### 方式 3：Docker Compose

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  autobaomiguan:
    image: guifengxiaoyan/autobaomiguan:latest
    container_name: autobaomiguan
    ports:
      - "3000:3000"
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
```

运行：
```bash
docker-compose up -d
```

## 镜像信息

| 项目 | 值 |
|------|------|
| 镜像名称 | `guifengxiaoyan/autobaomiguan` |
| 标签 | `latest`, `master`, `sha-{短 ID}`, `v{版本号}` |
| 架构支持 | `linux/amd64`, `linux/arm64` |
| 镜像大小 | 约 150MB |

## 自动构建触发条件

- push 到 `master` 分支
- 推送 `v*` 格式的 tags（如 `v1.0.0`）
- 手动触发 workflow（通过 GitHub Actions 页面）

## 版本标签说明

| 标签类型 | 示例 | 说明 |
|----------|------|------|
| 分支标签 | `master` | master 分支的最新构建 |
| 版本标签 | `v1.0.0` | 推送的 tag 版本 |
| SHA 标签 | `sha-abc1234` | 每次提交的短 SHA |
| 最新标签 | `latest` | master 分支默认标签 |

## 故障排查

### 构建失败

1. 查看 Actions 日志
2. 确认 Docker Hub 凭证正确
3. 检查网络连接

### 镜像拉取失败

1. 确认 Docker Hub 镜像存在：https://hub.docker.com/r/guifengxiaoyan/autobaomiguan
2. 检查网络是否可以访问 Docker Hub
3. 尝试手动拉取：`docker pull guifengxiaoyan/autobaomiguan:latest`

### NAS 上无法访问

1. 确认容器正在运行：`docker ps`
2. 检查端口是否被占用：`netstat -tlnp | grep 3000`
3. 检查 NAS 防火墙设置
4. 查看容器日志：`docker logs autobaomiguan`

## 安全建议

- ✅ 仅在局域网内访问
- ✅ 使用 NAS 自带的防火墙
- ✅ 如需外网访问，配置 Nginx 反向代理 + HTTPS
- ✅ 定期更新镜像获取安全补丁

## 更新镜像

```bash
# 拉取最新镜像
docker pull guifengxiaoyan/autobaomiguan:latest

# 停止旧容器
docker stop autobaomiguan
docker rm autobaomiguan

# 启动新容器
docker run -d -p 3000:3000 --name autobaomiguan guifengxiaoyan/autobaomiguan:latest
```

## 相关链接

- GitHub 仓库：https://github.com/guifengxiaoyan/DockerAutoBaomiGuan
- GitHub Actions：https://github.com/guifengxiaoyan/DockerAutoBaomiGuan/actions
- Docker Hub：https://hub.docker.com/r/guifengxiaoyan/autobaomiguan
- Web 应用源码：https://github.com/guifengxiaoyan/WEBAutoBaomiGuan

---

如有问题，请在 GitHub 提交 Issue。
