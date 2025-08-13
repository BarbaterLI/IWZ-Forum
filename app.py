from flask import Flask
from config import Config
from extensions import db, login_manager

def create_app():
    # 初始化应用
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = '请先登录以访问此页面。'
    
    # 用户加载回调
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # 注册路由
    from routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # 注册高级功能路由
    from routes_advanced import bp as advanced_bp
    app.register_blueprint(advanced_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
