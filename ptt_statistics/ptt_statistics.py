import argparse
import datetime
import sys
import traceback

import ptt_crawler

from . import models
from . import controllers


def get_args():
    p = argparse.ArgumentParser(prog='ptt-statistics')
    sub_p = p.add_subparsers(title='subcommands',
                             help="use ${sub-command} -h for further usage")

    p_board = sub_p.add_parser('board',
                               help="Craw the specific board")
    p_board.add_argument('board_name', help="The name of the board")
    p_board.add_argument('--from-year', nargs='?', type=int,
                         default=datetime.MINYEAR,
                         help="default: {}".format(datetime.MINYEAR))
    p_board.add_argument('--to-year', nargs='?', type=int,
                         default=datetime.date.today().year,
                         help="default: {}".format(datetime.date.today().year))

    p_path = sub_p.add_parser('path',
                              help="Get specific article info with path")
    p_path.add_argument('article_path',
                        help="The path of the article on www.ptt.cc")

    args = p.parse_args()
    return args


def main():
    args = get_args()

    if hasattr(args, 'board_name'):
        board = ptt_crawler.Board(args.board_name, verify=True)
        articles = board.articles()

        try:
            article = articles.__next__()
        except:
            return
        else:
            models.db.bind('sqlite', '../ptt_statistics.db', create_db=True)
            models.db.generate_mapping(create_tables=True, check_tables=True)

            controllers.db_board(board)

            while True:
                controllers.db_article(article, board)

                for comment in article.comments:
                    controllers.db_comment(comment, article, board)

                try:
                    article = articles.next()
                except StopIteration:
                    print("No next article.")
                    break
                except:
                    traceback.print_exc()
                    break

    if hasattr(args, 'article_path'):
        board = ptt_crawler.Board()
        try:
            page = board.get_data(args.article_path)
        except:
            print("Unknown Page. Use this format: /bbs/${board}/${id}.html")
        else:
            # TODO: get the content of article and store it to db
            print(board.get_url(args.article_path))
            print(page, type(page))


if __name__ == "__main__":
    status = main()
    sys.exit(status)
