"""
    Based on Python 3.7
    @author Yuexiang LI
"""

import threading
from pymysql import *
import translator
import crawler
import reverse

if __name__ == '__main__':
    # Get each word's url
    urls = crawler.get_url()
    print(len(urls))

    symbols1 = []
    symbols2 = []
    # Get phonetic symbols from urls
    t1 = threading.Thread(target=crawler.get_phonetic_symbol, args=[symbols1, urls[:int(len(urls) / 2)]])
    t2 = threading.Thread(target=crawler.get_phonetic_symbol, args=[symbols2, urls[int(len(urls) / 2):]])

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    symbols = symbols1 + symbols2
    print(len(symbols))

    conn = connect(host='127.0.0.1', port=3306, user='root', password='123456', database='wordmap', charset='utf8')
    cs = conn.cursor()  # Get the database cursor

    values = []

    for s in symbols:
        print(s["word"])
        print(s["symbol"])
        # Extract consonant from phonetic symbol
        consonant = translator.extract_consonant(s["symbol"])
        # Convert consonant into digit
        digit = translator.covert2digit(consonant)
        if digit != "":
            values.append((s["word"], s["symbol"], digit))

    try:
        # https://blog.csdn.net/Homewm/article/details/81703218
        # cs.executemany("INSERT IGNORE INTO map(word, phonemic_symbol, number) VALUES(%s, %s, %s)", values)
        cs.executemany("REPLACE INTO map(word, phonemic_symbol, number) VALUES(%s, %s, %s)", values)
        conn.commit()  # Execute SQL to save items
    except Exception as err:
        print(err)

    cs.close()
    conn.close()
    print('OK')

    # Get data from database
    results = reverse.get_data()
    # results = reverse.sort(results)
    print(results)
    # Build reverse index
    new = reverse.build_reverse_index(results)
    # Save as Json File
    reverse.save2file(new)
