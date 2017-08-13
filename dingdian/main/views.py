from flask import flash, render_template, url_for, redirect, request, current_app
from flask.blueprints import Blueprint

from dingdian import db
from .forms import SearchForm
from ..spider.spider import DdSpider
from ..models import Search, Novel, Chapter, Article

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search_name.data
        data = Search(search_name=search)
        db.session.add(data)
        db.session.commit()
        flash('搜索成功。')
        return redirect(url_for('main.result', search=search))
    return render_template('index.html', form=form)


@main.route('/results/<search>')
def result(search):
    books = Novel.query.filter_by(search_name=search).all()
    db.session.rollback()
    if books:
        return render_template('result.html', search=search, books=books)

    spider = DdSpider()
    for data in spider.get_index_result(search):
        novel = Novel(
            book_name = data['title'],
            book_url = data['url'],
            book_img = data['image'],
            author = data['author'],
            style = data['style'],
            profile = data['profile'],
            last_update = data['time'],
            search_name = search)
        db.session.add(novel)
        try:
            db.session.commit()
        except:
            db.session.rollback()
    books = Novel.query.filter_by(search_name=search).all()
    db.session.rollback()
    return render_template('result.html', search=search, books=books)


@main.route('/chapter/<int:book_id>')
def chapter(book_id):
    page = request.args.get('page', 1, type=int)
    all_chapter = Chapter.query.filter_by(book_id=book_id).first()
    if all_chapter:
        pagination = Chapter.query.filter_by(book_id=book_id).paginate(
            page, per_page=current_app.config['CHAPTER_PER_PAGE'], error_out=False
        )
        chapters = pagination.items
        book = Novel.query.filter_by(id=book_id).first()
        return render_template('chapter.html', book=book, chapters=chapters, pagination=pagination)

    spider = DdSpider()
    book = Novel.query.filter_by(id=book_id).first()
    for data in spider.get_chapter(book.book_url):
        chapter = Chapter(chapter=data['chapter'],
                          chapter_url=data['url'],
                          book_id=book_id)
        db.session.add(chapter)
    pagination2 = Chapter.query.filter_by(book_id=book_id).paginate(
        page, per_page=current_app.config['CHAPTER_PER_PAGE'], error_out=False
    )
    chapters = pagination2.items
    return render_template('chapter.html', book=book, chapters=chapters, pagination=pagination2)


@main.route('/content/<int:chapter_id>')
def content(chapter_id):
    book_id = Chapter.query.filter_by(id=chapter_id).first().book_id
    article = Article.query.filter_by(chapter_id=chapter_id).first()
    if article:
        chapter = Chapter.query.filter_by(id=chapter_id).first()
        return render_template('article.html', chapter=chapter, article=article, book_id=book_id)

    spider = DdSpider()
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    article2 = Article(content=spider.get_article(chapter.chapter_url), chapter_id=chapter_id)
    db.session.add(article2)
    return  render_template('atricle.html', chapter=chapter, article=article2, book_id=book_id)






















