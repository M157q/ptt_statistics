from datetime import datetime

from pony import orm

from . import models


@orm.db_session
def db_board(board):
    board_entity = models.Board.get(name=board.name)

    if board_entity is None:
        board_entity = models.Board(name=board.name,
                                    over18=bool(board.cookies['over18']))

    # orm.show(board_entity)


@orm.db_session
def db_article(article, board):
    board_entity = models.Board.get(name=board.name)
    article_entity = models.Article.get(identifier=article.id,
                                        board=board_entity)

    if article_entity is None:
        user_id = (article.author.split()[0]
                   if isinstance(article.author, str)
                   else '')
        user_entity = models.User.get(identifier=user_id)
        if user_entity is None:
            user_entity = models.User(identifier=user_id)

        article_type = (article.type.strip()
                        if isinstance(article.type, str)
                        else '')
        article_type_entity = models.ArticleType.get(name=article_type,
                                                     board=board_entity)
        if article_type_entity is None:
            article_type_entity = models.ArticleType(name=article_type,
                                                     board=board_entity)

        article_title = (article.title.strip()
                         if isinstance(article.title, str)
                         else '')
        article_title_entity = models.ArticleTitle.get(name=article_title,
                                                       board=board_entity)
        if article_title_entity is None:
            article_title_entity = models.ArticleTitle(name=article_title,
                                                       board=board_entity)

        article_entity = models.Article(identifier=article.id,
                                        url=article.url,
                                        user=user_entity,
                                        reply=bool(article.reply),
                                        type=article_type_entity,
                                        title=article_title_entity,
                                        datetime=article.time,
                                        content=article.content,
                                        board=board_entity)
    # elif article_entity.comments.count() > article.comments.count():
    # TODO: Add new comments

    # orm.show(article_entity)


@orm.db_session
def db_comment(comment, article, board):
    '''user, content, tag, time'''
    board_entity = models.Board.get(name=board.name)

    tag_entity = models.CommentTag.get(name=comment['tag'])
    if tag_entity is None:
        tag_entity = models.CommentTag(name=comment['tag'])

    user_entity = models.User.get(identifier=comment['user'])
    if user_entity is None:
        user_entity = models.User(identifier=comment['user'])

    comment_content_entity = models.CommentContent.get(s=comment['content'])
    if comment_content_entity is None:
        comment_content_entity = models.CommentContent(s=comment['content'])

    article_entity = models.Article.get(identifier=article.id,
                                        board=board_entity)

    # TODO: different board may have different time format for comments
    if isinstance(article_entity.datetime, datetime):
        article_year = article_entity.datetime.year
        date_time = datetime.strptime("{}/{}".format(article_year,
                                                     comment['time']),
                                      "%Y/%m/%d %H:%M")
        if date_time.month < article_entity.datetime.month:
            date_time = datetime.strptime("{}/{}".format(article_year+1,
                                                         comment['time']),
                                          "%Y/%m/%d %H:%M")
    else:
        date_time = datetime.strptime("{}/{}".format(9999,
                                                     comment['time']),
                                      "%Y/%m/%d %H:%M")

    comment_entity = models.Comment(tag=tag_entity,
                                    user=user_entity,
                                    content=comment_content_entity,
                                    datetime=date_time,
                                    article=article_entity)

    orm.show(comment_entity)
