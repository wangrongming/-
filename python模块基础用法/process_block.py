from multiprocessing import Process, dummy
from multiprocessing import Pool

import time


def run_tst(p_num=1):
    time.sleep(1)
    print("这是第{}个进程".format(p_num))


class OneName:

    def __init__(self, name):
        self.name = name

    def one_one_two(self):
        for i in range(100):
            time.sleep(1)
            print("我被运行 {}".format(self.name))

class TwoName:

    def __init__(self, name):
        self.name = name

    def one_one_two(self):
        for i in range(100):
            time.sleep(1)
            print("我被运行 {}".format(self.name))


def one_test():
    info1 = OneName(name="ceshi1")
    info2 = TwoName(name="ceshi2")
    li = []
    for i in range(1):
        p1 = Process(target=info1.one_one_two())
        p2 = Process(target=info2.one_one_two())
        p1.start()
        p2.start()
        p1.join()
        p2.join()


def two_test():
    info1 = OneName(name="ceshi1")
    info2 = TwoName(name="ceshi2")
    p = Pool(2)
    p.apply_async(info2.one_one_two())
    p.apply_async(info1.one_one_two())
    p.close()  # close()之后就不能继续添加新的Process
    p.join()  # 等待所有字子进程执行完毕


def three_test(self):
    pool = dummy.Pool(6)
    pool.map(self.run, range(1, 7))
    pool.close()
    pool.join()


from multiprocessing import Pool
import time


def func1():
    for i in range(10):
        time.sleep(1)
        print('running func%s' % 1)


def func2():
    for i in range(10):
        time.sleep(1)
        print('running func%s' % 2)


if __name__ == '__main__':
    p = Pool()
    p.apply_async(func1) #apply为同步执行任务, apply_async异步执行任务
    p.apply_async(func2) #apply为同步执行任务, apply_async异步执行任务
    p.close() #必须先要close
    p.join() #感知进程池中的任务执行结束

# if __name__ == '__main__':
#     two_test()
