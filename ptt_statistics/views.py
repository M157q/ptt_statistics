from . import utils


def show_specific_day_info(data):
    pass


def show_specific_month_info(data):
    pass


def show_specific_year_info(data):
    # Articles
    print("")
    print("## 總文章數")
    print("")
    print("共 {:,} 篇".format(data['articles']['total']))
    print("")

    len_of_month_articles = max(map(utils.get_format_len_of_num,
                                    data['articles']['months'].values()))
    for month, n_of_month_articles in data['articles']['months'].items():
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

    # Comments
    print("")
    print("## 總留言數")
    print("")
    print("共 {:,} 則".format(data['comments']['total']))
    print("")

    len_of_coment_tags = max(map(utils.get_format_len_of_num,
                                 data['comments']['tags'].values()))
    for comment_tag, n_of_comment_tags in data['comments']['tags'].items():
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

    # Users
    print("")
    print("## 有發文或留言的帳號總數（未重複）")
    print("")
    print("共 {:,} 位".format(data['users']['total']))
    print("")

    len_of_user_type = max(map(utils.get_format_len_of_num,
                               data['users']['comment_or_post'].keys()))
    len_of_n_of_user_type = max(map(utils.get_format_len_of_num,
                                    data['users']['comment_or_post'].values()))
    for user_type, n_of_user_type in data['users']['comment_or_post'].items():
        print("+ {0:{fill}<{1}}: {2:>{3},} 位 ({4:6.2%})".format(
            user_type,
            len_of_user_type,
            n_of_user_type,
            len_of_n_of_user_type,
            n_of_user_type/data['users']['total'],
            fill='　'))  # Use fullwidth space for Chinese character
    print("")
