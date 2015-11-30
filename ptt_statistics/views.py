from . import utils


def show_specific_day_info(data):
    pass


def show_specific_month_info(data):
    pass


def show_specific_year_info(data):
    # '''
    print("## 總文章數")
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
    # '''

    # '''
    print("## 發文帳號總數")
    print("共 {:,} 位".format(data['articles']['total_users']))
    print("")
    # '''

    # '''
    print("## 總留言數")
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

    print("## 總留言使用者數")
    print("共 {:,} 位".format(data['comments']['total_users']))
    # '''
