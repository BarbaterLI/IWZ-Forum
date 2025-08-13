# Flask论坛系统

一个功能完整的基于Flask和SQLite的论坛系统，具有现代化的用户界面和丰富的功能。

## 功能特性

### 用户系统
- 用户注册/登录
- 个人资料管理
- 头像设置
- 密码找回

### 内容管理
- 帖子发布与编辑
- 评论与回复
- 版块分类
- 标签系统
- 精华帖推荐
- 搜索功能

### 社交功能
- 好友系统
- 私信聊天
- 关注/粉丝系统
- 黑名单管理
- @提醒功能
- 收藏夹管理
- 点赞/踩功能

### 高级功能
- 投票系统
- 举报处理
- 后台管理
- 数据统计
- 互动历史

## 技术栈

- **后端**: Flask + SQLite
- **前端**: Bootstrap 5 + Jinja2模板
- **样式**: CSS3 + JavaScript
- **图标**: Font Awesome + Bootstrap Icons

## 安装与运行

### 环境要求
- Python 3.7+
- pip包管理器

### 安装步骤

1. 克隆项目到本地：
```bash
git clone <项目地址>
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

## 主要页面

- 首页 (`/`) - 论坛概览
- 登录/注册页面 - 用户认证
- 版块列表 (`/categories`) - 所有讨论区
- 版块详情 (`/category/<id>`) - 特定版块下的帖子
- 帖子详情 (`/post/<id>`) - 具体讨论内容
- 发帖页面 (`/create_post`) - 创建新话题
- 个人中心 (`/profile`) - 个人信息管理
- 搜索页面 (`/search`) - 内容搜索
- 后台管理 (`/admin/*`) - 管理员功能

## 开发说明

### 添加新功能
1. 在`models.py`中添加数据模型
2. 在`routes.py`或`routes_advanced.py`中添加路由
3. 在`templates/`中创建相应模板
4. 在`static/css/style.css`中添加样式（如需要）

### 自定义样式
- 主题颜色在`static/css/style.css`的`:root`部分定义
- 可以通过修改CSS变量来自定义主题色
- 深色模式支持已内置

## 许可证

MIT License

## 联系方式

如有问题，请提交issue或联系项目维护者。
