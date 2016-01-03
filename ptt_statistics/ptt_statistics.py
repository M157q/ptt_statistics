import argparse
import datetime
import sys
import traceback

import ptt_crawler
import requests

from . import constants
from . import controllers
from . import exceptions
from . import models
from . import utils
from . import views


def get_args():
    p = argparse.ArgumentParser(prog='ptt-statistics')
    sub_p = p.add_subparsers(
        title='subcommands',
        help="use ${sub-command} -h for further usage",
    )

    # subcommand: crawl
    p_crawl = sub_p.add_parser(
        'crawl',
        help="Crawl the specific board",
    )
    p_crawl.add_argument(
        'board_name',
        type=str,
        help="The name of the board",
    )
    p_crawl.add_argument(
        '--from-year',
        nargs='?',
        type=int,
        default=datetime.MINYEAR,
        help="default: {}".format(datetime.MINYEAR),
    )
    p_crawl.add_argument(
        '--to-year',
        nargs='?',
        type=int,
        default=datetime.date.today().year,
        help="default: {}".format(datetime.date.today().year),
    )

    # subcommand: get_article
    p_get_article = sub_p.add_parser(
        'get_article',
        help="Get specific article info with path",
    )
    p_get_article.add_argument(
        'article_path',
        type=str,
        help=(
            "The path of the article on www.ptt.cc "
            "in this format: '/bbs/${board}/${id}.html'"
        ),
    )

    # subcommand: show
    p_show = sub_p.add_parser(
        'show',
        help="Show info of the board via data in db",
    )
    p_show.add_argument(
        'board_to_show',
        type=str,
        help="The name of the board to show",
    )
    p_show.add_argument(
        'date',
        type=str,
        help=(
            "Info about which year of the board to show "
            "format: YYYY or YYYY.MM or YYYY.MM.DD"
        ),
    )

    args = p.parse_args()
    return args


def store_board_info(board_name, from_year, to_year):
    board = ptt_crawler.Board(board_name, verify=True)
    articles = board.articles()

    try:
        article = articles.next()
    except:
        print("No article in board '{}'.".format(board_name))
        print("Make sure you've entered the correct name.")
        return

    controllers.store_board(board)

    while True:
        if article:
            try:
                article_year = article.time.date().year
            except:
                pass
            else:
                if article_year < from_year:
                    print("Articles from {} to {} stored.".format(
                        from_year, to_year
                    ))
                    break

                if from_year <= article_year <= to_year:
                    controllers.store_article(article, board)
                    for comment in article.comments:
                        controllers.store_comment(comment, article, board)

        try:
            article = articles.next()
        except StopIteration:
            print("No next article.")
            break
        except requests.exceptions.ConnectionError:
            traceback.print_exc()
            print("ConnectionError happened.")
            break
        except:
            traceback.print_exc()
            article = None


def store_article_info(article_path):
    board = ptt_crawler.Board()
    try:
        page = board.get_data(article_path)
    except:
        print("Unknown Page. Use this format: /bbs/${board}/${id}.html")
    else:
        # TODO: [#2] get the content of article and store it to db
        print(board.get_url(article_path))
        print(page, type(page))


def show_board_info(board_name, date_tuple):
    try:
        year, month, day = utils.check_date_tuple(date_tuple)
    except ValueError as e:
        print(e)
        exit()

    if year and month and day:
        data = controllers.get_specific_day_info(board_name,
                                                 year=year,
                                                 month=month,
                                                 day=day)
        views.show_specific_day_info(data)
    elif year and month:
        data = controllers.get_specific_month_info(board_name,
                                                   year=year,
                                                   month=month)
        views.show_specific_month_info(data)
    elif year:
        try:
            views.show_board_specific_year_info(board_name, year)
        except exceptions.NoBoardError:
            sys.exit(
                ("Board: {} not found in database."
                 "\n"
                 "Please crawl the board first.")
                .format(board_name)
            )
        else:
            articles_total, articles_total_users = \
                views.show_articles_specific_year_info(
                    board_name,
                    year
                )

            comments_total, comments_total_users = \
                views.show_comments_specific_year_info(
                    board_name,
                    year
                )

            views.show_users_specific_year_info(
                board_name,
                year,
                articles_total_users,
                comments_total_users
            )

            views.show_top_n_specific_year_info(
                board_name,
                year,
                articles_total,
                comments_total,
                n=100,
            )


def main():
    args = get_args()
    utils.create_dir_if_not_exists()
    models.db.bind('sqlite', constants.db_path, create_db=True)
    models.db.generate_mapping(create_tables=True, check_tables=True)

    if hasattr(args, 'board_name'):
        store_board_info(args.board_name, args.from_year, args.to_year)
    if hasattr(args, 'article_path'):
        store_article_info(args.article_path)
    if hasattr(args, 'board_to_show') and hasattr(args, 'date'):
        try:
            date_list = list(map(int, filter(bool, args.date.split('.'))))
        except ValueError:
            print("Use this format for date: YYYY or YYYY.MM or YYYY.MM.DD")
        else:
            date_list += [None]*(3-len(date_list))
            show_board_info(args.board_to_show, tuple(date_list))


if __name__ == "__main__":
    status = main()
    sys.exit(status)
