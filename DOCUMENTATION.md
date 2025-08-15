# IWZ-Forum 完整文档

## 目录
1. [项目概述](#项目概述)
2. [功能特性](#功能特性)
3. [技术栈](#技术栈)
4. [安装与部署](#安装与部署)
5. [项目结构](#项目结构)
6. [数据库设计](#数据库设计)
7. [API接口](#api接口)
8. [用户界面](#用户界面)
9. [后台管理](#后台管理)
10. [安全机制](#安全机制)
11. [性能优化](#性能优化)
12. [扩展开发](#扩展开发)

## 项目概述
IWZ-Forum 是一个功能完整的现代化论坛系统，基于 Flask 和 SQLite 构建，提供了丰富的社交功能和美观的用户界面。系统支持用户注册登录、帖子发布、评论互动、好友系统、私信聊天、关注机制、标签分类、精华推荐、数据统计等完整功能。

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

### 管理功能
- 用户管理（查看、删除用户）
- 版块管理（创建、编辑、删除版块）
- 帖子管理（查看、删除帖子）
- 举报处理（处理或忽略举报）
- 数据统计（用户、帖子、评论增长图表）
- 请求日志查看

## 技术栈
- **后端**: Flask + SQLite
- **前端**: Bootstrap 5 + Jinja2模板
- **样式**: CSS3 + JavaScript，支持深色/浅色主题切换
- **图标**: Font Awesome + Bootstrap Icons
- **编辑器**: SimpleMDE Markdown编辑器
- **安全**: CSRF保护、XSS防护、SQL注入防护

## 安装与部署

### 环境要求
- Python 3.7+
- pip包管理器

### 安装步骤
1. 克隆项目到本地：
```bash
git clone https://github.com/BarbaterLI/IWZ-Forum.git
cd IWZ-Forum
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
python run.py
```

6. 在浏览器中访问 `http://localhost:5000`

默认管理员账号：
- 用户名: admin
- 密码: admin123

### 生产环境部署
在生产环境中，建议使用专业的WSGI服务器如Gunicorn或uWSGI配合Nginx进行部署。

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
├── PROJECT_STRUCTURE.md   # 项目结构说明
├── DOCUMENTATION.md       # 完整文档（当前文件）
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

## 数据库设计

### 核心表结构

#### User (用户表)
- id: Integer, 主键
- user_id: String, 唯一用户ID
- username: String, 用户名
- email: String, 邮箱
- password_hash: String, 密码哈希
- avatar: String, 头像文件名
- bio: String, 个人简介
- created_at: DateTime, 创建时间
- is_admin: Boolean, 是否为管理员
- last_seen: DateTime, 最后在线时间

#### Category (版块表)
- id: Integer, 主键
- name: String, 版块名称
- description: String, 版块描述
- created_at: DateTime, 创建时间

#### Post (帖子表)
- id: String, 主键 (UUID格式)
- title: String, 标题
- content: Text, 内容
- created_at: DateTime, 创建时间
- updated_at: DateTime, 更新时间
- view_count: Integer, 浏览数
- is_essence: Boolean, 是否为精华帖
- is_locked: Boolean, 是否锁定
- is_reported: Boolean, 是否被举报
- file_path: String, 附件路径
- file_name: String, 附件名称
- user_id: Integer, 外键关联User
- category_id: Integer, 外键关联Category

#### Comment (评论表)
- id: Integer, 主键
- content: Text, 内容
- created_at: DateTime, 创建时间
- is_reported: Boolean, 是否被举报
- user_id: Integer, 外键关联User
- post_id: String, 外键关联Post

#### Tag (标签表)
- id: Integer, 主键
- name: String, 标签名称
- created_at: DateTime, 创建时间

#### Message (私信表)
- id: Integer, 主键
- sender_id: Integer, 发送者ID
- recipient_id: Integer, 接收者ID
- content: Text, 内容
- created_at: DateTime, 创建时间
- is_read: Boolean, 是否已读

#### Report (举报表)
- id: Integer, 主键
- reporter_id: Integer, 举报者ID
- reported_type: String, 被举报类型 (post/comment)
- reported_id: Integer, 被举报ID
- reason: String, 举报理由
- created_at: DateTime, 创建时间
- status: String, 状态 (pending/resolved/dismissed)

#### Vote (投票表)
- id: Integer, 主键
- user_id: Integer, 用户ID
- voted_type: String, 投票类型 (post/comment)
- voted_id: Integer, 被投票ID
- vote_type: Integer, 投票类型 (1: 赞, -1: 踩)
- created_at: DateTime, 创建时间

#### Attachment (附件表)
- id: Integer, 主键
- filename: String, 文件名
- file_path: String, 文件路径
- file_size: Integer, 文件大小
- file_type: String, 文件类型
- created_at: DateTime, 创建时间
- post_id: String, 外键关联Post
- user_id: Integer, 外键关联User

#### RequestLog (请求日志表)
- id: Integer, 主键
- ip_address: String, IP地址
- user_agent: Text, 用户代理
- method: String, HTTP方法
- url: Text, 请求URL
- status_code: Integer, 状态码
- response_time: Float, 响应时间
- timestamp: DateTime, 时间戳
- user_id: Integer, 用户ID
- referrer: Text, 引荐页面
- content_length: Integer, 内容长度

### 关系表

#### user_friends (用户好友关系表)
- user_id: Integer, 用户ID
- friend_id: Integer, 好友ID

#### user_follows (用户关注关系表)
- user_id: Integer, 用户ID
- followed_id: Integer, 被关注者ID

#### user_blacklist (用户黑名单关系表)
- user_id: Integer, 用户ID
- blocked_id: Integer, 被屏蔽者ID

#### post_tags (帖子标签关联表)
- post_id: Integer, 帖子ID
- tag_id: Integer, 标签ID

#### post_favorites (帖子收藏关联表)
- user_id: Integer, 用户ID
- post_id: Integer, 帖子ID

#### post_votes (帖子投票关联表)
- user_id: Integer, 用户ID
- post_id: Integer, 帖子ID
- vote_type: Integer, 投票类型

#### comment_votes (评论投票关联表)
- user_id: Integer, 用户ID
- comment_id: Integer, 评论ID
- vote_type: Integer, 投票类型

## API接口

### 用户认证
- `GET /login` - 登录页面
- `POST /login` - 用户登录
- `GET /register` - 注册页面
- `POST /register` - 用户注册
- `GET /logout` - 用户登出

### 用户管理
- `GET /profile` - 个人中心
- `GET /profile/edit` - 编辑个人资料页面
- `POST /profile/edit` - 更新个人资料
- `GET /user/<user_id>` - 用户资料页

### 内容管理
- `GET /` - 首页
- `GET /categories` - 版块列表
- `GET /category/<category_id>` - 版块详情
- `GET /post/<post_id>` - 帖子详情
- `GET /create_post` - 发帖页面
- `POST /create_post` - 创建帖子
- `POST /post/<post_id>/comment` - 添加评论
- `GET /post/<post_id>/edit` - 编辑帖子页面
- `POST /post/<post_id>/edit` - 更新帖子
- `GET /comment/<comment_id>/edit` - 编辑评论页面
- `POST /comment/<comment_id>/edit` - 更新评论

### 搜索功能
- `GET /search` - 搜索页面

### 社交功能
- `GET /friends` - 好友列表
- `POST /add_friend/<user_id>` - 添加好友
- `POST /remove_friend/<user_id>` - 移除好友
- `GET /messages` - 消息列表
- `GET /messages/<user_id>` - 消息详情
- `POST /send_message/<user_id>` - 发送消息
- `GET /following` - 关注列表
- `GET /followers` - 粉丝列表
- `POST /follow/<user_id>` - 关注用户
- `POST /unfollow/<user_id>` - 取消关注
- `GET /blacklist` - 黑名单
- `POST /block/<user_id>` - 加入黑名单
- `POST /unblock/<user_id>` - 移出黑名单
- `POST /vote/<entity_type>/<entity_id>/<vote_type>` - 点赞/踩
- `GET /favorites` - 收藏夹
- `POST /favorite/<post_id>` - 添加收藏
- `POST /unfavorite/<post_id>` - 移除收藏
- `POST /share/<post_id>` - 转发帖子
- `GET /mentions` - @提醒
- `GET /tags` - 标签列表
- `GET /tag/<tag_id>` - 标签详情
- `GET /essence` - 精华帖
- `GET /create_vote` - 创建投票页面
- `POST /create_vote` - 创建投票
- `GET /post_stats` - 发帖统计
- `GET /interactions` - 互动历史
- `POST /report/<entity_type>/<entity_id>` - 举报内容

### 后台管理
- `GET /admin` - 后台仪表板
- `GET /admin/logs` - 请求日志
- `GET /admin/users` - 用户管理
- `POST /admin/user/<user_id>/delete` - 删除用户
- `GET /admin/categories` - 版块管理
- `POST /admin/category/create` - 创建版块
- `POST /admin/category/<category_id>/edit` - 编辑版块
- `POST /admin/category/<category_id>/delete` - 删除版块
- `GET /admin/posts` - 帖子管理
- `POST /admin/post/<post_id>/delete` - 删除帖子
- `GET /admin/reports` - 举报管理
- `POST /admin/report/<report_id>/resolve` - 处理举报
- `POST /admin/report/<report_id>/dismiss` - 忽略举报
- `GET /admin/analytics` - 数据统计

## 用户界面

### 前端技术
- Bootstrap 5: 响应式布局框架
- Font Awesome: 图标库
- Bootstrap Icons: 图标库
- SimpleMDE: Markdown编辑器
- 自定义CSS: 主题样式和动画效果

### 主题系统
系统支持深色/浅色主题切换，用户可以根据喜好选择界面主题。

### 响应式设计
界面采用响应式设计，适配各种设备屏幕尺寸，包括桌面、平板和手机。

### 交互效果
- 页面加载动画
- 按钮悬停效果
- 卡片悬停效果
- 代码块复制功能
- 表单自动CSRF令牌添加

## 后台管理

### 仪表板
提供系统概览，包括用户数、帖子数、评论数、待处理举报等统计信息。

### 用户管理
- 查看所有用户列表
- 删除违规用户
- 管理员权限设置

### 版块管理
- 创建、编辑、删除版块
- 版块名称和描述管理

### 帖子管理
- 查看所有帖子
- 删除违规帖子
- 精华帖设置

### 举报管理
- 查看待处理举报
- 处理或忽略举报
- 举报状态跟踪

### 数据统计
- 用户增长统计图表
- 帖子增长统计图表
- 评论增长统计图表
- 版块数据统计

### 请求日志
- 查看系统请求日志
- 按时间筛选日志
- IP地址、用户代理等信息记录

## 安全机制

### 认证安全
- 密码哈希存储 (Werkzeug security)
- Session安全配置
- CSRF保护 (Flask-WTF)
- 登录状态管理 (Flask-Login)

### 数据安全
- SQL注入防护 (SQLAlchemy ORM)
- XSS防护 (Bleach HTML清理)
- 输入验证和清理
- 文件上传安全检查

### 通信安全
- HTTPS支持 (开发环境自签名证书)
- 安全响应头设置
- 内容安全策略

### 权限控制
- 用户角色权限管理
- 管理员权限验证
- 资源访问控制

## 性能优化

### 数据库优化
- 索引优化
- 查询优化
- 分页处理
- 关联查询优化

### 前端优化
- 静态资源压缩
- 图片优化
- 代码分割
- 缓存策略

### 服务器优化
- 请求日志记录
- 响应时间监控
- 内存使用优化
- 连接池管理

## 扩展开发

### 添加新功能
1. 在models.py中添加数据模型
2. 在routes.py或routes_advanced.py中添加路由
3. 在templates/中添加模板文件
4. 在static/css/style.css中添加样式
5. 在static/js/script.js中添加JavaScript

### 自定义主题
可以通过修改static/css/style.css文件来自定义主题颜色和样式。

### 插件开发
系统采用模块化设计，可以方便地添加新的功能模块。

## 常见问题

### 数据库初始化失败
确保已正确安装所有依赖，并且Python环境正常。

### 文件上传失败
检查uploads目录权限，确保应用有写入权限。

### 页面加载缓慢
检查服务器性能，优化数据库查询，启用缓存机制。

### 安全警告
生产环境请使用正式SSL证书，不要使用开发环境的自签名证书。

## 贡献指南
欢迎提交Issue和Pull Request来改进IWZ-Forum项目。

## 许可证
AGPL V3 License

## 联系方式
本项目随缘更新,并且不修bug,使用出现问题概不负责.
