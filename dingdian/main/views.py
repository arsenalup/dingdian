from flask import flash, render_template, url_for, redirect, request, current_app
from flask.blueprints import Blueprint

from dingdian import db
from .forms import SearchForm
from ..spider.spider import DdSpider
from ..models import Search, Novel, Chapter, Article

main = Blueprint('mian', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search_name.data
        data = Search(search_name=Search)
        ds.session.add(data)
        flash('搜索成功')
        return redirect(url_for('main.result', search=search))
    return render_template('index.html', form=form)


@main.route('/results/<search>')
def result(search):
    books = Novel.query.filter_by(search_name=search).all()
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
            lasy_update = data['time'],
            search_name = search
        )
        db.session.add(novel)
    books = Novel.query.filter_by(search_name=search).all()
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
























