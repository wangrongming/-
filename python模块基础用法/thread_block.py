import threading


def thread_test(i):
    print("当前是线程{}".format(i))


if __name__ == '__main__':
    for i in range(5):
        t = threading.Thread(target=thread_test, args=(i,))
        t.start()

