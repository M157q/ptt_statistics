import argparse
import datetime
import sys
import time

import ptt_crawler


def get_args():
    p = argparse.ArgumentParser(prog='ptt-statistics')

    p.add_argument('board')
    p.add_argument('--from-year', nargs='?', type=int,
                   default=datetime.date.today().year,
                   description="(default: current year)")
    p.add_argument('--to-year', nargs='?', type=int,
                   default=datetime.date.today().year,
                   description="(default: current year)")

    args = p.parse_args()

    # from xxxx/01/01 00:00:00
    args.from_year = datetime.datetime(args.from_year, 1, 1, 0, 0, 0)
    # to xxxx/12/31 23:59:59
    args.to_year = datetime.datetime(args.to_year, 12, 31, 23, 59, 59)

    return args


def main():
    args = get_args()
    board = ptt_crawler.Board(args.board, verify=True)

    print(board.cookies['over18'])
    print(board.name)
    while True:
        try:
            article = board.articles().__next__()
        except:
            continue
        else:
            print(article.id)
            # print(article.url)
            # print(article.author)
            # print(article.reply)
            # print(article.type)
            # print(article.title)
            # print(article.time)
            # print(article.content)
            # print(article.comments)
            break

        time.sleep(1)


if __name__ == "__main__":
    status = main()
    sys.exit(status)
