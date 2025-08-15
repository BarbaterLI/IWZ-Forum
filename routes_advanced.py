from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Category, Post, Comment, Tag, Message, Report, Vote, RequestLog
from datetime import datetime, timedelta
import os

# 创建蓝图
bp = Blueprint('advanced', __name__)

# 编辑帖子页面
@bp.route('/post/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # 检查用户是否有权限编辑帖子
    if post.user_id != current_user.id and not current_user.is_admin:
        flash('您没有权限编辑此帖子')
        return redirect(url_for('main.post_detail', post_id=post.id))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category_id']
        
        # 更新帖子
        post.title = title
        post.content = content
        post.category_id = category_id
        post.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('帖子更新成功')
        return redirect(url_for('main.post_detail', post_id=post.id))
    
    categories = Category.query.all()
    return render_template('edit_post.html', post=post, categories=categories)

# 编辑评论页面
@bp.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    # 检查用户是否有权限编辑评论
    if comment.user_id != current_user.id and not current_user.is_admin:
        flash('您没有权限编辑此评论')
        return redirect(url_for('main.post_detail', post_id=comment.post.id))
    
    if request.method == 'POST':
        content = request.form['content']
        
        # 更新评论
        comment.content = content
        
        db.session.commit()
        
        flash('评论更新成功')
        return redirect(url_for('main.post_detail', post_id=comment.post.id))
    
    return render_template('edit_comment.html', comment=comment)

# 搜索页面
@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    users = []
    posts = []
    
    if query:
        # 搜索帖子标题、内容、ID
        posts = Post.query.filter(
            db.or_(
                Post.title.contains(query),
                Post.content.contains(query),
                Post.id.contains(query)  # 搜索帖子ID
            )
        ).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        
        # 搜索用户名称和用户ID
        users = User.query.filter(
            db.or_(
                User.username.contains(query),
                User.user_id.contains(query)  # 搜索用户ID
            )
        ).all()
    else:
        posts = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
    
    return render_template('search.html', posts=posts, users=users, query=query)

# 后台管理页面 - 仪表板
@bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('您没有权限访问此页面')
        return redirect(url_for('main.index'))
    
    # 统计数据
    user_count = User.query.count()
    post_count = Post.query.count()
    comment_count = Comment.query.count()
    report_count = Report.query.filter_by(status='pending').count()
    
    # 最近的帖子
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # 最近的用户
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count,
                          post_count=post_count,
                          comment_count=comment_count,
                          report_count=report_count,
                          recent_posts=recent_posts,
                          recent_users=recent_users)

# 后台管理页面 - 请求日志
@bp.route('/admin/logs')
@login_required
def admin_logs():
    if not current_user.is_admin:
        flash('您没有权限访问此页面')
        return redirect(url_for('main.index'))
    
    # 获取过滤参数
    days = request.args.get('days', 7, type=int)
    page = request.args.get('page', 1, type=int)
    
    # 计算日期范围
    from datetime import datetime, timedelta
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 查询日志
    logs = RequestLog.query.filter(RequestLog.timestamp >= start_date).order_by(
        RequestLog.timestamp.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/logs.html', logs=logs)

# 后台管理页面 - 用户管理
@bp.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('您没有权限访问此页面')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users)

# 删除用户
@bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    # 不能删除管理员用户
    if user.is_admin:
        flash('不能删除管理员用户')
        return redirect(url_for('advanced.admin_users'))
    
    # 不能删除自己
    if user.id == current_user.id:
        flash('不能删除自己')
        return redirect(url_for('advanced.admin_users'))
    
    # 删除用户相关数据
    # 删除用户的帖子
    Post.query.filter_by(user_id=user.id).delete()
    
    # 删除用户的评论
    Comment.query.filter_by(user_id=user.id).delete()
    
    # 删除用户的消息
    Message.query.filter(
        db.or_(
            Message.sender_id == user.id,
            Message.recipient_id == user.id
        )
    ).delete()
    
    # 删除用户的举报
    Report.query.filter_by(reporter_id=user.id).delete()
    
    # 删除用户的投票
    Vote.query.filter_by(user_id=user.id).delete()
    
    # 删除用户
    db.session.delete(user)
    db.session.commit()
    
    flash('用户删除成功')
    return redirect(url_for('advanced.admin_users'))

# 后台管理页面 - 版块管理
@bp.route('/admin/categories')
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('您没有权限访问此页面')
        return redirect(url_for('main.index'))
    
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

