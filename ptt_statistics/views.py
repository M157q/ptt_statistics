def show_specific_day_info(data):
    pass


def show_specific_month_info(data):
    pass


def show_specific_year_info(data):
    print("## 總文章數")
    print("扣除掉已經刪除的文章，共 {:,} 篇".format(data['articles']['total']))
    print("")

    for month, n_of_month_articles in data['articles']['months'].items():
        print("+ {} 月: {:,} 篇".format(month, n_of_month_articles))
    print("")

    print("## 總發文人數")
    print("ID 不重複狀況下，共 {:,} 人".format(data['authors']['total']))
    print("")

    print("## 總留言數")
    print("共 {:,} 則".format(data['comments']['total']))
    print("")
    for comment_tag, n_of_comment_tag in data['comments']['tags'].items():
        print("+ {}: {:,} 則".format(comment_tag, n_of_comment_tag))
