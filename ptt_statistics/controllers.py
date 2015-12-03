import datetime
import re
import sys
from collections import defaultdict
from pprint import pprint

from pony import orm

from . import models
from . import exceptions


@orm.db_session
def store_board(board):
    board_entity = models.Board.get(name=board.name)

    update_time = datetime.datetime.now()
    if board_entity is None:
        board_entity = models.Board(
            name=board.name,
            update_time=update_time
        )
    else:
        board_entity.update_time = update_time

    orm.show(board_entity)


@orm.db_session
def store_article(article, board):
    board_entity = models.Board.get(name=board.name)
    article_entity = models.Article.get(identifier=article.id,
                                        board=board_entity)

    update_time = datetime.datetime.now()
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

        try:
            article_date = article.time.date()
            article_time = article.time.time()
        except (AttributeError, ValueError):
            article_date = None
            article_time = None

        article_entity = models.Article(identifier=article.id,
                                        url=article.url,
                                        user=user_entity,
                                        reply=bool(article.reply),
                                        type=article_type_entity,
                                        title=article_title_entity,
                                        date=article_date,
                                        time=article_time,
                                        content=article.content,
                                        board=board_entity,
                                        update_time=update_time)
        board_entity.update_time = update_time
        pprint(vars(article))
        orm.show(article_entity)
    else:
        article_entity.update_time = update_time
        board_entity.update_time = update_time


@orm.db_session
def store_comment(comment, article, board):
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

    try:
        comment_year = article_entity.date.year
    except AttributeError:
        comment_year = datetime.MAXYEAR

    m = re.match(r"(\d+/\d+)?\s*(\d+:\d+)?", comment['time'])
    comment_date, comment_time = m.groups()
    if comment_date:
        comment_month, comment_day = map(int, comment_date.split('/'))

        try:
            article_month = article_entity.date.month
        except AttributeError:
            pass
        else:
            if (
                article_month == 12 and
                comment_month == 1 and
                comment_year != datetime.MAXYEAR
            ):
                comment_year += 1
            elif comment_month < article_month:
                return

        try:
            comment_date = datetime.date(comment_year,
                                         comment_month,
                                         comment_day)
        except ValueError:
            comment_date = None
    if comment_time:
        comment_hour, comment_min = map(int, comment_time.split(':'))
        try:
            comment_time = datetime.time(comment_hour, comment_min)
        except ValueError:
            comment_time = None

    try:
        comment_entity = models.Comment.get(
            tag=tag_entity,
            user=user_entity,
            content=comment_content_entity,
            date=comment_date,
            time=comment_time,
            article=article_entity
        )
    except:
        import traceback
        traceback.print_exc()
        orm.show(tag_entity)
        orm.show(user_entity)
        orm.show(comment_content_entity)
        print(comment_date)
        print(comment_time)
        orm.show(article_entity)
        print(article_entity.url)

    if comment_entity is None:
        comment_entity = models.Comment(tag=tag_entity,
                                        user=user_entity,
                                        content=comment_content_entity,
                                        date=comment_date,
                                        time=comment_time,
                                        article=article_entity)

        update_time = datetime.datetime.now()
        board_entity.update_time = update_time
        article_entity.update_time = update_time

        pprint(comment.items())
        orm.show(comment_entity)


@orm.db_session
def get_specific_day_info(board_name, **kargs):
    pass


@orm.db_session
def get_specific_month_info(board_name, **kargs):
    pass


@orm.db_session
def get_board_specific_year_info(board_name, year):

    board_entity = models.Board.get(name=board_name)

    if board_entity is None:
        raise exceptions.NoBoardError(board_name)

    board_year_record_entity = models.BoardYearRecord.get(
        year=year,
        board=board_entity.id
    )

    if board_year_record_entity is None:
        board_year_record_entity = models.BoardYearRecord(
            year=year,
            board=board_entity,
            update_time=datetime.datetime.now(),
        )

    board = {
        'name': board_year_record_entity.board.name,
        'year': board_year_record_entity.year,
        'update_time': board_year_record_entity.board.update_time,
    }

    return board

