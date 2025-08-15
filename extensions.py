from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# 创建扩展实例
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
