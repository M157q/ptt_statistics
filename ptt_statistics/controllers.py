import datetime
import re
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
        board=board_entity
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
def get_articles_specific_year_info(board_name, year):

    board_entity = models.Board.get(name=board_name)

    if board_entity is None:
        raise exceptions.NoBoardError(board_name)

    board_year_record_entity = models.BoardYearRecord.get(
        year=year,
        board=board_entity
    )

    if not (
        board_year_record_entity
        and board_year_record_entity.update_time > board_entity.update_time
        and board_year_record_entity.articles_total
        and board_year_record_entity.articles_months
        and board_year_record_entity.articles_total_users
    ):
        update_time = datetime.datetime.now()

        if board_year_record_entity is None:
            board_year_record_entity = models.BoardYearRecord(
                year=year,
                board=board_entity,
                update_time=update_time,
            )

        year_articles = orm.select(
            article for article in models.Article
            if article.date.year == year
            and article.board.name == board_name
        )
        months = {
            month: orm.count(
                article
                for article in year_articles
                if article.date.month == month)
            for month in range(1, 13)
        }
        total_users = orm.count(article.user for article in year_articles)

        board_year_record_entity.set(
            articles_total=year_articles.count(),
            articles_months=repr(months),
            articles_total_users=total_users,
            update_time=update_time,
        )

    articles = {
        'total': board_year_record_entity.articles_total,
        'months': eval(board_year_record_entity.articles_months),
        'total_users': board_year_record_entity.articles_total_users,
    }

    return articles


@orm.db_session
def get_comments_specific_year_info(board_name, year):

    board_entity = models.Board.get(name=board_name)

    if board_entity is None:
        raise exceptions.NoBoardError(board_name)

    board_year_record_entity = models.BoardYearRecord.get(
        year=year,
        board=board_entity
    )

    if not (
        board_year_record_entity
        and board_year_record_entity.update_time > board_entity.update_time
        and board_year_record_entity.comments_total
        and board_year_record_entity.comments_tags
        and board_year_record_entity.comments_total_users
    ):
        update_time = datetime.datetime.now()

        if board_year_record_entity is None:
            board_year_record_entity = models.BoardYearRecord(
                year=year,
                board=board_entity,
                update_time=update_time,
            )

        tags = defaultdict(int)
        for tag_name in orm.select(
            comment.tag.name
            for comment in models.Comment
            if comment.date.year == year
            and comment.article.board.name == board_name
        ).without_distinct():
            tags[tag_name] += 1

        total_users = orm.select(
            comment.user
            for comment in models.Comment
            if comment.date.year == year
            and comment.article.board.name == board_name
        ).count()

        total = orm.select(
            comment
            for comment in models.Comment
            if comment.date.year == year
            and comment.article.board.name == board_name
        ).count()

        board_year_record_entity.set(
            comments_total=total,
            comments_tags=repr(tags).replace("<class 'int'>", "int"),
            comments_total_users=total_users,
            update_time=update_time,
        )

    comments = {
        'total': board_year_record_entity.comments_total,
        'tags': eval(board_year_record_entity.comments_tags),
        'total_users': board_year_record_entity.comments_total_users,
    }

    return comments


@orm.db_session
def get_users_specific_year_info(
    board_name,
    year,
    articles_total_users,
    comments_total_users,
):

    board_entity = models.Board.get(name=board_name)

    if board_entity is None:
        raise exceptions.NoBoardError(board_name)

    board_year_record_entity = models.BoardYearRecord.get(
        year=year,
        board=board_entity
    )

    if not (
        board_year_record_entity
        and board_year_record_entity.update_time > board_entity.update_time
        and board_year_record_entity.users_total
        and board_year_record_entity.users_comment_or_post
    ):
        update_time = datetime.datetime.now()

        if board_year_record_entity is None:
            board_year_record_entity = models.BoardYearRecord(
                year=year,
                board=board_entity,
                update_time=update_time,
            )

        comment_or_post = {}
        year_articles = orm.select(
            article for article in models.Article
            if article.date.year == year
            and article.board.name == board_name
        )
        comment_or_post['發文且留言'] = orm.count(
            article.user
            for article in year_articles
            if article.user.comments.select(
                lambda c: c.date.year == year
            )
        )
        comment_or_post['只留言'] = (
            comments_total_users - comment_or_post['發文且留言']
        )
        comment_or_post['只發文'] = (
            articles_total_users - comment_or_post['發文且留言']
        )

        total = (
            articles_total_users
            + comments_total_users
            - comment_or_post['發文且留言']
        )

        board_year_record_entity.set(
            users_total=total,
            users_comment_or_post=repr(comment_or_post),
            update_time=update_time,
        )

    users = {
        'total': board_year_record_entity.users_total,
        'comment_or_post': eval(
            board_year_record_entity.users_comment_or_post
        ),
    }

    return users