# 创建版块
@bp.route('/admin/category/create', methods=['POST'])
@login_required
def admin_create_category():
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    
    name = request.form.get('name')
    description = request.form.get('description')
    
    if name:
        # 检查版块是否已存在
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash('版块名称已存在')
        else:
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            flash('版块创建成功')
    else:
        flash('版块名称不能为空')
    
    return redirect(url_for('advanced.admin_categories'))

# 编辑版块
@bp.route('/admin/category/<int:category_id>/edit', methods=['POST'])
@login_required
def admin_edit_category(category_id):
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    
    category = Category.query.get_or_404(category_id)
    name = request.form.get('name')
    description = request.form.get('description')
    
    if name:
        # 检查版块名称是否已存在（排除当前版块）
        existing_category = Category.query.filter(Category.name == name, Category.id != category_id).first()
        if existing_category:
            flash('版块名称已存在')
        else:
            category.name = name
            category.description = description
            db.session.commit()
            flash('版块更新成功')
    else:
        flash('版块名称不能为空')
    
    return redirect(url_for('advanced.admin_categories'))

# 删除版块
@bp.route('/admin/category/<int:category_id>/delete', methods=['POST'])
@login_required
def admin_delete_category(category_id):
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    
    category = Category.query.get_or_404(category_id)
    
    # 检查版块下是否有帖子
    if category.posts.count() > 0:
        flash('无法删除有帖子的版块')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('版块删除成功')
    
    return redirect(url_for('advanced.admin_categories'))

# 后台管理页面 - 帖子管理
@bp.route('/admin/posts')
@login_required
def admin_posts():
    if not current_user.is_admin:
        flash('您没有权限访问此页面')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/posts.html', posts=posts)

# 删除帖子
@bp.route('/admin/post/<post_id>/delete', methods=['POST'])
@login_required
def admin_delete_post(post_id):
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    
    post = Post.query.get_or_404(post_id)
    
    # 删除帖子相关的评论
    Comment.query.filter_by(post_id=post.id).delete()
    
    # 删除帖子相关的举报
    Report.query.filter_by(reported_type='post', reported_id=post.id).delete()
    
    # 删除帖子相关的投票
    Vote.query.filter_by(voted_type='post', voted_id=post.id).delete()
    
    # 删除帖子
    db.session.delete(post)
    db.session.commit()
    
    flash('帖子删除成功')
    return redirect(url_for('advanced.admin_posts'))

