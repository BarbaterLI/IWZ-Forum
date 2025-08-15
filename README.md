# IWZ-Forum 论坛系统

一个功能完整的基于 Flask 和 SQLite 的现代化论坛系统，具有丰富的社交功能和美观的用户界面。

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![License](https://img.shields.io/github/license/BarbaterLI/IWZ-Forum)

## 功能特性

### 核心功能
- **用户系统**: 注册登录、个人资料管理、头像设置
- **内容管理**: 帖子发布编辑、评论回复、版块分类、标签系统
- **社交互动**: 好友系统、私信聊天、关注机制、收藏夹、点赞踩功能
- **高级功能**: 投票系统、举报处理、数据统计、@提醒、精华帖推荐
- **后台管理**: 用户管理、版块管理、帖子管理、举报处理、数据统计

### 技术特色
- 响应式设计，支持深色/浅色主题切换
- Markdown编辑器支持
- 代码块复制功能
- 完善的安全机制（CSRF保护、XSS防护）
- 丰富的数据统计和分析功能

## 快速开始

### 环境要求
- Python 3.7+
- pip包管理器

### 安装运行

```bash
# 1. 克隆项目
git clone https://github.com/BarbaterLI/IWZ-Forum.git
cd IWZ-Forum

# 2. 创建虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库
python init_db.py

# 5. 运行应用
python run.py

# 6. 访问 http://localhost:5000
```

默认管理员账号：
- 用户名: admin
- 密码: admin123

## 项目结构

```
IWZ-Forum/
├── app.py              # 应用入口
├── run.py              # 运行脚本
├── config.py           # 配置文件
├── extensions.py       # Flask扩展
├── init_db.py          # 数据库初始化
├── requirements.txt    # 依赖列表
├── README.md           # 说明文档
├── models.py           # 数据模型
├── routes.py           # 主要路由
├── routes_advanced.py  # 高级功能路由
├── static/             # 静态资源
│   ├── css/style.css   # 自定义样式
│   ├── js/script.js    # 自定义脚本
│   ├── images/         # 图片资源
│   └── uploads/        # 用户上传文件
└── templates/          # 模板文件
    ├── base.html       # 基础模板
    ├── index.html      # 首页
    ├── admin/          # 后台管理模板
    └── ...             # 其他页面模板
```

## 文档

- [完整文档](DOCUMENTATION.md) - 详细的开发和使用文档
- [项目结构说明](PROJECT_STRUCTURE.md) - 项目文件组织说明

## 许可证

本项目采用 AGPL V3 许可证，详情请见 [LICENSE](LICENSE) 文件。

## 免责声明

本项目随缘更新，不提供技术支持，使用出现问题概不负责。
