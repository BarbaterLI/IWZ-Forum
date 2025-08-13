from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db
import markdown
import uuid

# 用户好友关系表
user_friends = db.Table('user_friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# 用户关注关系表
user_follows = db.Table('user_follows',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# 用户黑名单关系表
user_blacklist = db.Table('user_blacklist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('blocked_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# 帖子标签关联表
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# 帖子收藏关联表
post_favorites = db.Table('post_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

# 帖子点赞/踩关联表
post_votes = db.Table('post_votes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('vote_type', db.Integer)  # 1: 赞, -1: 踩
)

# 评论点赞/踩关联表
comment_votes = db.Table('comment_votes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True),
    db.Column('vote_type', db.Integer)  # 1: 赞, -1: 踩
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(200), default='default.jpg')
    bio = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    # 好友关系
    friends = db.relationship('User', secondary=user_friends,
                              primaryjoin=(user_friends.c.user_id == id),
                              secondaryjoin=(user_friends.c.friend_id == id),
                              backref=db.backref('friend_of', lazy='dynamic'),
                              lazy='dynamic')
    
    # 关注关系
    followed = db.relationship('User', secondary=user_follows,
                               primaryjoin=(user_follows.c.user_id == id),
                               secondaryjoin=(user_follows.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    
    # 黑名单关系
    blocked = db.relationship('User', secondary=user_blacklist,
                              primaryjoin=(user_blacklist.c.user_id == id),
                              secondaryjoin=(user_blacklist.c.blocked_id == id),
                              backref=db.backref('blocked_by', lazy='dynamic'),
                              lazy='dynamic')
    
    # 收藏关系
    favorites = db.relationship('Post', secondary=post_favorites,
                                backref=db.backref('favorited_by', lazy='dynamic'),
                                lazy='dynamic')
    
    # 帖子投票关系
    post_votes = db.relationship('Post', secondary=post_votes,
                                 backref=db.backref('voted_by', lazy='dynamic'),
                                 lazy='dynamic')
    
    # 评论投票关系
    comment_votes = db.relationship('Comment', secondary=comment_votes,
                                    backref=db.backref('voted_by', lazy='dynamic'),
                                    lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def is_friend(self, user):
        return self.friends.filter(user_friends.c.friend_id == user.id).count() > 0
        
    def add_friend(self, user):
        if not self.is_friend(user):
            self.friends.append(user)
            
    def remove_friend(self, user):
        if self.is_friend(user):
            self.friends.remove(user)
            
    def is_following(self, user):
        return self.followed.filter(user_follows.c.followed_id == user.id).count() > 0
        
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            
    def is_blocked(self, user):
        return self.blocked.filter(user_blacklist.c.blocked_id == user.id).count() > 0
        
    def block(self, user):
        if not self.is_blocked(user):
            self.blocked.append(user)
            
    def unblock(self, user):
        if self.is_blocked(user):
            self.blocked.remove(user)
            
    def is_favorite(self, post):
        return self.favorites.filter(post_favorites.c.post_id == post.id).count() > 0
        
    def add_favorite(self, post):
        if not self.is_favorite(post):
            self.favorites.append(post)
            
    def remove_favorite(self, post):
        if self.is_favorite(post):
            self.favorites.remove(post)
            
    def vote_post(self, post, vote_type):
        # 检查是否已经投票
        existing_vote = db.session.query(post_votes).filter_by(
            user_id=self.id, post_id=post.id
        ).first()
        
        if existing_vote:
            # 更新现有投票
            stmt = post_votes.update().where(
                db.and_(
                    post_votes.c.user_id == self.id,
                    post_votes.c.post_id == post.id
                )
            ).values(vote_type=vote_type)
            db.session.execute(stmt)
        else:
            # 添加新投票
            stmt = post_votes.insert().values(
                user_id=self.id, post_id=post.id, vote_type=vote_type
            )
            db.session.execute(stmt)
        
    def get_post_vote(self, post):
        vote = db.session.query(post_votes).filter_by(user_id=self.id, post_id=post.id).first()
        return vote.vote_type if vote else 0
        
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', secondary=post_tags, backref='tags', lazy='dynamic')
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Post(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: f"iwz-f-{uuid.uuid4()}")
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = db.Column(db.Integer, default=0)
    is_essence = db.Column(db.Boolean, default=False)  # 精华帖
    is_locked = db.Column(db.Boolean, default=False)   # 锁定帖子
    is_reported = db.Column(db.Boolean, default=False) # 被举报
    file_path = db.Column(db.String(300))              # 上传的文件路径
    file_name = db.Column(db.String(200))              # 上传的文件名
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    attachments = db.relationship('Attachment', backref='post', lazy='dynamic')
    
    def get_vote_count(self):
        # 计算赞/踩数量
        votes = db.session.query(post_votes).filter_by(post_id=self.id).all()
        upvotes = sum(1 for vote in votes if vote.vote_type == 1)
        downvotes = sum(1 for vote in votes if vote.vote_type == -1)
        return upvotes, downvotes
        
    def get_content_html(self):
        # 将Markdown内容转换为HTML
        md = markdown.Markdown(extensions=['fenced_code', 'tables'])
        html = md.convert(self.content)
        # 确保代码块被正确包装以便复制功能工作
        return html
        
    def __repr__(self):
        return f'<Post {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_reported = db.Column(db.Boolean, default=False) # 被举报
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    def get_vote_count(self):
        # 计算赞/踩数量
        votes = db.session.query(comment_votes).filter_by(comment_id=self.id).all()
        upvotes = sum(1 for vote in votes if vote.vote_type == 1)
        downvotes = sum(1 for vote in votes if vote.vote_type == -1)
        return upvotes, downvotes
        
    def get_content_html(self):
        # 将Markdown内容转换为HTML
        md = markdown.Markdown(extensions=['fenced_code', 'tables'])
        return md.convert(self.content)
    
    def __repr__(self):
        return f'<Comment {self.id}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    # 关系
    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    
    def __repr__(self):
        return f'<Message {self.id}>'

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reported_type = db.Column(db.String(20), nullable=False)  # 'post' or 'comment'
    reported_id = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, resolved, dismissed
    
    # 关系
    reporter = db.relationship('User', foreign_keys=[reporter_id])
    
    def __repr__(self):
        return f'<Report {self.id}>'

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    voted_type = db.Column(db.String(20), nullable=False)  # 'post' or 'comment'
    voted_id = db.Column(db.Integer, nullable=False)
    vote_type = db.Column(db.Integer, nullable=False)  # 1: 赞, -1: 踩
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<Vote {self.id}>'

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)    # 文件名
    file_path = db.Column(db.String(300), nullable=False)   # 文件路径
    file_size = db.Column(db.Integer)                       # 文件大小(字节)
    file_type = db.Column(db.String(50))                    # 文件类型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 关系
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<Attachment {self.filename}>'
