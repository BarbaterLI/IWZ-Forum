from app import create_app
from extensions import db
from models import User, Category, Post, Comment, Tag, Attachment
import uuid

def init_database():
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已存在初始数据
        if Category.query.first() is None:
            # 创建示例版块
            general = Category(name="综合讨论", description="综合讨论区")
            tech = Category(name="技术交流", description="技术交流与分享")
            life = Category(name="生活分享", description="生活点滴分享")
            
            db.session.add(general)
            db.session.add(tech)
            db.session.add(life)
            db.session.commit()
            
            print("已创建示例版块：综合讨论、技术交流、生活分享")
        
        # 创建示例标签
        if Tag.query.first() is None:
            tags = [
                Tag(name="技术"),
                Tag(name="生活"),
                Tag(name="娱乐"),
                Tag(name="教程"),
                Tag(name="问答")
            ]
            for tag in tags:
                db.session.add(tag)
            db.session.commit()
            print("已创建示例标签：技术、生活、娱乐、教程、问答")
        
        # 创建管理员用户（如果不存在）
        if User.query.first() is None:
            admin = User(username="admin", email="admin@example.com", is_admin=True)
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("已创建管理员账户：admin / admin123")
        
        print("数据库初始化完成！")

if __name__ == "__main__":
    init_database()
