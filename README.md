# 保密观自动刷课 - Web 版

基于 [AutoBaomiGuan](https://github.com/vay1314/AutoBaomiGuan) 项目开发的在线 Web 版本。

## 功能特性

- 多账号登录，token 自动缓存
- 查看课程目录与学习进度
- 一键学习所有课程
- 自动完成课程考试（满分）
- 响应式 UI 设计，支持手机和电脑访问

## 在线访问

**预览地址**: https://3000-a37ea19e371a1a3c.monkeycode-ai.online

## 本地运行

### 安装依赖

```bash
pip install -r requirements.txt flask flask-cors --break-system-packages
```

### 启动服务

```bash
python3 app.py
```

服务启动后可以访问：http://localhost:3000

## 项目结构

```
/workspace
├── app.py              # Flask 后端服务
├── index.html          # 前端页面
├── api_handlers.py     # API 处理函数
├── config.py           # 配置文件
├── login.py            # 登录模块
├── course.py           # 课程管理模块
└── requirements.txt    # Python 依赖
```

## 使用说明

1. **登录账号**
   - 输入用户名和密码
   - 点击登录按钮
   - 登录成功后 token 会自动保存

2. **切换账号**
   - 已保存的账号会显示在登录页面
   - 点击账号即可快速切换

3. **学习课程**
   - 登录后自动加载课程列表
   - 可以逐个学习课程
   - 也可以点击"一键学习所有课程"批量完成

4. **查看进度**
   - 页面顶部显示总课程数、已完成数量和完成率
   - 课程列表中显示每个课程的学习状态

## 注意事项

- 本工具仅供学习交流使用
- 请使用合法合规的账号进行刷课
- 请勿滥用工具影响平台正常运营
