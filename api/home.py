import time
import random
import uiautomator2

from .cv import UIMatcher
from .base import *


home = FindImage('img/liwu.bmp', at=(891, 413, 930, 452), else_=Click(100, 539, delay=Delay.network), retry=True)


class 体力(Command):
    '''
    购买体力，需要在我的主页时调用
    '''

    def __init__(self, 次数: int):
        self.x = 次数

    def __call__(self, device: uiautomator2.Device):
        print('[体力] 次数 = %s' % self.x)

        s = Sequence(
            Click(320, 31),
            ClickImage('img/ok.bmp'),
            ClickImage('img/zhandou_ok.jpg'),
            Click(131, 533),  # 点击一下首页比较保险
        )

        Sequence(
            home,
            *(s for _ in range(self.x)),
            home,
        )(device)


class 玛那(Command):
    '''
    购买玛那，逻辑始终为先单抽再批量，次数为点击次数
    '''

    def __init__(self, 次数):
        self.x = 次数

    def __call__(self, device: uiautomator2.Device):
        print('[玛那] 次数 = %s' % self.x)

        s0 = Sequence(
            FindImage('img/quxiao2.jpg', else_=Click(0, 0), retry=True),
            Click(596, 471),
            ClickImage('img/ok.bmp'),
            Delay(Delay.network + 1.1),
        )
        s1 = Sequence(
            FindImage('img/quxiao2.jpg', else_=Click(0, 0), retry=True),
            Click(816, 478),
            ClickImage('img/ok.bmp'),
            Delay(Delay.network + 1.1 * 10),
        )

        Sequence(
            home,
            Click(189, 62),
            *(s1 if i else s0 for i in range(self.x)),
            FindImage('img/quxiao2.jpg', else_=Delay(Delay.loading), retry=True),
            home,
        )(device)


class 经验药剂(Command):
    '''
    购买经验药剂
    '''

    def __call__(self, device: uiautomator2.Device):
        print('[经验药剂]')

        Sequence(
            home,
            Click(617, 435, delay=Delay.network),
            FindImage('img/tongchang.jpg', else_=Click(0, 0), retry=3),
            Click(387, 151, delay=False),
            Click(557, 151, delay=False),
            Click(729, 151, delay=False),
            Click(900, 151, delay=False),
            Click(785, 438),
            ClickImage('img/ok.bmp', delay=Delay.network),
            ClickImage('img/ok.bmp', else_=Click(0, 0)),
            home,
        )(device)


class 任务(Command):
    '''
    收取任务报酬，需要在我的主页调用
    '''

    def __call__(self, device: uiautomator2.Device):
        print('[任务]')

        Sequence(
            home,
            ClickImage('img/renwu.jpg', delay=Delay.network),
            Click(846, 437, delay=Delay.network),
            home,
        )(device)


class 礼物(Command):
    '''
    收取礼物，需要在我的主页调用
    '''

    def __call__(self, device: uiautomator2.Device):
        print('[礼物]')

        Sequence(
            home,
            FindImage('img/shouqulvli.jpg', at=(98, 458, 199, 496), else_=Click(910, 434), retry=True),
            Click(811, 477),
            ClickImage('img/ok.bmp', delay=Delay.network),
            Click(0, 0),
            home,
        )(device)


class 我的主页(Command):
    '''
    进入我的主页
    '''

    体力 = 体力
    玛那 = 玛那
    经验药剂 = 经验药剂
    任务 = 任务
    礼物 = 礼物

    def __call__(self, device: uiautomator2.Device):
        print('[我的主页]')

        t = 0

        while t < 3:
            time.sleep(Delay.loading)
            screenshot = device.screenshot(format='opencv')

            if UIMatcher.where(screenshot, 'img/liwu.bmp', at=(891, 413, 930, 452)):
                t += 1

            if UIMatcher.where(screenshot, 'img/niudan_jiasu.jpg', at=(700, 0, 960, 100)):
                # 跳过新角色登场
                Click(893, 39)(device)
                continue

            if UIMatcher.where(screenshot, 'img/jingsaikaishi.bmp', at=(755, 471, 922, 512)):
                # 赛马
                Click(786, 308, delay=0.2)(device)  # 选择角色
                Click(842, 491, delay=0.5)(device)  # 开始
                continue

            Click(90, 539, False)(device)
            Click(330, 270, False)(device)

        # 原版逻辑：这里防一波第二天可可萝跳脸教程
        screenshot = device.screenshot(format='opencv')
        num, _, _ = UIMatcher.highlight(screenshot)
        if num < 50000:
            FindImage('img/renwu_1.bmp', else_=Click(837, 433, delay=1.0), retry=True)(device)
            FindImage('img/liwu.bmp', at=(891, 413, 930, 452), else_=Click(90, 514, delay=0.2))(device)
            return
        if UIMatcher.where(screenshot, 'img/kekeluo.bmp'):
            FindImage('img/renwu_1.bmp', else_=Click(837, 433, delay=1.0), retry=True)(device)
            FindImage('img/liwu.bmp', at=(891, 413, 930, 452), else_=Click(90, 514, delay=0.2))(device)
