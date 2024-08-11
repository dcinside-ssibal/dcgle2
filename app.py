from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from sqlalchemy import func
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False

db = SQLAlchemy(app)
scheduler = BackgroundScheduler()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))
    type = db.Column(db.String(20))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gallery_id = db.Column(db.String(20), db.ForeignKey('gallery.id'))
    link = db.Column(db.String(200))

    gallery = db.relationship('Gallery', backref=db.backref('posts', lazy=True))


def init_galleries():
    with app.app_context():
        galleries = [
            {'id': 'tcggame', 'name': 'TCG', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=tcggame', 'type': 'minor'},
            {'id': 'galaxy', 'name': '갤럭시', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=galaxy', 'type': 'minor'},
            {'id': 'galaxy_tab', 'name': '갤럭시탭', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=galaxy_tab', 'type': 'minor'},
            {'id': 'newjeans', 'name': '뉴진스', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=newjeans', 'type': 'minor'},
            {'id': 'lobotomycorporation', 'name': '로보토미 코퍼레이션', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=lobotomycorporation', 'type': 'minor'},
            {'id': 'loaon', 'name': '로아온', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=loaon', 'type': 'minor'},
            {'id': 'comic_new4', 'name': '만화', 'url': 'https://gall.dcinside.com/board/lists?id=comic_new4', 'type': 'official'},
            {'id': 'wutheringwaves', 'name': '명조 워더링 웨이브', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=wutheringwaves', 'type': 'minor'},
            {'id': 'ptjabcd', 'name': '박태준유니버스', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=ptjabcd', 'type': 'minor'},
            {'id': 'staraiload', 'name': '붕괴 스타레일', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=staraiload', 'type': 'minor'},
            {'id': 'stellive', 'name': '스텔라이브', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=stellive', 'type': 'minor'},
            {'id': 'gaon', 'name': '써클차트', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=gaon', 'type': 'minor'},
            {'id': 'els', 'name': '엘리오스', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=els', 'type': 'minor'},
            {'id': 'yjrs', 'name': '여장', 'url': 'https://gall.dcinside.com/board/lists/?id=yjrs', 'type': 'official'},
            {'id': 'umamusu', 'name': '우마무스메 프리티 더비', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=umamusu', 'type': 'minor'},
            {'id': 'onshinproject', 'name': '원신 project', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=onshinproject', 'type': 'minor'},
            {'id': 'masterduel', 'name': '유희왕 마스터듀얼', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=masterduel', 'type': 'minor'},
            {'id': 'leesedol', 'name': '이세계아이돌갤러리', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=leesedol', 'type': 'minor'},
            {'id': 'genrenovel', 'name': '장르소설', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=genrenovel', 'type': 'minor'},
            {'id': 'ckierun', 'name': '쿠키런 모험의 탑', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=ckierun', 'type': 'minor'},
            {'id': 'thesingularity', 'name': '특이점이 온다', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=thesingularity', 'type': 'minor'},
            {'id': 'prospect', 'name': '퓨처스리그', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=prospect', 'type': 'minor'},
            {'id': 'pjsekaikr', 'name': '프로젝트 세카이 한국서버', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=pjsekaikr', 'type': 'minor'},
            {'id': 'pjsekaikr', 'name': '프로젝트 세카이 한국서버', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=pjsekaikr', 'type': 'minor'},
            {'id': 'newheadphone', 'name': '헤드폰', 'url': 'https://gall.dcinside.com/mgallery/board/lists/?id=newheadphone', 'type': 'minor'}
        ]


        for gallery_data in galleries:
            existing_gallery = Gallery.query.filter_by(id=gallery_data['id']).first()
            if not existing_gallery:
                gallery = Gallery(
                    id=gallery_data['id'],
                    name=gallery_data['name'],
                    url=gallery_data['url'],
                    type=gallery_data['type']
                )
                db.session.add(gallery)
        db.session.commit()

def crawl_galleries():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        with app.app_context():
            galleries = Gallery.query.all()
            print(galleries)
            total_new_posts = 0
            for gallery in galleries:
                response = requests.get(gallery.url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                posts = soup.select('tr.ub-content')

                new_posts_count = 0
                for post in posts:
                    post_id = post.get('data-no')
                    if not post_id:
                        continue

                    post_id = int(post_id)
                    title_element = post.select_one('.gall_tit a')
                    title = title_element.text.strip()

                    link = title_element['href']
                    full_link = f"https://gall.dcinside.com{link}"

                    author_elem = post.select_one('.gall_writer')
                    if author_elem:
                        author_text = author_elem.get_text(strip=True)
                        if author_text == 'ㅇㅇ':
                            author = author_elem['data-uid']  # 'ㅇㅇ'일 경우 data-uid 속성 가져오기
                        else:
                            author = author_text
                    else:
                        author = ''

                    created_at_str = post.select_one('.gall_date')['title']
                    created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')

                    existing_post = Post.query.get(post_id)
                    if not existing_post:
                        new_post = Post(
                            id=post_id,
                            title=title,
                            author=author,
                            created_at=created_at,
                            gallery_id=gallery.id,
                            link=full_link
                        )
                        db.session.add(new_post)
                        new_posts_count += 1

                total_new_posts += new_posts_count

            db.session.commit()
            logger.info(f"Crawling completed. Total {total_new_posts} new posts added")

    except Exception as e:
        logger.error(f"Error during crawling: {e}")
        db.session.rollback()

def scheduled_crawl():
    with app.app_context():
        crawl_galleries()

def init_app():
    with app.app_context():
        db.create_all()  # 데이터베이스의 테이블 생성
        init_galleries()  # 초기 갤러리 데이터 추가
        
        scheduler.add_job(scheduled_crawl, 'interval', minutes=1)
        scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    galleries = Gallery.query.order_by(Gallery.name).all()
    gallery_id = request.form.get('gallery_id', 'all')
    query = request.form.get('query', '')

    if gallery_id == 'all':
        if query:
            search_results = Post.query.filter(or_(Post.title.contains(query),
                                                   Post.author.contains(query))).order_by(Post.created_at.desc()).paginate(page=request.args.get('page', 1, type=int), per_page=30)
        else:
            search_results = Post.query.order_by(Post.created_at.desc()).paginate(page=request.args.get('page', 1, type=int), per_page=30)
    else:
        if query:
            search_results = Post.query.filter(Post.gallery_id == gallery_id,
                                               or_(Post.title.contains(query),
                                                   Post.author.contains(query))).order_by(Post.created_at.desc()).paginate(page=request.args.get('page', 1, type=int), per_page=30)
        else:
            search_results = Post.query.filter_by(gallery_id=gallery_id).order_by(Post.created_at.desc()).paginate(page=request.args.get('page', 1, type=int), per_page=30)

    return render_template('index.html', search_results=search_results, query=query, galleries=galleries, selected_gallery=gallery_id)


if __name__ == '__main__':
    init_app()
    app.run(host='0.0.0.0', port=80)
