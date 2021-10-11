from concurrent.futures import ProcessPoolExecutor


def _counter(counter, task_name):
    print("Start process {}!".format(task_name))
    while counter:
        print("{} : {}".format(task_name, counter))
        counter -= 1
    print("End process {}!".format(task_name))
    return "Completed {}!".format(task_name)


def _submit_process():
    executor = ProcessPoolExecutor(max_workers=5)
    future = executor.submit(_counter, 10, "task1")
    print('State of future: ', future.done())
    print('futre result: ', future.result())
    print('State of future: ', future.done())


_submit_process()
