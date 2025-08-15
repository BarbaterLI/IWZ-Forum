# IWZ-Forum 项目结构说明

## 项目概述
IWZ-Forum 是一个基于 Flask 和 SQLite 的现代化论坛系统，具有丰富的功能和美观的用户界面。

## 项目结构
```
IWZ-Forum/
├── app.py                 # Flask 应用入口
├── run.py                 # 应用运行脚本
├── config.py              # 配置文件
├── extensions.py          # Flask 扩展初始化
├── init_db.py             # 数据库初始化脚本
├── requirements.txt       # 项目依赖
├── README.md              # 项目说明文档
├── PROJECT_STRUCTURE.md   # 项目结构说明（当前文件）
├── models.py              # 数据模型定义
├── routes.py              # 主要路由处理
├── routes_advanced.py     # 高级功能路由处理
├── static/                # 静态资源文件夹
│   ├── css/
│   │   └── style.css      # 自定义样式
│   ├── js/
│   │   └── script.js      # 自定义JavaScript
│   ├── images/
│   │   ├── default-avatar.png
│   │   ├── default-avatar.png2
│   │   └── default-avatar.svg
│   ├── favicon.ico        # 网站图标
│   └── uploads/           # 用户上传文件
└── templates/             # Jinja2 模板文件夹
    ├── base.html          # 基础模板
    ├── index.html         # 首页
    ├── login.html         # 登录页面
    ├── register.html      # 注册页面
    ├── profile.html       # 用户个人中心
    ├── edit_profile.html  # 编辑个人资料
    ├── user_detail.html   # 用户资料页
    ├── categories.html    # 版块列表
    ├── category_detail.html # 版块详情
    ├── create_post.html   # 发帖页面
    ├── edit_post.html     # 编辑帖子
    ├── post_detail.html   # 帖子详情
    ├── search.html        # 搜索页面
    ├── friends.html       # 好友列表
    ├── messages.html      # 消息列表
    ├── message_detail.html # 消息详情
    ├── following.html     # 关注列表
    ├── followers.html     # 粉丝列表
    ├── blacklist.html     # 黑名单
    ├── favorites.html     # 收藏夹
    ├── interactions.html  # 互动历史
    ├── mentions.html      # @提醒
    ├── tags.html          # 标签列表
    ├── tag_detail.html    # 标签详情
    ├── essence.html       # 精华帖
    ├── create_vote.html   # 创建投票
    ├── post_stats.html    # 发帖统计
    ├── edit_comment.html  # 编辑评论
    ├── macros.html        # 模板宏
    ├── admin/             # 后台管理模板
    │   ├── dashboard.html # 后台仪表板
    │   ├── users.html     # 用户管理
    │   ├── categories.html # 版块管理
    │   ├── posts.html     # 帖子管理
    │   ├── reports.html   # 举报管理
    │   ├── analytics.html # 数据统计
    │   └── logs.html      # 请求日志
    └── ...                # 其他模板文件
```

## 核心组件说明

### 1. 应用入口 (app.py)
- Flask 应用创建和配置
- 扩展初始化
- 请求前后处理
- 路由注册

### 2. 配置文件 (config.py)
- 应用密钥配置
- 数据库连接配置
- 文件上传配置
- CSRF保护配置

### 3. 扩展文件 (extensions.py)
- SQLAlchemy 数据库扩展
- Flask-Login 用户认证扩展
- CSRF保护扩展

### 4. 数据模型 (models.py)
- User 用户模型
- Category 版块模型
- Post 帖子模型
- Comment 评论模型
- Tag 标签模型
- Message 私信模型
- Report 举报模型
- Vote 投票模型
- Attachment 附件模型
- RequestLog 请求日志模型

### 5. 路由文件
- routes.py: 主要功能路由
- routes_advanced.py: 高级功能路由

### 6. 静态资源
- CSS 样式文件
- JavaScript 脚本文件
- 图片资源
- 用户上传文件

### 7. 模板文件
- 基础模板和布局
- 页面模板
- 后台管理模板
- 模板宏

## 运行方式
1. 安装依赖: `pip install -r requirements.txt`
2. 初始化数据库: `python init_db.py`
3. 运行应用: `python run.py`
4. 访问地址: `http://localhost:5000`

## 默认管理员账号
- 用户名: admin
- 密码: admin123
