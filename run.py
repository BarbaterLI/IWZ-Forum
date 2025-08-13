#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flask论坛系统启动脚本
支持Windows、Linux和macOS
"""

import os
import sys
import platform
import subprocess
import webbrowser
import time
from threading import Timer

def is_venv():
    """检查是否在虚拟环境中"""
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    return True

def check_dependencies():
    """检查依赖包"""
    try:
        import flask
        import flask_login
        import flask_wtf
        import wtforms
        return True
    except ImportError as e:
        print(f"缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def init_database():
    """初始化数据库"""
    if not os.path.exists('forum.db'):
        print("初始化数据库...")
        try:
            subprocess.run([sys.executable, 'init_db.py'], check=True)
            print("数据库初始化完成")
            return True
        except subprocess.CalledProcessError:
            print("数据库初始化失败")
            return False
    return True

def open_browser():
    """在浏览器中打开应用"""
    def _open():
        webbrowser.open('http://localhost:5000')
    timer = Timer(2.0, _open)  # 2秒后打开浏览器
    timer.daemon = True
    timer.start()

def main():
    """主函数"""
    print("Flask论坛系统启动器")
    print("=" * 30)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查虚拟环境
    if not is_venv():
        print("警告: 建议在虚拟环境中运行此应用")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 初始化数据库
    if not init_database():
        sys.exit(1)
    
    # 设置环境变量
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    # 打开浏览器
    open_browser()
    
    # 启动应用
    print("启动Flask应用...")
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止应用")
    print("=" * 30)
    
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n应用已停止")
    except subprocess.CalledProcessError as e:
        print(f"启动失败: {e}")

if __name__ == '__main__':
    main()
