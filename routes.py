from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Category, Post, Comment, Attachment
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import markdown
import bleach

# 创建蓝图
bp = Blueprint('main', __name__)

# 首页
@bp.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    categories = Category.query.all()
    return render_template('index.html', posts=posts, categories=categories)

# 用户注册
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('main.register'))
            
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册')
            return redirect(url_for('main.register'))
            
        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

# 用户登录
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')
            
    return render_template('login.html')

# 用户登出
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 版块列表
@bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

# 版块详情
@bp.route('/category/<int:category_id>')
def category_detail(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.created_at.desc()).all()
    return render_template('category_detail.html', category=category, posts=posts)

# 帖子详情
@bp.route('/post/<post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    # 增加浏览量
    post.view_count += 1
    db.session.commit()
    return render_template('post_detail.html', post=post)

# 发帖
@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category_id']
        
        # 处理Markdown内容
        # 允许的HTML标签
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'a', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre']
        allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
        }
        
        # 清理内容
        clean_content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)
        
        post = Post(title=title, content=clean_content, author=current_user, category_id=category_id)
        db.session.add(post)
        db.session.flush()  # 获取post.id用于附件关联
        
        # 处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                try:
                    # 检查文件大小 (10MB限制)
                    file.seek(0, os.SEEK_END)
                    file_length = file.tell()
                    file.seek(0)
                    
                    if file_length > 10 * 1024 * 1024:  # 10MB
                        flash('文件大小不能超过10MB')
                        return redirect(request.url)
                    
                    # 保存文件
                    filename = secure_filename(file.filename)
                    upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(current_app.root_path, 'uploads'))
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    
                    # 保存文件信息到数据库
                    attachment = Attachment(
                        filename=filename,
                        file_path=file_path,
                        file_size=file_length,
                        file_type=file.content_type or 'unknown',
                        post_id=post.id,
                        user_id=current_user.id
                    )
                    db.session.add(attachment)
                except RequestEntityTooLarge:
                    flash('文件大小超过限制')
                    return redirect(request.url)
                except Exception as e:
                    flash(f'文件上传失败: {str(e)}')
                    return redirect(request.url)
        
        db.session.commit()
        
        flash('帖子发布成功')
        return redirect(url_for('main.post_detail', post_id=post.id))
        
    categories = Category.query.all()
    return render_template('create_post.html', categories=categories)

# 回帖
@bp.route('/post/<post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    
    comment = Comment(content=content, author=current_user, post=post)
    db.session.add(comment)
    db.session.commit()
    
    flash('回复成功')
    return redirect(url_for('main.post_detail', post_id=post_id))

# 用户个人中心
@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# 用户资料页
@bp.route('/user/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return render_template('user_detail.html', user=user, posts=posts)

# 下载附件
@bp.route('/attachment/<int:attachment_id>')
@login_required
def download_attachment(attachment_id):
    attachment = Attachment.query.get_or_404(attachment_id)
    # 检查文件是否存在
    if not os.path.exists(attachment.file_path):
        flash('文件不存在')
        return redirect(request.referrer or url_for('main.index'))
    
    # 使用send_file发送文件
    from flask import send_file
    return send_file(attachment.file_path, as_attachment=True, download_name=attachment.filename)
