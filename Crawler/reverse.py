import json
import os

from pymysql import *


def get_data():
    """
    Read data from database

    :return:
    """
    conn = connect(host='127.0.0.1', port=3306, user='root', password='123456', database='wordmap', charset='utf8')
    cs = conn.cursor()
    cs.execute("SELECT word, number FROM map")
    result = cs.fetchall()

    return result


def sort(origin):
    """
    Sort by number

    :param origin:
    :return:
    """
    # Convert tuple into list
    origin = list(origin)
    origin.sort(key=lambda x: x[1])

    return origin


def build_reverse_index(old_index):
    """
    Build reverse index from origin

    :param old_index:
    :return:
    """
    new_index = {}

    # Old data must be sorted
    old_index = sort(old_index)

    # Use the number as index
    index = list(set([x[1] for x in old_index]))
    index.sort()
    print(index)

    i = 0
    number = 0
    words = []
    while i < len(old_index):
        if old_index[i][1] != number:
            # save reverse index
            new_index[number] = words
            # next
            number = old_index[i][1]
            # new a reference; words.clear() is invalid
            words = [old_index[i][0]]
        else:
            # collect words
            words.append(old_index[i][0])
        i += 1

    new_index[number] = words

    # Build reverse index, two loops N²，do not need sort
    # for i in index:
    #     words = []
    #     for data in old_index:
    #         if data[1] == i:
    #             words.append(data[0])
    #     new_index[i] = words

    print(new_index)

    return new_index


def save2file(test_dict):
    """
    Save inverse index in a Json file

    :param test_dict:
    :return:
    """
    json_str = json.dumps(test_dict, indent=4)
    # Get parent dir
    parent = os.path.abspath(os.path.join(os.getcwd(), ".."))
    with open(parent + '/Resources/test_data.json', 'w') as json_file:
        json_file.write(json_str)


'''
if __name__ == '__main__':
    results = get_data()
    print(type(results))
    # results = sort(results)
    print(results)

    new = build_reverse_index(results)
    save2file(new)
'''
