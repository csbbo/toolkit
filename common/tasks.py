import time

import dramatiq


@dramatiq.actor(queue_name="main")
def cal_number() -> None:
    for i in range(100):
        print(i)
        time.sleep(1)