# 举报处理页面
@bp.route('/admin/reports')
@login_required
def admin_reports():
    if not current_user.is_admin:
        flash('您没有权限访问此页面')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    reports = Report.query.order_by(Report.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/reports.html', reports=reports)

# 处理举报
@bp.route('/admin/report/<int:report_id>/resolve', methods=['POST'])
@login_required
def resolve_report(report_id):
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    
    report = Report.query.get_or_404(report_id)
    report.status = 'resolved'
    db.session.commit()
    
    flash('举报已处理')
    return redirect(url_for('advanced.admin_reports'))

# 忽略举报
@bp.route('/admin/report/<int:report_id>/dismiss', methods=['POST'])
@login_required
def dismiss_report(report_id):
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    
    report = Report.query.get_or_404(report_id)
    report.status = 'dismissed'
    db.session.commit()
    
    flash('举报已忽略')
    return redirect(url_for('advanced.admin_reports'))

# 数据统计页面
@bp.route('/admin/analytics')
@login_required
def admin_analytics():
    if not current_user.is_admin:
        flash('您没有权限访问此页面')
        return redirect(url_for('main.index'))
    
    # 用户增长统计
    user_stats_result = db.session.query(
        db.func.date(User.created_at).label('date'),
        db.func.count(User.id).label('count')
    ).group_by(db.func.date(User.created_at)).all()
    
    # 转换为字典列表
    user_stats = [{'date': str(stat.date), 'count': stat.count} for stat in user_stats_result]
    
    # 帖子增长统计
    post_stats_result = db.session.query(
        db.func.date(Post.created_at).label('date'),
        db.func.count(Post.id).label('count')
    ).group_by(db.func.date(Post.created_at)).all()
    
    # 转换为字典列表
    post_stats = [{'date': str(stat.date), 'count': stat.count} for stat in post_stats_result]
    
    # 评论增长统计
    comment_stats_result = db.session.query(
        db.func.date(Comment.created_at).label('date'),
        db.func.count(Comment.id).label('count')
    ).group_by(db.func.date(Comment.created_at)).all()
    
    # 转换为字典列表
    comment_stats = [{'date': str(stat.date), 'count': stat.count} for stat in comment_stats_result]
    
    # 版块数据
    categories = Category.query.all()
    
    return render_template('admin/analytics.html', 
                          user_stats=user_stats,
                          post_stats=post_stats,
                          comment_stats=comment_stats,
                          categories=categories)

# 好友系统页面 - 好友列表
@bp.route('/friends')
@login_required
def friends():
    friends = current_user.friends.all()
    return render_template('friends.html', friends=friends)

# 添加好友
@bp.route('/add_friend/<int:user_id>', methods=['POST'])
@login_required
def add_friend(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('您不能添加自己为好友')
        return redirect(url_for('main.user_detail', user_id=user.id))
    
    current_user.add_friend(user)
    db.session.commit()
    
    flash(f'已添加 {user.username} 为好友')
    return redirect(url_for('main.user_detail', user_id=user.id))

# 移除好友
@bp.route('/remove_friend/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    user = User.query.get_or_404(user_id)
    
    current_user.remove_friend(user)
    db.session.commit()
    
    flash(f'已从好友列表中移除 {user.username}')
    return redirect(url_for('advanced.friends'))

# 私信聊天页面
@bp.route('/messages')
@login_required
def messages():
    # 获取与当前用户相关的消息
    messages = Message.query.filter(
        db.or_(
            Message.sender_id == current_user.id,
            Message.recipient_id == current_user.id
        )
    ).order_by(Message.created_at.desc()).all()
    
    # 获取唯一的对话用户
    user_ids = set()
    for msg in messages:
        if msg.sender_id != current_user.id:
            user_ids.add(msg.sender_id)
        if msg.recipient_id != current_user.id:
            user_ids.add(msg.recipient_id)
    
    users = User.query.filter(User.id.in_(user_ids)).all()
    
    # 添加获取最后消息的函数
    def get_last_message(user1_id, user2_id):
        last_message = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == user1_id, Message.recipient_id == user2_id),
                db.and_(Message.sender_id == user2_id, Message.recipient_id == user1_id)
            )
        ).order_by(Message.created_at.desc()).first()
        return last_message
    
    return render_template('messages.html', users=users, get_last_message=get_last_message)

