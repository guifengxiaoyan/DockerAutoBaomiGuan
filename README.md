# AutoBaomiGuan Web - 保密观自动刷课 Web 版

基于 [AutoBaomiGuan](https://github.com/vay1314/AutoBaomiGuan) 项目开发的在线 Web 版本。

## 功能特性

- 多账号登录，token 自动缓存
- 一键学习所有课程
- 自动完成考试（满分）
- 实时学习日志
- 简洁的 Web 界面

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt flask flask-cors --break-system-packages
```

### 启动服务

```bash
python3 app.py
```

访问 http://localhost:3000 即可使用。

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
└── README.md           # 项目说明
```

## 配置说明

`config.py` 主要字段：

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `course_packet_id` | 课程 ID | 2026 年度培训 ID |
| `CREDENTIALS_FILE` | 凭证缓存文件 | credentials.json |

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/login` | POST | 用户登录 |
| `/api/accounts` | GET | 获取已保存的账号 |
| `/api/select-account` | POST | 切换账号 |
| `/api/course/list` | GET | 获取课程列表 |
| `/api/course/progress` | GET | 获取学习进度 |
| `/api/course/study-all` | POST | 一键学习所有课程 |

## 注意事项

- 本工具仅供学习交流使用
- 请使用合法合规的账号
- 请勿滥用工具影响平台正常运营

## 相关项目

- 原始项目：https://github.com/vay1314/AutoBaomiGuan

## License

MIT License
