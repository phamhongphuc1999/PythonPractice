from concurrent.futures import ThreadPoolExecutor


def _counter(counter, task_name):
    print("Start process {}!".format(task_name))
    while counter:
        print("{} : {}".format(task_name, counter))
        counter -= 1
    print("End process {}!".format(task_name))
    return "Completed {}!".format(task_name)


def _submit_thread():
    executor = ThreadPoolExecutor(max_workers=5)
    future = executor.submit(_counter, 1000, "task1")
    # print('futre result: ', future.result())


_submit_thread()
