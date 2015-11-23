import datetime

from pony import orm

db = orm.Database()


class Board(db.Entity):
    name = orm.Required(str, unique=True)
    articles = orm.Set("Article")
    article_types = orm.Set("ArticleType")
    article_titles = orm.Set("ArticleTitle")


class User(db.Entity):
    identifier = orm.Optional(str, unique=True)
    articles = orm.Set("Article")
    comments = orm.Set("Comment")
    article_types = orm.Set("ArticleType")
    article_titles = orm.Set("ArticleTitle")


class Article(db.Entity):
    identifier = orm.Required(str)
    url = orm.Required(str, unique=True)
    user = orm.Required(User)
    reply = orm.Required(bool)
    type = orm.Required("ArticleType")
    title = orm.Required("ArticleTitle")
    date = orm.Optional(datetime.date, nullable=True)
    time = orm.Optional(datetime.time, nullable=True)
    content = orm.Optional(orm.LongStr, nullable=True)
    comments = orm.Set("Comment")
    board = orm.Required(Board)

    orm.composite_index(identifier, board)
    orm.composite_index(type, title, board)


class ArticleType(db.Entity):
    name = orm.Optional(str, nullable=True)
    board = orm.Required(Board)
    articles = orm.Set(Article)
    users = orm.Set(User)


class ArticleTitle(db.Entity):
    name = orm.Optional(str, nullable=True)
    board = orm.Required(Board)
    articles = orm.Set(Article)
    users = orm.Set(User)


class Comment(db.Entity):
    tag = orm.Required("CommentTag")
    user = orm.Required(User)
    content = orm.Required("CommentContent")
    date = orm.Optional(datetime.date, nullable=True)
    time = orm.Optional(datetime.time, nullable=True)
    article = orm.Required(Article)

    # orm.composite_index(tag, user, content, date, time, article)


class CommentTag(db.Entity):
    name = orm.Required(str, unique=True)
    comments = orm.Set(Comment)


class CommentContent(db.Entity):
    s = orm.Optional(str, unique=True, nullable=True)
    comments = orm.Set(Comment)
