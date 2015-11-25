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


def get_args():
    p = argparse.ArgumentParser(prog='ptt-statistics')
    sub_p = p.add_subparsers(title='subcommands',
                             help="use ${sub-command} -h for further usage")

    # subcommand: board
    p_board = sub_p.add_parser('board',
                               help="Craw the specific board")
    p_board.add_argument('board_name', help="The name of the board")
    p_board.add_argument('--from-year', nargs='?', type=int,
                         default=datetime.MINYEAR,
                         help="default: {}".format(datetime.MINYEAR))
    p_board.add_argument('--to-year', nargs='?', type=int,
                         default=datetime.date.today().year,
                         help="default: {}".format(datetime.date.today().year))

    # subcommand: path
    p_path = sub_p.add_parser('path',
                              help="Get specific article info with path")
    p_path.add_argument('article_path',
                        help=("The path of the article on www.ptt.cc"
                              "\n"
                              "In this format: '/bbs/${board}/${id}.html' "))

    # subcommand: show
    p_show = sub_p.add_parser('show',
                              help="Show info of the board via data in db")
    p_show.add_argument('board_to_show',
                        help="The name of the board for showing its info")
    p_show.add_argument('show_type',
                        help="The type for showing the board info")

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


def main():
    args = get_args()
    utils.create_dir_if_not_exists()

    if hasattr(args, 'board_name'):
        store_board_info(args.board_name)
    if hasattr(args, 'article_path'):
        store_article_info(args.article_path)


if __name__ == "__main__":
    status = main()
    sys.exit(status)
