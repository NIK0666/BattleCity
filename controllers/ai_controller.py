import time


class AIController:
    """Отвечает за управление искуственным интелектом"""
    DELTA_TIME = 0.2

    def __init__(self):
        self.upd_time = time.time()
        pass

    def update(self):
        curr_time = time.time()
        if curr_time - self.upd_time >= self.DELTA_TIME:
            pass
        self.upd_time = curr_time