@orm.db_session
def get_top_n_total_articles_and_comments_gained_specific_year_info(
    board_name,
    year,
):

    board_entity = models.Board.get(name=board_name)

    if board_entity is None:
        raise exceptions.NoBoardError(board_name)

    board_year_record_entity = models.BoardYearRecord.get(
        year=year,
        board=board_entity
    )

    if not (
        board_year_record_entity
        and board_year_record_entity.update_time > board_entity.update_time
        and board_year_record_entity.top_n_total_articles
        and board_year_record_entity.top_n_total_push_comments_gained
        and board_year_record_entity.top_n_total_boo_comments_gained
    ):
        update_time = datetime.datetime.now()

        if board_year_record_entity is None:
            board_year_record_entity = models.BoardYearRecord(
                year=year,
                board=board_entity,
                update_time=update_time,
            )

        total_articles = defaultdict(int)
        total_push_comments_gained = defaultdict(int)
        total_boo_comments_gained = defaultdict(int)

        year_articles = orm.select(
            article for article in models.Article
            if article.date.year == year
            and article.board.name == board_name
        )
        for article in year_articles:
            author = article.user.identifier
            total_articles[author] += 1

            for comment in article.comments:
                if comment.tag.name == '推':
                    total_push_comments_gained[author] += 1
                if comment.tag.name == '噓':
                    total_boo_comments_gained[author] += 1

        board_year_record_entity.set(
            top_n_total_articles=repr(
                total_articles
            ).replace("<class 'int'>", "int"),
            top_n_total_push_comments_gained=repr(
                total_push_comments_gained
            ).replace("<class 'int'>", "int"),
            top_n_total_boo_comments_gained=repr(
                total_boo_comments_gained
            ).replace("<class 'int'>", "int"),
        )

    total_articles = eval(
        board_year_record_entity.top_n_total_articles
    )
    total_push_comments_gained = eval(
        board_year_record_entity.top_n_total_push_comments_gained
    )
    total_boo_comments_gained = eval(
        board_year_record_entity.top_n_total_boo_comments_gained
    )

    return (
        total_articles, total_push_comments_gained, total_boo_comments_gained
    )


@orm.db_session
def get_top_n_total_comments_used_specific_year_info(
    board_name,
    year,
):

    board_entity = models.Board.get(name=board_name)

    if board_entity is None:
        raise exceptions.NoBoardError(board_name)

    board_year_record_entity = models.BoardYearRecord.get(
        year=year,
        board=board_entity
    )

    if not (
        board_year_record_entity
        and board_year_record_entity.update_time > board_entity.update_time
        and board_year_record_entity.top_n_total_push_comments_used
        and board_year_record_entity.top_n_total_boo_comments_used
    ):
        update_time = datetime.datetime.now()

        if board_year_record_entity is None:
            board_year_record_entity = models.BoardYearRecord(
                year=year,
                board=board_entity,
                update_time=update_time,
            )

        total_push_comments_used = defaultdict(int)
        total_boo_comments_used = defaultdict(int)
        year_comments = orm.select(
            comment
            for comment in models.Comment
            if comment.date.year == year
            and comment.article.board.name == board_name
        )
        for comment in year_comments:
            if comment.tag.name == '推':
                total_push_comments_used[comment.user.identifier] += 1
            if comment.tag.name == '噓':
                total_boo_comments_used[comment.user.identifier] += 1

        board_year_record_entity.set(
            top_n_total_push_comments_used=repr(
                total_push_comments_used
            ).replace("<class 'int'>", "int"),
            top_n_total_boo_comments_used=repr(
                total_boo_comments_used
            ).replace("<class 'int'>", "int"),
        )

    total_push_comments_used = eval(
        board_year_record_entity.top_n_total_push_comments_used
    )
    total_boo_comments_used = eval(
        board_year_record_entity.top_n_total_boo_comments_used
    )

    return (total_push_comments_used, total_boo_comments_used)
