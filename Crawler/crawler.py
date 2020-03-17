"""
    Based on Python 3.7
    @author Yuexiang LI
"""

import threading
import requests
from bs4 import BeautifulSoup
from pymysql import *

import translator

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

    # Request a specific url by using get method, and it will return a Response object
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print("Fail to request word list page!")
        return

    # Obtain text from Response object
    soup = BeautifulSoup(res.text, "lxml")

    # Find the tag, containing the hyperlink for the word, under the div tag named 'main'
    # class 'bs4.element.Tag'
    word_list = soup.find("div", class_="main").find_all("a")
    # Deduplicate
    word_list = list(set(word_list))

    for word in word_list:
        word_url.append({"word": word["title"], "url": word["href"]})
    print(word_url)

    return word_url


def get_phonetic_symbol(phonetic_symbols, word_url):
    """
    Extract phonetic symbols and store them

    :param phonetic_symbols: Store the phonetic symbol
    :param word_url:
    :return:
    """

    # phonetic_symbols = []

    url_prefix = "http://www.phonemicchart.com"

    for w_url in word_url:
        print("----------")
        url = url_prefix + w_url["url"]
        print(url)
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print("Fail to request phonetic symbol page: " + url)
            continue
            # return

        soup = BeautifulSoup(res.text, "lxml")

        # Find the phonetic symbol
        # print(soup)
        symbol = soup.find("span", class_="H4")

        # Some words may not have the phonetic symbol in this website, e.g. anytime
        if symbol:
            symbol = symbol.get_text()

            # Store the phonetic symbol with corresponding word
            phonetic_symbols.append({"word": w_url["word"], "symbol": symbol})
            
            print(symbol)
            # print(translator.covert2digit(translator.extract_consonant(symbol)))

    # return phonetic_symbols



if __name__ == '__main__':
    urls = get_url()
    print(len(urls))

    symbols1 = []
    symbols2 = []
    t1 = threading.Thread(target=get_phonetic_symbol, args=[symbols1, urls[:int(len(urls) / 2)]])
    t2 = threading.Thread(target=get_phonetic_symbol, args=[symbols2, urls[int(len(urls) / 2):]])

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
