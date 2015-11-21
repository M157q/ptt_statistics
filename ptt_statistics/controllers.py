from datetime import datetime

from pony import orm

from . import models


@orm.db_session
def db_board(board):
    board_entity = models.Board.get(name=board.name)

    if board_entity is None:
        board_entity = models.Board(name=board.name,
                                    over18=bool(board.cookies['over18']))
    models.Board.select().show()


@orm.db_session
def db_article(article, board):
    article_entity = models.Article.get(identifier=article.id)
    board_entity = models.Board.get(name=board.name)

    if article_entity is None:
        author_id = article.author.split()[0]
        author = models.Person.get(identifier=author_id)
        if author is None:
            author = models.Person(identifier=author_id)

        time = datetime.strptime(article.time, "%Y-%m-%d %H:%M:%S")

        article_entity = models.Article(identifier=article.id,
                                        url=article.url,
                                        author=author,
                                        reply=bool(article.reply),
                                        type=article.type.strip(),
                                        title=article.title,
                                        time=time,
                                        content=article.content,
                                        in_which_board=board_entity)
    elif article_entity.comments.count() > article.comments.count():
            # TODO: Add new comments
            pass

    models.Article.select().show()
