from dingdian import db

#search模型
class Search(db.model):
    #设置表格名
    __tablename__ = 'searches'
    id = db.Column(db.Integer, primary_key=True)
    search_name = db.Column(db.String(64), index=True)
    #db.relationship的第一个参数说明另一端的模型是哪一个
    #backerf的值是向另一端的模型加一个属性，反向应用
    #lazy指定jioned的加载记录，使用联接
    novels = db.relationship('Novel', backref='search', lazy='joined')


#Novel模型
class Novel(db.model):
    __tablename__ = 'novels'
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(64), index=True)
    book_url = db.Column(db.String)
    book_img = db.Column(db.String)
    author = db.Column(db.String(64))
    style = db.Column(db.String(64), nullable=True)
    last_update = db.Column(db.String(64), nullable=True)
    profile = db.Column(db.Text, nullable=True)
    #db.foreignkey 外键
    search_name = db.Column(db.String, db.ForeignKey('searches.search_name'))
    chapters = db.relationship('Chapter', backref='book', lazy='dynamic')


class