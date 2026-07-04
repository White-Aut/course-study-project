# 掘金头条-黑马FASTAPI课程-后端

> 基于 **FastAPI** 的新闻头条后端服务，黑马程序员 FastAPI 课程项目。

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| **FastAPI** | Web 框架 |
| **SQLAlchemy 2.0 (async)** | ORM |
| **MySQL + aiomysql** | 异步数据库驱动 |
| **Redis** | 缓存 |
| **passlib + bcrypt** | 密码加密 |
| **Pydantic v2** | 数据校验 |
| **Uvicorn** | ASGI 服务器 |

## 📦 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/White-Aut/course-study-portfolio.git
cd course-study-portfolio/掘金头条-黑马FASTAPI课程-后端
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的数据库密码等信息
```

### 5. 启动服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

## 📁 项目结构

```
├── main.py                  # 应用入口
├── config/                  # 配置
│   ├── db_conf.py           # 数据库配置
│   ├── cache_conf.py        # Redis 配置
│   └── cache/
│       └── news_cache.py    # 新闻缓存策略
├── models/                  # SQLAlchemy 数据模型
│   ├── base.py              # 基类
│   ├── users.py             # 用户模型
│   ├── news.py              # 新闻/分类模型
│   ├── favorite.py          # 收藏模型
│   └── history.py           # 浏览历史模型
├── schemas/                 # Pydantic 请求/响应模型
├── crud/                    # 数据库操作
├── routers/                 # API 路由
└── utils/                   # 工具函数
    ├── auth.py              # 认证
    ├── security.py          # 密码加密
    ├── response.py          # 统一响应
    ├── exception.py         # 异常定义
    └── exception_handlers.py# 异常处理注册
```

## 📡 API 概览

| 模块 | 前缀 | 说明 |
|------|------|------|
| 用户 | `/api/user` | 注册、登录、信息、修改密码 |
| 新闻 | `/api/news` | 分类列表、新闻列表、新闻详情 |
| 收藏 | `/api/favorite` | 收藏/取消收藏/收藏列表 |
| 历史 | `/api/history` | 浏览历史记录 |

## ⚠️ 注意

- 本项目仅为**后端 API**，不包含前端页面
- 需要提前创建 MySQL 数据库 `news_app`
- 需要本地运行 Redis 服务
