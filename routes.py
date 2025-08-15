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
    post_count = Post.query.count()
    comment_count = Comment.query.count()
    user_count = User.query.count()
    category_count = Category.query.count()
    active_users = User.query.order_by(User.last_seen.desc()).limit(12).all()
    return render_template('index.html', posts=posts, categories=categories, 
                          post_count=post_count, comment_count=comment_count, 
                          user_count=user_count, category_count=category_count,
                          active_users=active_users)

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
    # 获取所有版块（用于侧边栏）
    all_categories = Category.query.all()
    return render_template('category_detail.html', category=category, posts=posts, all_categories=all_categories)

# 帖子详情
@bp.route('/post/<post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    # 增加浏览量
    post.view_count += 1
    db.session.commit()
    
    # 获取相关帖子
    related_posts = Post.query.filter(
        Post.category_id == post.category_id, 
        Post.id != post.id
    ).order_by(Post.created_at.desc()).limit(5).all()
    
    return render_template('post_detail.html', post=post, related_posts=related_posts)

# 发帖
@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            category_id = request.form.get('category_id')
            
            # 验证输入
            if not title:
                flash('请填写帖子标题')
                return redirect(url_for('main.create_post'))
            
            if not content:
                flash('请填写帖子内容')
                return redirect(url_for('main.create_post'))
            
            if not category_id:
                flash('请选择版块')
                return redirect(url_for('main.create_post'))
            
            # 处理Markdown内容
            # 允许的HTML标签
            allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'a', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre']
            allowed_attributes = {
                'a': ['href', 'title'],
                'img': ['src', 'alt', 'title', 'width', 'height'],
            }
            
            # 清理内容 (XSS防护)
            clean_content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)
            
            # 创建帖子
            post = Post(title=title, content=clean_content, author=current_user, category_id=int(category_id))
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
                            return redirect(url_for('main.create_post'))
                        
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
                        return redirect(url_for('main.create_post'))
                    except Exception as e:
                        flash(f'文件上传失败: {str(e)}')
                        return redirect(url_for('main.create_post'))
            
            db.session.commit()
            
            flash('帖子发布成功')
            return redirect(url_for('main.post_detail', post_id=post.id))
        except Exception as e:
            db.session.rollback()
            flash(f'发帖失败: {str(e)}')
            return redirect(url_for('main.create_post'))
        
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

# 编辑用户资料
@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        bio = request.form['bio']
        
        # 处理头像上传
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and avatar_file.filename != '':
                # 检查文件类型
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
                file_ext = avatar_file.filename.rsplit('.', 1)[1].lower() if '.' in avatar_file.filename else ''
                if file_ext in allowed_extensions:
                    # 生成文件名：iwz-f-u-uuid.扩展名
                    filename = f"iwz-f-u-{current_user.user_id}.{file_ext}"
                    upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(current_app.root_path, 'uploads'))
                    
                    # 创建上传目录（如果不存在）
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    # 保存并压缩图片
                    file_path = os.path.join(upload_folder, filename)
                    
                    # 如果是图片文件，进行压缩处理
                    if file_ext in {'png', 'jpg', 'jpeg', 'gif', 'bmp'}:
                        try:
                            from PIL import Image
                            
                            # 打开图片
                            image = Image.open(avatar_file)
                            
                            # 转换为RGB模式（如果需要）
                            if image.mode in ('RGBA', 'LA', 'P'):
                                # 如果是RGBA或LA模式，转换为RGB并处理透明背景
                                if file_ext == 'jpg' or file_ext == 'jpeg':
                                    background = Image.new('RGB', image.size, (255, 255, 255))
                                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                                    image = background
                                else:
                                    image = image.convert('RGB')
                            
                            # 强制压缩到512x512
                            image = image.resize((512, 512), Image.Resampling.LANCZOS)
                            
                            # 保存图片
                            if file_ext == 'png':
                                image.save(file_path, 'PNG', optimize=True)
                            elif file_ext == 'jpg' or file_ext == 'jpeg':
                                image.save(file_path, 'JPEG', quality=85, optimize=True)
                            elif file_ext == 'gif':
                                image.save(file_path, 'GIF', optimize=True)
                            elif file_ext == 'bmp':
                                image.save(file_path, 'BMP')
                                
                        except Exception as e:
                            # 如果图片处理失败，直接保存原文件
                            avatar_file.seek(0)  # 重置文件指针
                            avatar_file.save(file_path)
                    else:
                        # 非图片文件直接保存
                        avatar_file.save(file_path)
                    
                    # 更新用户头像字段
                    current_user.avatar = filename
                else:
                    flash('头像文件格式不支持，仅支持 PNG, JPG, JPEG, GIF, BMP 格式')
                    return redirect(url_for('main.edit_profile'))
        
        # 检查用户名是否已存在（排除当前用户）
        existing_user = User.query.filter(User.username == username, User.id != current_user.id).first()
        if existing_user:
            flash('用户名已存在')
            return redirect(url_for('main.edit_profile'))
            
        # 检查邮箱是否已存在（排除当前用户）
        existing_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_email:
            flash('邮箱已被注册')
            return redirect(url_for('main.edit_profile'))
        
        # 更新用户信息
        current_user.username = username
        current_user.email = email
        current_user.bio = bio
        
        db.session.commit()
        
        flash('资料更新成功')
        return redirect(url_for('main.profile'))
    
    return render_template('edit_profile.html')

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
