import threading
import time
import logging

def test1(list, target):
    for i in range(0, 100):
        list[0] += 1
        logging.warning(str(target) + " : " + str(list))
        # print()
        # time.sleep(1)
    # for i in range(1, 10000):
    #     logging.warning(target)


def test2(list, target):
    for i in range(0, 100):
        list[0] += 1
        logging.warning(str(target) + " : " + str(list))
        # print()
        # time.sleep(1)
    # for i in range(1, 10000):
    #     logging.warning(target)

if __name__ == '__main__':
    list = [0]

    t1 = threading.Thread(target=test1, args=(list, 1))
    t2 = threading.Thread(target=test2, args=(list, 2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


    # print(list)