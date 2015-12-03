from . import utils


def show_specific_day_info(data):
    pass


def show_specific_month_info(data):
    pass


def show_board_specific_year_info(board):
    print("")
    print("# {} 版 {} 年統計資料".format(
        board['name'],
        board['year'],
    ))
    print("")
    print("資料最後更新時間：{}".format(
        board['update_time'].strftime("%Y-%m-%d %H:%M:%S")
    ))


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

        len_of_n_of_month_articles = utils.get_format_len_of_container(
            data['articles']['months'].values(),
            'num'
        )
        print("|{0:^5}|{1:^{2}}|{3:^8}|".format(
            "月份",
            "文章數",
            len_of_n_of_month_articles + 2,
            "比例",
        ))
        print("|{0:->{1}}|{2:->{3}}|{4:->{5}}|".format(
            ':',
            len("月份") + 5,
            ':',
            len_of_n_of_month_articles + len("文章數") + 2,
            ':',
            len("比例") + 8,
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

        len_of_n_of_comment_tags = utils.get_format_len_of_container(
            data['comments']['tags'].values(),
            'num'
        )
        print("|{0:^4}|{1:^{2}}|{3:^8}|".format(
            "",
            "留言數",
            len_of_n_of_comment_tags + 2,
            "比例"
        ))
        print("|{0:->{1}}|{2:->{3}}|{4:->{5}}|".format(
            ':',
            len("") + 4,
            ':',
            len_of_n_of_comment_tags + len("留言數") + 2,
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

        format_len_of_user_type = utils.get_format_len_of_container(
            data['users']['comment_or_post'].keys(),
            'str'
        )
        format_len_of_n_of_user_type = utils.get_format_len_of_container(
            data['users']['comment_or_post'].values(),
            'num'
        )
        print("|{0:{fill}^{1}}|{2:^{3}}|{4:^8}|".format(
            "類型",
            format_len_of_user_type + 1,
            "人數",
            format_len_of_n_of_user_type + 3,
            "比例",
            fill='　'  # Use fullwidth space for Chinese character
        ))
        print("|{0:->{1}}|{0:->{2}}|{0:->{3}}|".format(
            ':',
            format_len_of_user_type*2 + 2,
            format_len_of_n_of_user_type + len("人數") + 3,
            len("比例") + 8,
        ))
        for user_type, n_of_user_type in sorted(
            data['users']['comment_or_post'].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print("| {0:{fill}<{1}} | {2:>{3},} 位 | ({4:6.2%}) |".format(
                user_type,
                format_len_of_user_type,
                n_of_user_type,
                format_len_of_n_of_user_type,
                n_of_user_type/data['users']['total'],
                fill='　'))  # Use fullwidth space for Chinese character
        print("")

    def show_top_n_data(n=100):
        def show_top_n_data_template(
            show_type=None,
            title=None,
            n=100,
            data_dict=None,
            header_of_rank='名次',
            header_of_user='帳號',
            header_of_value=None,
            count_word_of_value='',
            header_of_percentage='比例',             # total required
            denominator_of_percentage=None,          # total required
            name_of_denominator_of_percentage=None,  # total required
            header_of_numerator=None,    # average required
            header_of_denominator=None,  # average required
            numerator_dict=None,         # average required
            denominator_dict=None,       # average required
            denominator_threshold=None,  # average required
        ):

            print("")
            print("## {} 前 {} 名".format(title, n))
            print("")

            top_n_data = utils.get_n_ranked_data_from_dict(data_dict, n)
            format_len_of_rank = utils.get_format_len_of_container(
                (t.rank for t in top_n_data),
                'num'
            )
            format_len_of_data_of_rank = max(
                len(header_of_rank)*2,
                format_len_of_rank
            )
            format_len_of_user = utils.get_format_len_of_container(
                (t.name for t in top_n_data),
                'str'
            )
            format_len_of_data_of_user = max(
                len(header_of_user)*2,
                format_len_of_user
            )
            format_len_of_value = utils.get_format_len_of_container(
                (t.value for t in top_n_data),
                'num'
            )
            format_len_of_data_of_value = max(
                (len(header_of_value)*2 +
                 len(' (') + len(count_word_of_value)*2 + len(')')),
                format_len_of_value
            )

            if show_type == 'total':
                format_len_of_percentage = 6
                format_len_of_data_of_percentage = max(
                    len(header_of_percentage),
                    format_len_of_percentage
                )

                header = "| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} |"
                print(header.format(
                    header_of_rank,
                    format_len_of_data_of_rank - len(header_of_rank),
                    header_of_user,
                    format_len_of_data_of_user - len(header_of_user),
                    "{} ({})".format(header_of_value, count_word_of_value),
                    (format_len_of_data_of_value
                     - len(header_of_value)
                     - len(count_word_of_value)),
                    header_of_percentage,
                    (format_len_of_data_of_percentage
                     - len(header_of_percentage))
                ))

                separator = "|{0:->{1}}|{0:->{2}}|{0:->{3}}|{0:->{4}}|"
                print(separator.format(
                    ':',
                    len(' ') + format_len_of_data_of_rank + len(' '),
                    len(' ') + format_len_of_data_of_user + len(' '),
                    len(' ') + format_len_of_data_of_value + len(' '),
                    len(' ') + format_len_of_data_of_percentage + len(' ')
                ))

                datum = "| {0:>{1},} | {2:>{3}} | {4:>{5},} | {6:6.2%} |"
                for t in top_n_data:
                    print(datum.format(
                        t.rank,
                        format_len_of_data_of_rank,
                        t.name,
                        format_len_of_data_of_user,
                        t.value,
                        format_len_of_data_of_value,
                        t.value/denominator_of_percentage
                    ))

                sum_of_top_n_data_values = sum(t.value for t in top_n_data)
                print("")
                print("共 {0:>{1},} {2}，佔年度{3} {4:6.2%}".format(
                    sum_of_top_n_data_values,
                    utils.get_format_len_of_num(sum_of_top_n_data_values),
                    count_word_of_value,
                    name_of_denominator_of_percentage,
                    sum_of_top_n_data_values/denominator_of_percentage
                ))
                print("")

                return top_n_data[-1].value

            if show_type == 'average':
                format_len_of_numerator = utils.get_format_len_of_container(
                    (numerator_dict[t.name] for t in top_n_data),
                    'num'
                )
                format_len_of_data_of_numerator = max(
                    len(header_of_numerator)*2,
                    format_len_of_numerator
                )
                format_len_of_denominator = utils.get_format_len_of_container(
                    (denominator_dict[t.name] for t in top_n_data),
                    'num'
                )
                format_len_of_data_of_denominator = max(
                    len(header_of_denominator)*2,
                    format_len_of_denominator
                )

                header = ("| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} |"
                          " {8:^{9}} |")
                print(header.format(
                    header_of_rank,
                    format_len_of_data_of_rank - len(header_of_rank),
                    header_of_user,
                    format_len_of_data_of_user - len(header_of_user),
                    "{} ({})".format(header_of_value, count_word_of_value),
                    (format_len_of_data_of_value
                     - len(header_of_value)
                     - len(count_word_of_value)),
                    header_of_numerator,
                    format_len_of_data_of_numerator - len(header_of_numerator),
                    header_of_denominator,
                    (format_len_of_data_of_denominator
                     - len(header_of_denominator))
                ))

                separator = (
                    "|{0:->{1}}|{0:->{2}}|{0:->{3}}|{0:->{4}}|{0:->{5}}|"
                )
                print(separator.format(
                    ':',
                    len(' ') + format_len_of_data_of_rank + len(' '),
                    len(' ') + format_len_of_data_of_user + len(' '),
                    len(' ') + format_len_of_data_of_value + len(' '),
                    len(' ') + format_len_of_data_of_numerator + len(' '),
                    len(' ') + format_len_of_data_of_denominator + len(' ')
                ))

                datum = (
                    "| {0:>{1},} | {2:>{3}} | {4:>{5},} | {6:>{7},} |"
                    " {8:>{9},} |"
                )
                for t in top_n_data:
                    print(datum.format(
                        t.rank,
                        format_len_of_data_of_rank,
                        t.name,
                        format_len_of_data_of_user,
                        t.value,
                        format_len_of_data_of_value,
                        numerator_dict[t.name],
                        format_len_of_data_of_numerator,
                        denominator_dict[t.name],
                        format_len_of_data_of_denominator,
                    ))

                print("")
                print("僅顯示{}到達 {} 以上的資料".format(
                    header_of_denominator,
                    denominator_threshold,
                ))
                print("")

        def show_top_n_total_articles(n):
            total_articles_threshold = show_top_n_data_template(
                show_type='total',
                title="最多發文數",
                n=n,
                data_dict=data['top_n']['total_articles'],
                header_of_value='發文數',
                count_word_of_value='篇',
                denominator_of_percentage=data['articles']['total'],
                name_of_denominator_of_percentage='總文章數'
            )

            return total_articles_threshold

        def show_top_n_total_push_comments_gained(n):
            show_top_n_data_template(
                show_type='total',
                title="最多「被」推文數",
                n=n,
                data_dict=data['top_n']['total_push_comments_gained'],
                header_of_value='被推文數',
                count_word_of_value='則',
                denominator_of_percentage=data['comments']['total'],
                name_of_denominator_of_percentage='總留言數'
            )

        def show_top_n_total_boo_comments_gained(n):
            show_top_n_data_template(
                show_type='total',
                title="最多「被」噓文數",
                n=n,
                data_dict=data['top_n']['total_boo_comments_gained'],
                header_of_value='被噓文數',
                count_word_of_value='則',
                denominator_of_percentage=data['comments']['total'],
                name_of_denominator_of_percentage='總留言數'
            )

        def show_top_n_total_push_comments_used(n):
            show_top_n_data_template(
                show_type='total',
                title="最多「使用」推文數",
                n=n,
                data_dict=data['top_n']['total_push_comments_used'],
                header_of_value='推文使用量',
                count_word_of_value='則',
                denominator_of_percentage=data['comments']['total'],
                name_of_denominator_of_percentage='總留言數'
            )

        def show_top_n_total_boo_comments_used(n):
            show_top_n_data_template(
                show_type='total',
                title="最多「使用」噓文數",
                n=n,
                data_dict=data['top_n']['total_boo_comments_used'],
                header_of_value='噓文使用量',
                count_word_of_value='則',
                denominator_of_percentage=data['comments']['total'],
                name_of_denominator_of_percentage='總留言數'
            )

        def show_top_n_average_push_comments_gained(
            n,
            total_articles_threshold
        ):
            show_top_n_data_template(
                show_type='average',
                title="最多平均「被」推文數",
                n=n,
                data_dict={
                    user: (
                        round((
                            data['top_n']['total_push_comments_gained'][user]
                            / data['top_n']['total_articles'][user]),
                            2
                        )
                    )
                    for user, total_articles
                    in data['top_n']['total_articles'].items()
                    if total_articles >= total_articles_threshold
                },
                header_of_value='推文比',
                count_word_of_value='則／篇',
                header_of_numerator='被推文數（則）',
                header_of_denominator='總發文數（篇）',
                numerator_dict=data['top_n']['total_push_comments_gained'],
                denominator_dict=data['top_n']['total_articles'],
                denominator_threshold=total_articles_threshold,
            )

        def show_top_n_average_boo_comments_gained(
            n,
            total_articles_threshold
        ):
            show_top_n_data_template(
                show_type='average',
                title="最多平均「被」噓文數",
                n=n,
                data_dict={
                    user: (
                        round((
                            data['top_n']['total_boo_comments_gained'][user]
                            / data['top_n']['total_articles'][user]),
                            2
                        )
                    )
                    for user, total_articles
                    in data['top_n']['total_articles'].items()
                    if total_articles >= total_articles_threshold
                },
                header_of_value='噓文比',
                count_word_of_value='則／篇',
                header_of_numerator='被噓文數（則）',
                header_of_denominator='總發文數（篇）',
                numerator_dict=data['top_n']['total_boo_comments_gained'],
                denominator_dict=data['top_n']['total_articles'],
                denominator_threshold=total_articles_threshold,
            )

        '''
        "average_push_comments_gained": "平均被推文數",
        "average_boo_comments_gained": "平均被噓文數",
        '''

        total_articles_threshold = show_top_n_total_articles(n) - 5
        show_top_n_total_push_comments_gained(n)
        show_top_n_average_push_comments_gained(n, total_articles_threshold)
        show_top_n_total_boo_comments_gained(n)
        show_top_n_average_boo_comments_gained(n, total_articles_threshold)
        show_top_n_total_push_comments_used(n)
        show_top_n_total_boo_comments_used(n)

    show_board_data()
    show_articles_data()
    show_comments_data()
    show_users_data()
    show_top_n_data(n=100)
