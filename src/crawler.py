"""
    Based on Python 3.7
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/65.0.3325.146 Safari/537.36 "
}


def get_url():
    """
    Reference: https://www.jianshu.com/p/f8516eb9913f

    :return:
    """

    word_url = []

    url = "http://www.phonemicchart.com/transcribe/1000_basic_words.html"

    # 利用requests对象的get方法，对指定的url发起请求
    # 该方法会返回一个Response对象
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print("Fail to request word list page!")
        return

    # 通过Response对象的text方法获取网页的文本信息
    soup = BeautifulSoup(res.text, "lxml")

    # 找出名为main的div标签下的所有单词的超链接标签
    word_list = soup.find("div", class_="main").find_all("a")

    for word in word_list:
        word_url.append({"word": word["title"], "url": word["href"]})
    print(word_url)

    """
    for t in table:
        word_list = t.find_all("a")
        print(word_list)

        for word in word_list:
            print(word)
            print(word["href"])
            print(word["title"])
            word_url.append({"word": word["title"], "url": word["href"]})
    print(word_url)
    """
    # for t in table:
    #     print("________________")
    #     print(t)
    #     word_list = t.find("td").find_all("p")
    #     print(word_list)
    #     word_list.pop(0)
    #     print(word_list)
    #
    #     word = []
    #     for w in word_list:
    #         print(w)
    #         word = w.find_all("a")
    #         print(word)
    #     print(word)
    #
    #     for w in word:
    #         print(w)
    #         # 获取属性
    #         print(w["href"])
    #         print(w["title"])
    #         word_url.append({"word": w["title"], "url": w["href"]})
    #
    # print(word_url)

    return word_url


def get_phonemic_symbol(word_url):
    """

    :param word_url:
    :return:
    """

    phonemic_symbols = []

    url_prefix = "http://www.phonemicchart.com"

    for w_url in word_url:
        print("----------")
        url = url_prefix + w_url["url"]
        print(url)
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print("Fail to request phonemic symbol page!")
            return

        soup = BeautifulSoup(res.text, "lxml")

        # 获取音标
        # print(soup)
        symbol = soup.find("span", class_="H4")

        # anytime没有音标
        if symbol:
            symbol = symbol.get_text()

            print(symbol)
            # 把单词和对应的音标存起来
            phonemic_symbols.append({"word": w_url["word"], "symbol": symbol})

    return phonemic_symbols


if __name__ == '__main__':
    urls = get_url()
    print(len(urls))
    symbols = get_phonemic_symbol(urls)
    print(symbols)
    print(len(symbols))
