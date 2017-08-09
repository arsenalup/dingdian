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