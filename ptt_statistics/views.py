from . import utils


def show_specific_day_info(data):
    pass


def show_specific_month_info(data):
    pass


def show_specific_year_info(data):
    def show_board_data():
        print("")
        print("# {} 版 {} 年統計資料".format(
            data['board']['name'],
            data['board']['year'],
        ))
        print("")
        print("資料最後更新時間：{}".format(
            data['board']['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        ))

    def show_articles_data():
        print("")
        print("## 總文章數")
        print("")
        print("共 {:,} 篇".format(data['articles']['total']))
        print("")

        len_of_n_of_month_articles = max(
            map(
                utils.get_format_len_of_num,
                data['articles']['months'].values()
            )
        )
        print("|{0:^5}|{1:^{2}}|{3:^8}|".format(
            "月份",
            "文章數",
            len_of_n_of_month_articles+2,
            "比例",
        ))
        print("|{0:->{1}}|{2:->{3}}|{4:->{5}}|".format(
            ':',
            len("月份")+5,
            ':',
            len_of_n_of_month_articles+len("文章數")+2,
            ':',
            len("比例")+8,
        ))
        for month in sorted(data['articles']['months']):
            n_of_month_articles = data['articles']['months'][month]
            print("| {0:>2} 月 | {1:>{2},} 篇 | ({3:6.2%}) |".format(
                month,
                n_of_month_articles,
                len_of_n_of_month_articles,
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

        len_of_n_of_comment_tags = max(
            map(
                utils.get_format_len_of_num,
                data['comments']['tags'].values()
            )
        )
        print("|{0:^4}|{1:^{2}}|{3:^8}|".format(
            "",
            "留言數",
            len_of_n_of_comment_tags+2,
            "比例"
        ))
        print("|{0:->{1}}|{2:->{3}}|{4:->{5}}|".format(
            ':',
            len("")+4,
            ':',
            len_of_n_of_comment_tags+len("留言數")+2,
            ':',
            len("比例")+8,
        ))
        for comment_tag, n_of_comment_tags in sorted(
            data['comments']['tags'].items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            print("| {0} | {1:>{2},} 則 | ({3:6.2%}) |".format(
                comment_tag,
                n_of_comment_tags,
                len_of_n_of_comment_tags,
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

        len_of_user_type = max(
            map(
                utils.get_format_len_of_str,
                data['users']['comment_or_post'].keys()
            )
        )
        len_of_n_of_user_type = max(
            map(
                utils.get_format_len_of_num,
                data['users']['comment_or_post'].values()
            )
        )
        print("|{0:{fill}^{1}}|{2:^{3}}|{4:^8}|".format(
            "類型",
            len_of_user_type+1,
            "人數",
            len_of_n_of_user_type+3,
            "比例",
            fill='　'  # Use fullwidth space for Chinese character
        ))
        print("|{0:->{1}}|{2:->{3}}|{4:->{5}}|".format(
            ':',
            len_of_user_type*2+2,
            ':',
            len_of_n_of_user_type+len("人數")+3,
            ':',
            len("比例")+8,
        ))
        for user_type, n_of_user_type in sorted(
            data['users']['comment_or_post'].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print("| {0:{fill}<{1}} | {2:>{3},} 位 | ({4:6.2%}) |".format(
                user_type,
                len_of_user_type,
                n_of_user_type,
                len_of_n_of_user_type,
                n_of_user_type/data['users']['total'],
                fill='　'))  # Use fullwidth space for Chinese character
        print("")

    def show_top_n_data(n=100):
        def show_top_n_total_articles(n):
            print("")
            print("## 最多發文數 前 {} 名".format(n))
            print("")

            top_n_data = utils.get_n_ranked_data_from_dict(
                data['top_n']['total_articles'],
                n
            )
            len_of_rank = max(
                map(
                    utils.get_format_len_of_num,
                    (t.rank for t in top_n_data)
                )
            )
            len_of_user = max(
                map(
                    utils.get_format_len_of_str,
                    (t.name for t in top_n_data)
                )
            )
            len_of_n_of_articles = max(
                map(
                    utils.get_format_len_of_num,
                    (t.value for t in top_n_data)
                )
            )
            s = "|{0:^{1}}|{2:^{3}}|{4:^{5}}|{6:^8}|"
            print(s.format(
                "名次",
                len_of_rank+2,
                "帳號",
                len_of_user,
                "文章數",
                len_of_n_of_articles+2,
                "比例"
            ))
            s = "|{0:->{1}}|{2:->{3}}|{4:->{5}}|{6:->{7}}|"
            print(s.format(
                ':',
                len_of_rank+len("名次")+2,
                ':',
                len_of_user+len("帳號"),
                ':',
                len_of_n_of_articles+len("文章數")+2,
                ':',
                len("比例")+8
            ))
            s = "| {0:>{1},} | {2:>{3}} | {4:>{5},} 篇 | ({6:6.2%}) |"
            for t in top_n_data:
                print(s.format(
                    t.rank,
                    len_of_rank+2,
                    t.name,
                    len_of_user,
                    t.value,
                    len_of_n_of_articles,
                    t.value/data['articles']['total']
                ))

            sum_of_top_n_data_values = sum(t.value for t in top_n_data)
            print("")
            print("共 {0:>{1},} 篇，佔年度發文數 {2:6.2%}".format(
                sum_of_top_n_data_values,
                utils.get_format_len_of_num(sum_of_top_n_data_values),
                sum_of_top_n_data_values/data['articles']['total']
            ))
            print("")

        def show_top_n_total_push_comments_gained(n):
            print("")
            print("## 最多「被」推文數 前 {} 名".format(n))
            print("")

            top_n_data = utils.get_n_ranked_data_from_dict(
                data['top_n']['total_push_comments_gained'],
                n
            )
            len_of_rank = max(
                map(
                    utils.get_format_len_of_num,
                    (t.rank for t in top_n_data)
                )
            )
            len_of_user = max(
                map(
                    utils.get_format_len_of_str,
                    (t.name for t in top_n_data)
                )
            )
            len_of_n_of_push_comments_gained = max(
                map(
                    utils.get_format_len_of_num,
                    (t.value for t in top_n_data)
                )
            )
            s = "|{0:^{1}}|{2:^{3}}|{4:^{5}}|{6:^8}|"
            print(s.format(
                "名次",
                len_of_rank+2,
                "帳號",
                len_of_user,
                "被推文數",
                len_of_n_of_push_comments_gained+1,
                "比例"
            ))
            s = "|{0:->{1}}|{2:->{3}}|{4:->{5}}|{6:->{7}}|"
            print(s.format(
                ':',
                len_of_rank+len("名次")+2,
                ':',
                len_of_user+len("帳號"),
                ':',
                len_of_n_of_push_comments_gained+len("被推文數")+1,
                ':',
                len("比例")+8
            ))
            s = "| {0:>{1},} | {2:>{3}} | {4:>{5},} 則 | ({6:6.2%}) |"
            for t in top_n_data:
                print(s.format(
                    t.rank,
                    len_of_rank+2,
                    t.name,
                    len_of_user,
                    t.value,
                    len_of_n_of_push_comments_gained,
                    t.value/data['comments']['total']
                ))

            sum_of_top_n_data_values = sum(t.value for t in top_n_data)
            print("")
            print("共 {0:>{1},} 則，佔年度留言數 {2:6.2%}".format(
                sum_of_top_n_data_values,
                utils.get_format_len_of_num(sum_of_top_n_data_values),
                sum_of_top_n_data_values/data['comments']['total']
            ))
            print("")

        '''
        "total_push_comments_gained": "最多「被」推文",
        "average_push_comments_gained": "平均被推文數",
        "total_boo_comments_gained": "最多「被」噓文",
        "average_boo_comments_gained": "平均被噓文數",
        "total_push_comments_used": "最多「使用」推文",
        "total_boo_comments_used": "最多「使用」噓文",
        '''

        show_top_n_total_articles(n)
        show_top_n_total_push_comments_gained(n)

    show_board_data()
    show_articles_data()
    show_comments_data()
    show_users_data()
    show_top_n_data(n=100)