@orm.db_session
def get_specific_year_info(board_name, year):

    board_entity = models.Board.get(name=board_name)

    if board_entity is None:
        raise exceptions.NoBoardError(board_name)

    board_year_record_entity = models.BoardYearRecord.get(
        year=kargs['year'],
        board=board_entity.id
    )

    if (
        board_year_record_entity
        and board_year_record_entity.update_time > board_entity.update_time
    ):
        board = {
            'name': board_entity.name,
            'year': kargs['year'],
            'update_time': board_entity.update_time,
        }
        articles = {
            'total': board_year_record_entity.articles_total,
            'months': eval(board_year_record_entity.articles_months),
            'total_users': board_year_record_entity.articles_total_users,
        }
        comments = {
            'total': board_year_record_entity.comments_total,
            'tags': eval(board_year_record_entity.comments_tags),
            'total_users': board_year_record_entity.comments_total_users,
        }
        users = {
            'total': board_year_record_entity.users_total,
            'comment_or_post':
                eval(board_year_record_entity.users_comment_or_post),
        }
        top_n = {
            'total_articles': eval(
                board_year_record_entity.top_n_total_articles
            ),
            'total_push_comments_gained': eval(
                board_year_record_entity.top_n_total_push_comments_gained
            ),
            'total_boo_comments_gained': eval(
                board_year_record_entity.top_n_total_boo_comments_gained
            ),
            'total_push_comments_used': eval(
                board_year_record_entity.top_n_total_push_comments_used
            ),
            'total_boo_comments_used': eval(
                board_year_record_entity.top_n_total_boo_comments_used
            ),
        }
    else:
        update_time = datetime.datetime.now()

        # Board
        board = {}
        board['name'] = board_entity.name
        board['year'] = kargs['year']
        board['update_time'] = board_entity.update_time

        # Articles
        total_articles = orm.select(
            article for article in models.Article
            if article.date.year == kargs['year']
            and article.board.name == board_name
        )
        articles = {}
        articles['total'] = total_articles.count()

        articles['months'] = {
            month: orm.count(
                article
                for article in total_articles
                if article.date.month == month)
            for month in range(1, 13)
        }

        articles['total_users'] = orm.count(article.user
                                            for article in total_articles)

        # Comments
        total_comments = orm.select(
            comment
            for comment in models.Comment
            if comment.date.year == kargs['year']
            and comment.article.board.name == board_name
        )
        comments = {}
        tag_names = orm.select(tag.name for tag in models.CommentTag)
        comments['total'] = total_comments.count()
        comments['tags'] = {
            tag_name: orm.count(
                comment
                for comment in total_comments
                if comment.tag.name == tag_name
            )
            for tag_name in tag_names
        }

        comments['total_users'] = orm.count(comment.user
                                            for comment in total_comments)

        # Users
        users = {}
        users['comment_or_post'] = {}
        users['comment_or_post']['發文且留言'] = orm.count(
            article.user
            for article in total_articles
            if article.user.comments.select(
                lambda c: c.date.year == kargs['year']
            )
        )
        users['comment_or_post']['只留言'] = (
            comments['total_users'] - users['comment_or_post']['發文且留言']
        )
        users['comment_or_post']['只發文'] = (
            articles['total_users'] - users['comment_or_post']['發文且留言']
        )

        users['total'] = {}
        users['total'] = (
            articles['total_users'] + comments['total_users']
            - users['comment_or_post']['發文且留言']
        )

        # Top N
        top_n = {}
        top_n['total_articles'] = defaultdict(int)
        top_n['total_push_comments_gained'] = defaultdict(int)
        top_n['total_boo_comments_gained'] = defaultdict(int)
        for article in total_articles:
            author = article.user.identifier
            top_n['total_articles'][author] += 1

            for comment in article.comments:
                if comment.tag.name == '推':
                    top_n['total_push_comments_gained'][author] += 1
                if comment.tag.name == '噓':
                    top_n['total_boo_comments_gained'][author] += 1

        top_n['total_push_comments_used'] = defaultdict(int)
        top_n['total_boo_comments_used'] = defaultdict(int)
        for comment in total_comments:
            if comment.tag.name == '推':
                top_n['total_push_comments_used'][comment.user.identifier] += 1
            if comment.tag.name == '噓':
                top_n['total_boo_comments_used'][comment.user.identifier] += 1

        if board_year_record_entity:
            board_year_record_entity.set(
                update_time=update_time,
                articles_total=articles['total'],
                articles_months=repr(articles['months']),
                articles_total_users=articles['total_users'],
                comments_total=comments['total'],
                comments_tags=repr(comments['tags']),
                comments_total_users=comments['total_users'],
                users_total=users['total'],
                users_comment_or_post=repr(users['comment_or_post']),
                top_n_total_articles=repr(
                    top_n['total_articles']
                ).replace("<class 'int'>", "int"),
                top_n_total_push_comments_gained=repr(
                    top_n['total_push_comments_gained']
                ).replace("<class 'int'>", "int"),
                top_n_total_boo_comments_gained=repr(
                    top_n['total_boo_comments_gained']
                ).replace("<class 'int'>", "int"),
                top_n_total_push_comments_used=repr(
                    top_n['total_push_comments_used']
                ).replace("<class 'int'>", "int"),
                top_n_total_boo_comments_used=repr(
                     top_n['total_boo_comments_used']
                ).replace("<class 'int'>", "int"),
            )
        else:
            board_year_record_entity = models.BoardYearRecord(
                year=kargs['year'],
                board=board_entity.id,
                update_time=update_time,
                articles_total=articles['total'],
                articles_months=repr(articles['months']),
                articles_total_users=articles['total_users'],
                comments_total=comments['total'],
                comments_tags=repr(comments['tags']),
                comments_total_users=comments['total_users'],
                users_total=users['total'],
                users_comment_or_post=repr(users['comment_or_post']),
                top_n_total_articles=repr(
                    top_n['total_articles']
                ).replace("<class 'int'>", "int"),
                top_n_total_push_comments_gained=repr(
                    top_n['total_push_comments_gained']
                ).replace("<class 'int'>", "int"),
                top_n_total_boo_comments_gained=repr(
                    top_n['total_boo_comments_gained']
                ).replace("<class 'int'>", "int"),
                top_n_total_push_comments_used=repr(
                    top_n['total_push_comments_used']
                ).replace("<class 'int'>", "int"),
                top_n_total_boo_comments_used=repr(
                    top_n['total_boo_comments_used']
                ).replace("<class 'int'>", "int"),
            )

        orm.show(board_year_record_entity)

    data = {}
    sub_dicts = ('board', 'articles', 'comments', 'users', 'top_n')
    for sub_dict in sub_dicts:
        data[sub_dict] = eval(sub_dict)

    return data
