from datetime import datetime

from pony import orm

db = orm.Database()


class Board(db.Entity):
    name = orm.Required(str, unique=True)
    over18 = orm.Required(bool)
    articles = orm.Set("Article")


class Person(db.Entity):
    identifier = orm.Required(str, unique=True)
    articles = orm.Set("Article")
    comments = orm.Set("Comment")


class Article(db.Entity):
    identifier = orm.Required(str, unique=True)
    url = orm.Required(str, unique=True)
    author = orm.Required(Person)
    reply = orm.Required(bool)
    type = orm.Optional(str)
    title = orm.Required(str)
    time = orm.Required(datetime)
    content = orm.Required(orm.LongStr)
    comments = orm.Set("Comment")
    in_which_board = orm.Required(Board)


class Comment(db.Entity):
    tag = orm.Required("Tag")
    user = orm.Required(Person)
    content = orm.Required(str)
    time = orm.Required(datetime)
    in_which_article = orm.Required(Article)


class Tag(db.Entity):
    name = orm.Required(str)
    comments = orm.Set(Comment)
