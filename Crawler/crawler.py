"""
    Based on Python 3.7
    @author Yuexiang LI
"""

import threading
import requests
from bs4 import BeautifulSoup
from pymysql import *

from Crawler import translator

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/65.0.3325.146 Safari/537.36 "
}


def get_url():
    """
    Get each word's url
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
    # class 'bs4.element.Tag'
    word_list = soup.find("div", class_="main").find_all("a")
    # Deduplicate
    word_list = list(set(word_list))

    for word in word_list:
        word_url.append({"word": word["title"], "url": word["href"]})
    print(word_url)

    return word_url


def get_phonemic_symbol(phonemic_symbols, word_url):
    """

    :param word_url:
    :return:
    """

    # phonemic_symbols = []

    url_prefix = "http://www.phonemicchart.com"

    for w_url in word_url:
        print("----------")
        url = url_prefix + w_url["url"]
        print(url)
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print("Fail to request phonemic symbol page: " + url)
            # return

        soup = BeautifulSoup(res.text, "lxml")

        # 获取音标
        # print(soup)
        symbol = soup.find("span", class_="H4")

        # anytime没有音标
        if symbol:
            symbol = symbol.get_text()

            print(symbol)
            print(translator.covert2digit(translator.extract_consonant(symbol)))
            # 把单词和对应的音标存起来
            phonemic_symbols.append({"word": w_url["word"], "symbol": symbol})

    # return phonemic_symbols


'''
if __name__ == '__main__':
    urls = get_url()
    print(len(urls))

    symbols1 = []
    symbols2 = []
    t1 = threading.Thread(target=get_phonemic_symbol, args=[symbols1, urls[:int(len(urls) / 2)]])
    t2 = threading.Thread(target=get_phonemic_symbol, args=[symbols2, urls[int(len(urls) / 2):]])

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    symbols = symbols1 + symbols2
    print(len(symbols))

    conn = connect(host='127.0.0.1', port=3306, user='root', password='123456', database='wordmap', charset='utf8')
    cs = conn.cursor()  # 获取游标

    values = []

    for s in symbols:
        print(s["word"])
        print(s["symbol"])
        consonant = translator.extract_consonant(s["symbol"])
        digit = translator.covert2digit(consonant)
        if digit != "":
            values.append((s["word"], s["symbol"], digit))

    try:
        # https://blog.csdn.net/Homewm/article/details/81703218
        cs.executemany("REPLACE INTO map(word, phonemic_symbol, number) VALUES(%s, %s, %s)", values)
        conn.commit()  # 提交
    except Exception as err:
        print(err)

    cs.close()
    conn.close()
    print('OK')
'''
