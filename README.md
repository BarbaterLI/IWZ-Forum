# IWZ-Forum论坛系统

[![License](https://img.shields.io/github/license/BarbaterLI/IWZ-Forum)](LICENSE)
[![Version](https://img.shields.io/github/v/tag/BarbaterLI/IWZ-Forum?sort=semver)](https://github.com/BarbaterLI/IWZ-Forum/releases)
[![Release](https://img.shields.io/github/downloads/BarbaterLI/IWZ-Forum/total)](https://github.com/BarbaterLI/IWZ-Forum/releases)
[![Stars](https://img.shields.io/github/stars/BarbaterLI/IWZ-Forum?style=social)](https://github.com/BarbaterLI/IWZ-Forum)
[![Forks](https://img.shields.io/github/forks/BarbaterLI/IWZ-Forum?style=social)](https://github.com/BarbaterLI/IWZ-Forum)
[![Issues](https://img.shields.io/github/issues/BarbaterLI/IWZ-Forum)](https://github.com/BarbaterLI/IWZ-Forum/issues)
[![Last Commit](https://img.shields.io/github/last-commit/BarbaterLI/IWZ-Forum)](https://github.com/BarbaterLI/IWZ-Forum/commits/main)

一个功能完整的基于Flask和SQLite的论坛系统，具有现代化的用户界面和丰富的功能。

## 版本
0.0.1 (rc)

## 功能特性

### 用户系统
- 用户注册/登录认证
- 个人资料管理（头像、个人简介）
- 密码找回功能
- 管理员权限系统

### 内容管理
- 帖子发布、编辑、删除
- 评论与回复系统
- 版块分类管理
- 标签系统
- 精华帖推荐
- 全文搜索功能

### 社交功能
- 好友系统（添加/移除好友）
- 私信聊天功能
- 关注/粉丝系统
- 用户黑名单管理
- @提醒功能
- 收藏夹管理
- 点赞/踩功能

### 高级功能
- 投票系统
- 举报处理机制
- 后台管理面板
- 数据统计与分析
- 互动历史记录

## 管理功能
- 用户管理（查看、删除用户）
- 版块管理（创建、编辑、删除版块）
- 帖子管理（查看、删除帖子）
- 举报处理（处理或忽略举报）
- 数据统计（用户、帖子、评论增长图表）

## 技术栈

- **后端**: Flask + SQLite
- **前端**: Bootstrap 5 + Jinja2模板
- **样式**: CSS3 + JavaScript，支持深色/浅色主题切换
- **图标**: Font Awesome + Bootstrap Icons

## 安装与运行

### 环境要求
- Python 3.7+
- pip包管理器

### 安装步骤

1. 克隆项目到本地：
```bash
git clone https://github.com/BarbaterLI/IWZ-Forum.git
cd flask-forum
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 初始化数据库：
```bash
python init_db.py
```

5. 运行应用：
```bash
python app.py
```

6. 在浏览器中访问 `http://localhost:5000`

## 项目结构

```
flask-forum/
├── app.py                 # 应用入口
├── config.py              # 配置文件
├── extensions.py          # Flask扩展
├── init_db.py             # 数据库初始化
├── requirements.txt       # 依赖列表
├── README.md              # 说明文档
├── models.py              # 数据模型
├── routes.py              # 主要路由
├── routes_advanced.py     # 高级功能路由
├── static/                # 静态资源
│   ├── css/
│   ├── js/
│   └── images/
└── templates/             # 模板文件
    ├── admin/             # 后台管理模板
    └── ...                # 其他模板
```


## 许可证

AGPL V3 License

## 联系方式

本项目随缘更新,并且不修bug,使用出现问题概不负责.

