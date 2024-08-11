from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # 데이터베이스 파일 이름을 확인하세요
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SQLAlchemy 모델 정의
class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))
    type = db.Column(db.String(20))

    def __repr__(self):
        return f"<Gallery(id='{self.id}', name='{self.name}', type='{self.type}')>"

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gallery_id = db.Column(db.String(20), db.ForeignKey('gallery.id'))
    
    gallery = db.relationship('Gallery', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', author='{self.author}', created_at={self.created_at}, gallery_id='{self.gallery_id}')>"

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    with app.app_context():
        # 갤러리 정보 출력
        galleries = Gallery.query.all()
        logger.info("갤러리 목록:")
        for gallery in galleries:
            logger.info(gallery)

        # 최신 10개의 포스트를 가져와서 출력
        latest_posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
        
        logger.info("\n최신 10개의 포스트:")
        for post in latest_posts:
            logger.info(post)
        
        # 데이터베이스에 있는 총 포스트 수 출력
        total_posts = Post.query.count()
        logger.info(f"\n데이터베이스에 총 {total_posts}개의 포스트가 있습니다.")

        # 각 gallery_id 별 포스트 수 출력
        gallery_counts = db.session.query(Post.gallery_id, db.func.count(Post.id)).group_by(Post.gallery_id).all()
        logger.info("\n각 갤러리별 포스트 수:")
        for gallery_id, count in gallery_counts:
            gallery_name = Gallery.query.get(gallery_id).name if Gallery.query.get(gallery_id) else "Unknown"
            logger.info(f"{gallery_id} ({gallery_name}): {count}개")

if __name__ == '__main__':
    check_database()