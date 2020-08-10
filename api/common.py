import time
import random
import uiautomator2

from .cv import UIMatcher
from .base import *


class 教程(Command):
    '''
    处理教程, 最终返回我的主页
    '''

    def __call__(self, device: uiautomator2.Device):
        '''
        有引导点引导
        有下一步点下一步
        有主页点主页
        有圆menu就点跳过，跳过
        有跳过点跳过
        都没有就点边界点
        # 有取消点取消
        '''

        class SkipBattle(Command):
            '''
            可跳过的战斗，用于新手教程，一共两场
            '''

            def __init__(self):
                self.count = 2

            def __call__(self, device: uiautomator2.Device):
                if not self.count:
                    return False

                ClickImage('img/caidan.jpg', at=(861, 15, 940, 37), delay=Delay.loading)(device)
                Click(593, 372)(device)
                self.count -= 1
                return True

        skip_battle = SkipBattle()
        t = 0

        while t < 2:
            Delay(Delay.loading)(device)

            # 点击引导
            screenshot = device.screenshot(format='opencv')
            n, x, y = UIMatcher.highlight(screenshot)
            if n < 77000:
                try:
                    Click(x, y + 20, delay=Delay.loading)(device)
                except AssertionError:
                    pass
                continue

            # 在我的主页
            if UIMatcher.where(screenshot, 'img/liwu.bmp', at=(891, 413, 930, 452)):
                t += 1
                continue

            # 行会教程
            if UIMatcher.where(screenshot, 'img/jiaruhanghui.jpg'):
                t += 1
                continue

            if (
                ClickImage('img/tongyi.jpg', at=(490, 459, 686, 496))(device) or
                ClickImage('img/dengji.jpg', at=(382, 352, 578, 391))(device) or
                ClickImage('img/ok.bmp')(device) or
                ClickImage('img/xiayibu.jpg')(device) or
                ClickImage('img/niudan_jiasu.jpg', at=(700, 0, 960, 100))(device) or
                ClickImage('img/wuyuyin.jpg', at=(450, 355, 512, 374))(device) or
                ClickImage('img/tiaoguo.jpg')(device) or
                ClickImage('img/zhuye.jpg', at=(46, 496, 123, 537))(device)
            ):
                continue

            if FindImage('img/caidan.jpg', at=(861, 15, 940, 37))(device):
                if skip_battle(device):
                    continue

            if FindImage('img/caidan_yuan.jpg', at=(898, 23, 939, 62), if_=Sequence(
                # 剧情
                ClickImage('img/caidan_yuan.jpg', at=(898, 23, 939, 62), delay=Delay.loading),
                Click(804, 45),
                Click(593, 372),
            ))(device):
                continue

            if FindImage('img/qianwanghuodong.bmp', if_=Sequence(
                Click(390, 369, delay=Delay.loading),
                Click(390, 369, delay=Delay.loading),
                Click(390, 369, delay=Delay.loading),
            ))(device):
                continue

            if FindImage('img/jingsaikaishi.bmp', at=(755, 471, 922, 512), if_=Sequence(
                # 赛马
                Click(786, 308, delay=0.2),  # 选择角色
                Click(842, 491, delay=0.5),  # 开始
            ))(device):
                continue

            if FindImage('img/kuaijin.jpg', at=(891, 478, 936, 517), if_=Sequence(
                Click(911, 493),
            ))(device):
                continue

            Click(0, 0, delay=False)(device)
            t = 0


class 设定(Command):
    '''
    设定跳过动画以及帧率
    '''

    def __call__(self, device: uiautomator2.Device):

        Sequence(
            Click(880, 520, delay=Delay.loading*1.5),
            Click(149, 269, delay=Delay.loading),
            Click(769, 87),
            Click(735, 238, delay=False),
            Click(735, 375, delay=False),
            Click(480, 480, delay=Delay.loading),
            Click(95, 516, delay=Delay.network),
        )(device)
