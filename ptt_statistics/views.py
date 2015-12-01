from . import utils


def show_specific_day_info(data):
    pass


def show_specific_month_info(data):
    pass


def show_specific_year_info(data):
    def show_board_data():
        print("")
        print("# {0}版 {1}年統計資料 （最後更新時間：{2}）".format(
            data['board']['name'],
            data['board']['year'],
            data['board']['update_time'].strftime("%Y-%m-%d %H:%M:%S"))
        )
    def show_articles_data():
        print("")
        print("## 總文章數")
        print("")
        print("共 {:,} 篇".format(data['articles']['total']))
        print("")

        len_of_month_articles = max(map(utils.get_format_len_of_num,
                                        data['articles']['months'].values()))
        for month in sorted(data['articles']['months']):
            n_of_month_articles = data['articles']['months'][month]
            print("+ {0:>2} 月: {1:>{2},} 篇 ({3:6.2%})".format(
                month,
                n_of_month_articles,
                len_of_month_articles,
                n_of_month_articles/data['articles']['total']))
        print("")

        print("")
        print("## 發文帳號總數（未重複）")
        print("")
        print("共 {:,} 位".format(data['articles']['total_users']))
        print("")


    def show_comments_data():
        print("")
        print("## 總留言數")
        print("")
        print("共 {:,} 則".format(data['comments']['total']))
        print("")

        len_of_coment_tags = max(map(utils.get_format_len_of_num,
                                     data['comments']['tags'].values()))
        for comment_tag in sorted(data['comments']['tags']):
            n_of_comment_tags = data['comments']['tags'][comment_tag]
            print("+ {0}: {1:>{2},} 則 ({3:6.2%})".format(
                comment_tag,
                n_of_comment_tags,
                len_of_coment_tags,
                n_of_comment_tags/data['comments']['total']))
        print("")

        print("")
        print("## 留言帳號總數（未重複）")
        print("")
        print("共 {:,} 位".format(data['comments']['total_users']))
        print("")


    def show_users_data():
        print("")
        print("## 有發文或留言的帳號總數（未重複）")
        print("")
        print("共 {:,} 位".format(data['users']['total']))
        print("")

        len_of_user_type = max(map(utils.get_format_len_of_num,
                                   data['users']['comment_or_post'].keys()))
        len_of_n_of_user_type = max(map(utils.get_format_len_of_num,
                                        data['users']['comment_or_post'].values()))
        for user_type in sorted(data['users']['comment_or_post']):
            n_of_user_type = data['users']['comment_or_post'][user_type]
            print("+ {0:{fill}<{1}}: {2:>{3},} 位 ({4:6.2%})".format(
                user_type,
                len_of_user_type,
                n_of_user_type,
                len_of_n_of_user_type,
                n_of_user_type/data['users']['total'],
                fill='　'))  # Use fullwidth space for Chinese character
        print("")


    show_board_data()
    show_articles_data()
    show_comments_data()
    show_users_data()
