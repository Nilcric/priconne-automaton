import os
import sys
import time
import logging
import uiautomator2

from .cv import UIMatcher


__all__ = ['Command', 'Delay', 'Click', 'FindImage', 'ClickImage', 'Sequence', 'Log']


class Command():
    '''
    指令类。执行指令需要创建指令的实例，然后再用指令实例调用设备。
    '''

    def __call__(self, device: uiautomator2.Device):
        pass


class Delay(Command):
    '''
    等待，延时，单位为秒。
    '''

    network = 2.5
    loading = 1.0
    click = 0.01

    def __init__(self, x):
        self.x = x

    def __call__(self, device: uiautomator2.Device):
        if isinstance(self.x, str):
            print(self.x)
            self.x = self.loading
        time.sleep(self.x)


class Click(Command):
    '''
    点击屏幕，参数可以是 float（比例）或者 int（像素）
    '''

    def __init__(self, x, y, delay=True):
        self.x, self.y = x, y
        self.delay = delay

    def __call__(self, device: uiautomator2.Device):
        x = self.x if isinstance(self.x, int) else int(self.x * device.window_size()[0])
        y = self.y if isinstance(self.y, int) else int(self.y * device.window_size()[1])
        device.click(x, y)
        if isinstance(self.delay, (int, float)):
            time.sleep(self.delay)
        elif self.delay is True:
            time.sleep(Delay.click)


class FindImage(Command):
    '''
    在屏幕上寻找控件，并按照寻找结果执行相应内容
    默认不重试（即0次），无限重试请传入 retry=True
    '''

    def __init__(self, image, at=None, if_=None, else_=None, retry=0):
        self.image = image
        self.at = at
        self.if_ = if_
        self.else_ = else_
        self.retry = retry

    def __call__(self, device: uiautomator2.Device):
        attempt = 0
        while True:
            screenshot = device.screenshot(format='opencv')
            if UIMatcher.where(screenshot, self.image, at=self.at):
                if self.if_:
                    self.if_(device)
                break
            else:
                if self.else_:
                    self.else_(device)
            attempt += 1
            if self.retry is not True and attempt >= self.retry:
                return False
        return True


class ClickImage(Command):
    '''
    在屏幕上寻找控件，并点击该控件
    默认不重试（即0次），无限重试请传入 retry=True
    '''

    def __init__(self, image, at=None, delay=True, else_=None, retry=0):
        self.image = image
        self.at = at
        self.delay = delay
        self.else_ = else_
        self.retry = retry

    def __call__(self, device: uiautomator2.Device):
        attempt = 0
        while True:
            screenshot = device.screenshot(format='opencv')
            point = UIMatcher.where(screenshot, self.image, at=self.at)
            if point:
                Click(*point, self.delay)(device)
                break
            else:
                if self.else_:
                    self.else_(device)
            attempt += 1
            if self.retry is not True and attempt >= self.retry:
                return False
        return True


class Sequence(Command):
    '''
    序列，一系列需要做的东西
    '''

    def __init__(self, *args):
        self.args = args

    def __call__(self, device: uiautomator2.Device):
        for arg in self.args:
            arg(device)


class Log(Command):
    '''
    日志，分账号记录在文件中
    '''

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, level, message):
        self.level = level
        self.message = message

    def __call__(self, device: uiautomator2.Device):
        name = device.username
        logger = logging.getLogger(name)
        if not logger.handlers:
            os.makedirs('log', exist_ok=True)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
            file_handler = logging.FileHandler('log/%s.txt' % name, encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            logger.setLevel(logging.DEBUG)
            logger.propagate = False

        logger.log(self.level, self.message)
