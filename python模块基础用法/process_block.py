from multiprocessing import Process
from multiprocessing import Pool

import time


def run_tst(p_num=1):
    time.sleep(1)
    print("这是第{}个进程".format(p_num))


def one_test():
    li = []
    for i in range(5):
        p = Process(target=run_tst, args=(i,))
        p.start()
        li.append(p)
    for i in li:
        i.join()


def two_test():
    p = Pool(5)
    for i in range(5):
        p.apply_async(run_tst, args=(i, ))
    p.close()  # close()之后就不能继续添加新的Process
    p.join()  # 等待所有字子进程执行完毕


if __name__ == '__main__':
    one_test()
    # two_test()