# 私信聊天详情页面
@bp.route('/messages/<int:user_id>')
@login_required
def message_detail(user_id):
    user = User.query.get_or_404(user_id)
    
    # 获取对话消息
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.recipient_id == user.id),
            db.and_(Message.sender_id == user.id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()
    
    # 标记为已读
    for msg in messages:
        if msg.recipient_id == current_user.id:
            msg.is_read = True
    
    db.session.commit()
    
    return render_template('message_detail.html', user=user, messages=messages)

# 发送私信
@bp.route('/send_message/<int:user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    recipient = User.query.get_or_404(user_id)
    content = request.form['content']
    
    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient.id,
        content=content
    )
    
    db.session.add(message)
    db.session.commit()
    
    flash('消息已发送')
    return redirect(url_for('advanced.message_detail', user_id=recipient.id))

# 关注系统页面 - 关注列表
@bp.route('/following')
@login_required
def following():
    following = current_user.followed.all()
    return render_template('following.html', following=following)

# 粉丝列表页面
@bp.route('/followers')
@login_required
def followers():
    followers = current_user.followers.all()
    return render_template('followers.html', followers=followers)

# 关注用户
@bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('您不能关注自己')
        return redirect(url_for('main.user_detail', user_id=user.id))
    
    current_user.follow(user)
    db.session.commit()
    
    flash(f'已关注 {user.username}')
    return redirect(url_for('main.user_detail', user_id=user.id))

# 取消关注
@bp.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user = User.query.get_or_404(user_id)
    
    current_user.unfollow(user)
    db.session.commit()
    
    flash(f'已取消关注 {user.username}')
    return redirect(url_for('advanced.following'))

# 用户黑名单页面
@bp.route('/blacklist')
@login_required
def blacklist():
    blocked = current_user.blocked.all()
    return render_template('blacklist.html', blocked=blocked)

# 加入黑名单
@bp.route('/block/<int:user_id>', methods=['POST'])
@login_required
def block(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('您不能将自己加入黑名单')
        return redirect(url_for('main.user_detail', user_id=user.id))
    
    current_user.block(user)
    db.session.commit()
    
    flash(f'已将 {user.username} 加入黑名单')
    return redirect(url_for('main.user_detail', user_id=user.id))

# 移出黑名单
@bp.route('/unblock/<int:user_id>', methods=['POST'])
@login_required
def unblock(user_id):
    user = User.query.get_or_404(user_id)
    
    current_user.unblock(user)
    db.session.commit()
    
    flash(f'已将 {user.username} 移出黑名单')
    return redirect(url_for('advanced.blacklist'))

# 点赞/踩功能
@bp.route('/vote/<string:entity_type>/<entity_id>/<int:vote_type>', methods=['POST'])
@login_required
def vote(entity_type, entity_id, vote_type):
    # 验证投票类型
    if vote_type not in [1, -1]:
        flash('无效的投票类型')
        return redirect(request.referrer or url_for('main.index'))
    
    # 处理帖子投票
    if entity_type == 'post':
        post = Post.query.get_or_404(entity_id)
        
        # 检查是否已经投票
        existing_vote = Vote.query.filter_by(
            user_id=current_user.id,
            voted_type='post',
            voted_id=post.id
        ).first()
        
        if existing_vote:
            # 更新现有投票
            existing_vote.vote_type = vote_type
        else:
            # 创建新投票
            vote = Vote(
                user_id=current_user.id,
                voted_type='post',
                voted_id=post.id,
                vote_type=vote_type
            )
            db.session.add(vote)
        
        db.session.commit()
        flash('投票成功')
        
    # 处理评论投票
    elif entity_type == 'comment':
        comment = Comment.query.get_or_404(entity_id)
        
        # 检查是否已经投票
        existing_vote = Vote.query.filter_by(
            user_id=current_user.id,
            voted_type='comment',
            voted_id=comment.id
        ).first()
        
        if existing_vote:
            # 更新现有投票
            existing_vote.vote_type = vote_type
        else:
            # 创建新投票
            vote = Vote(
                user_id=current_user.id,
                voted_type='comment',
                voted_id=comment.id,
                vote_type=vote_type
            )
            db.session.add(vote)
        
        db.session.commit()
        flash('投票成功')
        
    else:
        flash('无效的实体类型')
        
    return redirect(request.referrer or url_for('main.index'))

# 收藏夹管理页面
@bp.route('/favorites')
@login_required
def favorites():
    favorites = current_user.favorites.order_by(Post.created_at.desc()).all()
    return render_template('favorites.html', favorites=favorites)

# 添加收藏
@bp.route('/favorite/<post_id>', methods=['POST'])
@login_required
def add_favorite(post_id):
    post = Post.query.get_or_404(post_id)
    
    if not current_user.is_favorite(post):
        current_user.add_favorite(post)
        db.session.commit()
        flash('已添加到收藏夹')
    else:
        flash('该帖子已在您的收藏夹中')
        
    return redirect(request.referrer or url_for('main.post_detail', post_id=post.id))

# 移除收藏
@bp.route('/unfavorite/<post_id>', methods=['POST'])
@login_required
def remove_favorite(post_id):
    post = Post.query.get_or_404(post_id)
    
    if current_user.is_favorite(post):
        current_user.remove_favorite(post)
        db.session.commit()
        flash('已从收藏夹移除')
        
    return redirect(request.referrer or url_for('advanced.favorites'))

# 转发分享功能
@bp.route('/share/<post_id>', methods=['POST'])
@login_required
def share_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # 创建新帖子作为转发
    content = request.form.get('content', '')
    shared_content = f"[转发自 @{post.author.username}]\n{post.content}"
    
    if content:
        shared_content = f"{content}\n\n{shared_content}"
    
    new_post = Post(
        title=f"转发: {post.title}",
        content=shared_content,
        author=current_user,
        category=post.category
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    flash('帖子已转发')
    return redirect(url_for('main.post_detail', post_id=new_post.id))

# @提醒功能
@bp.route('/mentions')
@login_required
def mentions():
    # 这里需要实现@提醒的逻辑
    # 由于简化实现，我们只显示最近的评论
    comments = Comment.query.filter(
        Comment.content.contains(f'@{current_user.username}')
    ).order_by(Comment.created_at.desc()).limit(20).all()
    
    return render_template('mentions.html', comments=comments)

# 标签系统页面
@bp.route('/tags')
def tags():
    # 获取标签及其帖子数量
    tag_stats = db.session.query(
        Tag,
        db.func.count(Post.id).label('post_count')
    ).join(Post, Tag.posts).group_by(Tag.id).all()
    
    return render_template('tags.html', tag_stats=tag_stats)

# 标签详情页面
@bp.route('/tag/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts.order_by(Post.created_at.desc()).all()
    return render_template('tag_detail.html', tag=tag, posts=posts)

# 精华帖页面
@bp.route('/essence')
def essence():
    posts = Post.query.filter_by(is_essence=True).order_by(Post.created_at.desc()).all()
    return render_template('essence.html', posts=posts)

# 用户投票页面 - 发起投票
@bp.route('/create_vote', methods=['GET', 'POST'])
@login_required
def create_vote():
    if request.method == 'POST':
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        category_id = request.form.get('category_id', type=int)
        expire_days = request.form.get('expire_days', 7, type=int)
        vote_type = request.form.get('vote_type', 'single')
        options = request.form.getlist('options[]')
        
        # 验证输入
        if not title:
            flash('请填写投票标题')
            return redirect(url_for('advanced.create_vote'))
        
        if not category_id:
            flash('请选择版块')
            return redirect(url_for('advanced.create_vote'))
        
        if len(options) < 2:
            flash('至少需要两个投票选项')
            return redirect(url_for('advanced.create_vote'))
        
        # 检查选项是否重复
        if len(options) != len(set(options)):
            flash('投票选项不能重复')
            return redirect(url_for('advanced.create_vote'))
        
        # 创建投票帖子
        expire_at = datetime.utcnow() + timedelta(days=expire_days)
        
        # 创建投票内容（简化实现，实际应该创建专门的投票表）
        vote_content = f"[投票]\n{description}\n\n选项:\n"
        for i, option in enumerate(options, 1):
            vote_content += f"{i}. {option}\n"
        vote_content += f"\n投票类型: {vote_type}\n截止时间: {expire_at.strftime('%Y-%m-%d %H:%M')}"
        
        post = Post(
            title=title,
            content=vote_content,
            user_id=current_user.id,
            category_id=category_id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('投票创建成功')
        return redirect(url_for('main.post_detail', post_id=post.id))
    
    categories = Category.query.all()
    return render_template('create_vote.html', categories=categories)

# 发帖统计页面
@bp.route('/post_stats')
@login_required
def post_stats():
    # 获取用户发帖统计
    post_count = current_user.posts.count()
    
    # 按版块统计
    category_stats = db.session.query(
        Category.name,
        db.func.count(Post.id).label('count')
    ).join(Post).filter(Post.user_id == current_user.id).group_by(Category.name).all()
    
    # 按时间统计（最近30天）
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_stats = db.session.query(
        db.func.date(Post.created_at).label('date'),
        db.func.count(Post.id).label('count')
    ).filter(
        Post.user_id == current_user.id,
        Post.created_at >= thirty_days_ago
    ).group_by(db.func.date(Post.created_at)).all()
    
    return render_template('post_stats.html', 
                          post_count=post_count,
                          category_stats=category_stats,
                          daily_stats=daily_stats)

# 互动历史页面
@bp.route('/interactions')
@login_required
def interactions():
    # 获取用户的评论
    comments = current_user.comments.order_by(Comment.created_at.desc()).limit(20).all()
    
    # 获取用户的投票
    votes = Vote.query.filter_by(user_id=current_user.id).order_by(Vote.created_at.desc()).limit(20).all()
    
    return render_template('interactions.html', comments=comments, votes=votes)

# 举报功能
@bp.route('/report/<string:entity_type>/<entity_id>', methods=['POST'])
@login_required
def report(entity_type, entity_id):
    reason = request.form.get('reason', '')
    
    if not reason:
        flash('请提供举报理由')
        return redirect(request.referrer or url_for('main.index'))
    
    # 创建举报记录
    report = Report(
        reporter_id=current_user.id,
        reported_type=entity_type,
        reported_id=entity_id,
        reason=reason
    )
    
    db.session.add(report)
    
    # 标记被举报的实体
    if entity_type == 'post':
        post = Post.query.get_or_404(entity_id)
        post.is_reported = True
    elif entity_type == 'comment':
        comment = Comment.query.get_or_404(entity_id)
        comment.is_reported = True
    
    db.session.commit()
    
    flash('举报已提交，管理员将尽快处理')
    return redirect(request.referrer or url_for('main.index'))
