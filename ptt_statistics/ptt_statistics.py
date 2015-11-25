import argparse
import datetime
import sys
import traceback

import ptt_crawler
import requests

from . import constants
from . import controllers
from . import models
from . import utils
from . import views


def get_args():
    p = argparse.ArgumentParser(prog='ptt-statistics')
    sub_p = p.add_subparsers(title='subcommands',
                             help="use ${sub-command} -h for further usage")

    # subcommand: crawl
    p_board = sub_p.add_parser('crawl',
                               help="Crawl the specific board")
    p_board.add_argument('board_name',
                         type=str,
                         help="The name of the board")
    p_board.add_argument('--from-year',
                         nargs='?',
                         type=int,
                         default=datetime.MINYEAR,
                         help="default: {}".format(datetime.MINYEAR))
    p_board.add_argument('--to-year',
                         nargs='?',
                         type=int,
                         default=datetime.date.today().year,
                         help="default: {}".format(datetime.date.today().year))

    # subcommand: get_article
    p_path = sub_p.add_parser('get_article',
                              help="Get specific article info with path")
    p_path.add_argument('article_path',
                        type=str,
                        help=("The path of the article on www.ptt.cc"
                              "In this format: '/bbs/${board}/${id}.html' "))

    # subcommand: show
    p_show = sub_p.add_parser('show',
                              help="Show info of the board via data in db")
    p_show.add_argument('board_to_show',
                        type=str,
                        help="The name of the board to show")
    p_show.add_argument('date',
                        type=str,
                        help=("Info about which year of the board to show "
                              "format: YYYY or YYYY.MM or YYYY.MM.DD"))

    args = p.parse_args()
    return args


def store_board_info(board_name):
    # TODO: [#5] from_year and to_year selection
    board = ptt_crawler.Board(board_name, verify=True)
    articles = board.articles()

    try:
        article = articles.next()
    except:
        return
    else:
        models.db.bind('sqlite', constants.db_path, create_db=True)
        models.db.generate_mapping(create_tables=True, check_tables=True)

        controllers.store_board(board)

        while True:
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
                continue


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
    except ValueError:
        traceback.print_exc()
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
        data = controllers.get_specific_year_info(board_name,
                                                  year=year)
        views.show_specific_year_info(data)


def main():
    args = get_args()
    utils.create_dir_if_not_exists()

    if hasattr(args, 'board_name'):
        store_board_info(args.board_name)
    if hasattr(args, 'article_path'):
        store_article_info(args.article_path)
    if hasattr(args, 'board_to_show') and hasattr(args, 'date'):
        date_list = list(map(int, filter(bool, args.date.split('.'))))
        date_list += [None]*(3-len(date_list))
        show_board_info(args.board_to_show, tuple(date_list))


if __name__ == "__main__":
    status = main()
    sys.exit(status)
