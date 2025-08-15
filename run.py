import sys
from waitress import serve
from app import create_app

def main():
    # 检查是否启用调试模式
    debug_mode = '-debug' in sys.argv
    
    app = create_app()
    
    if debug_mode:
        print("启动IWZ-Forum论坛系统 (调试模式)...")
        print("访问地址: https://localhost:5000")
        print("按Ctrl+C停止服务器")
        print("=" * 50)
        print("调试功能已启用:")
        print("- 极端扩展日志记录")
        print("- 详细错误信息")
        print("- 自动重载")
        print("=" * 50)
        # 在调试模式下启用极端日志记录
        app.config['DEBUG_EXTREME_LOGGING'] = True
        # 在调试模式下使用Flask内置服务器
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
    else:
        print("启动IWZ-Forum论坛系统...")
        print("访问地址: http://localhost:5000")
        print("按Ctrl+C停止服务器")
        serve(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
