# AutoBaomiGuan Web - 保密观自动刷课 Web 版

基于 [AutoBaomiGuan](https://github.com/vay1314/AutoBaomiGuan) 项目开发的在线 Web 版本。

## 功能特性

- 多账号登录，token 自动缓存
- 一键学习所有课程
- 自动完成考试（满分）
- 实时学习日志
- 简洁的 Web 界面

## 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 克隆仓库
git clone https://github.com/guifengxiaoyan/WEBAutoBaomiGuan.git
cd WEBAutoBaomiGuan

# 使用 docker-compose 启动
docker-compose up -d

# 或者直接使用 docker 命令
docker build -t autobaomiguan .
docker run -d -p 3000:3000 --name autobaomiguan autobaomiguan
```

### 方式二：Python 直接运行

```bash
# 安装依赖
pip install -r requirements.txt flask flask-cors --break-system-packages

# 启动服务
python3 app.py
```

访问 http://localhost:3000 即可使用。

## Docker 部署说明

### 1. 构建镜像

```bash
docker build -t autobaomiguan .
```

### 2. 运行容器

```bash
docker run -d \
  -p 3000:3000 \
  -v $(pwd)/credentials.json:/app/credentials.json \
  --name autobaomiguan \
  autobaomiguan
```

### 3. 使用 docker-compose

```bash
docker-compose up -d
```

### 4. 查看日志

```bash
docker logs -f autobaomiguan
```

### 5. 停止服务

```bash
docker-compose down
# 或
docker stop autobaomiguan && docker rm autobaomiguan
```

## 使用说明

1. **登录账号**
   - 输入保密观账号和密码
   - 点击登录，token 会自动保存

2. **开始学习**
   - 点击"开始学习和考试"按钮
   - 系统会自动学习所有课程并完成考试

3. **查看进度**
   - 实时日志显示学习和考试进度
   - 点击"刷新进度"更新课程状态

4. **切换账号**
   - 已保存的账号会显示在登录页面
   - 点击账号即可快速切换

## 项目结构

```
/workspace
├── app.py              # Flask 后端服务
├── index.html          # 前端页面
├── api_handlers.py     # API 处理函数
├── config.py           # 配置文件
├── login.py            # 登录模块
├── course.py           # 课程管理模块
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 镜像配置
├── docker-compose.yml  # Docker Compose 配置
└── .dockerignore       # Docker 忽略文件
```

## 配置说明

`config.py` 主要字段：

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `course_packet_id` | 课程 ID | 2026 年度培训 ID |
| `CREDENTIALS_FILE` | 凭证缓存文件 | credentials.json |

## 注意事项

- 本工具仅供学习交流使用
- 请使用合法合规的账号
- 请勿滥用工具影响平台正常运营
- Docker 部署时，凭证文件会持久化保存

## 相关项目

- 原始项目：https://github.com/vay1314/AutoBaomiGuan
- Docker 版本：https://github.com/guifengxiaoyan/DockerAutoBaomiGuan

## License

MIT License
