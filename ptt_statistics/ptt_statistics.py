import argparse
import datetime
import sys
import time

import ptt_crawler


def get_args():
    p = argparse.ArgumentParser(prog='ptt-statistics')

    p.add_argument('board')
    p.add_argument('--from-year', nargs='?')
    p.add_argument('--to-year', nargs='?')

    args = p.parse_args()

    if args.from_year:      # from xxxx/01/01 00:00:00
        args.from_year = datetime.datetime(args.from_year, 1, 1,
                                           0, 0, 0)
    else:
        args.from_year = datetime.datetime(datetime.date.today().year, 1, 1,
                                           0, 0, 0)

    if args.to_year:      # to xxxx/12/31 23:59:59
        args.to_year = datetime.datetime(args.to_year, 12, 31,
                                         23, 59, 59)
    else:
        args.to_year = datetime.datetime(datetime.date.today().year, 12, 31,
                                         23, 59, 59)

    return args


def main():
    args = get_args()
    board = ptt_crawler.Board(args.board, verify=False)
    print(board)

    for i, article in enumerate(board.articles()):
        print(article.content)

        for comment in article.comments:
            print(comment)

        time.sleep(1)


if __name__ == "__main__":
    status = main()
    sys.exit(status)
