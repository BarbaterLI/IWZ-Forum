from flask import Flask, request, g
from config import Config
from extensions import db, login_manager, csrf
from models import RequestLog
import time
import os

def create_app():
    # 初始化应用
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 配置安全设置
    app.config.update(
        SESSION_COOKIE_SECURE=True,  # 设置安全cookie
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = '请先登录以访问此页面。'
    
    # 用户加载回调
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # 请求开始前记录时间
    @app.before_request
    def before_request():
        g.start_time = time.time()
        
        # 极端扩展日志记录（仅在调试模式下）
        if app.config.get('DEBUG_EXTREME_LOGGING', False):
            print(f"[EXTREME LOG] 请求开始: {request.method} {request.url}")
            print(f"[EXTREME LOG] 请求头: {dict(request.headers)}")
            if request.is_json:
                print(f"[EXTREME LOG] JSON数据: {request.get_json()}")
            elif request.form:
                print(f"[EXTREME LOG] 表单数据: {dict(request.form)}")
            elif request.args:
                print(f"[EXTREME LOG] 查询参数: {dict(request.args)}")
    
    # 请求结束后记录日志和添加安全头
    @app.after_request
    def after_request(response):
        # 添加安全头
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # 记录请求日志
        if hasattr(g, 'start_time'):
            response_time = (time.time() - g.start_time) * 1000  # 转换为毫秒
        else:
            response_time = 0
        
        # 获取用户ID（如果已登录）
        user_id = None
        if hasattr(request, 'user') and request.user:
            user_id = request.user.id
        elif hasattr(g, 'user_id'):
            user_id = g.user_id
        
        # 创建请求日志记录
        log_entry = RequestLog(
            ip_address=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
            user_agent=request.headers.get('User-Agent', ''),
            method=request.method,
            url=request.url,
            status_code=response.status_code,
            response_time=response_time,
            user_id=user_id,
            referrer=request.headers.get('Referer', ''),
            content_length=request.content_length or 0
        )
        
        try:
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            # 如果日志记录失败，回滚并继续
            db.session.rollback()
            print(f"日志记录失败: {str(e)}")
        
        # 极端扩展日志记录（仅在调试模式下）
        if app.config.get('DEBUG_EXTREME_LOGGING', False):
            print(f"[EXTREME LOG] 响应状态: {response.status_code}")
            print(f"[EXTREME LOG] 响应时间: {response_time:.2f}ms")
            print(f"[EXTREME LOG] 响应头: {dict(response.headers)}")
            if response.is_json:
                print(f"[EXTREME LOG] JSON响应: {response.get_json()}")
            print("=" * 80)
        
        return response
    
    # 注册路由
    from routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # 注册高级功能路由
    from routes_advanced import bp as advanced_bp
    app.register_blueprint(advanced_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    # 在生产环境中应该使用WSGI服务器
    app.run(debug=True, ssl_context='adhoc')  # 临时启用HTTPS以支持安全cookie
