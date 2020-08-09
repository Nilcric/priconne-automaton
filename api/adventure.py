import os
import time
import random
import uiautomator2

from .cv import UIMatcher
from .base import *
from .utils import *
from .common import 教程


N_MAP = 12

MAP_POINTS = {
    'N': {
        1: (110, 290),
        2: (130, 410),
        3: (140, 190),
        4: (190, 240),
        5: (140, 200),
        6: (200, 390),
        7: (280, 200),
        8: (200, 250),
        9: (200, 200),
        10: (150, 190),
        11: (160, 320),
        12: (190, 200),
    },
    'H': {
        1: (250, 330),
        2: (290, 260),
        3: (260, 250),
        4: (250, 270),
        5: (250, 310),
        6: (270, 290),
        7: (280, 230),
        8: (220, 380),
        9: (220, 260),
        10: (220, 350),
        11: (220, 360),
        12: (220, 250),
    },
}


class Align(Command):
    '''
    已经进入主线地图后调用。
    切换到对应的主线地图。在一定点击次数内确定当前处于哪个地图，最终定位到需要刷的图。

    mode 为难度，普通 'N'，困难 'H'。x 为地图序号。
    例如想要刷 H10-3，则此处调用为 Align('H', 10)
    '''

    def __init__(self, mode, x):
        self.mode = mode
        self.x = x

    def __call__(self, device: uiautomator2.Device):
        if self.mode == 'N':
            FindImage('img/normal.jpg', else_=Click(708, 83, delay=1.5), retry=3)(device)
            FindImage('img/normal.jpg', else_=Delay('进入主线NORMAL关卡失败，请手动进入！'), retry=True)(device)
        if self.mode == 'H':
            FindImage('img/hard.jpg', else_=Click(830, 83, delay=1.5), retry=3)(device)
            FindImage('img/hard.jpg', else_=Delay('进入主线HARD关卡失败，请手动进入！'), retry=True)(device)

        map_index = None
        for _ in range(N_MAP):
            device.swipe_points(((240, 270), (720, 270)), 0.1)
            Delay(Delay.loading)(device)
            for i in range(1, N_MAP+1):
                image = 'new_img/map/%s%s.png' % (self.mode, i)
                if os.path.exists(image) and FindImage(image)(device):
                    map_index = i
                    break
            if map_index is not None:
                break
            Left()(device)

        Go(self.x - (map_index or 1))(device)
        Delay(Delay.loading)(device)
        device.swipe_points(((240, 270), (720, 270)), 0.1)
        Delay(Delay.loading)(device)


class 扫荡(Command):
    '''
    使用扫荡券完成关卡。需要在进入主线关卡界面后调用。
    例如 扫荡('N12-1', 3, 17) 即扫荡 N12-1 ~ N12-17 关卡，每个关卡扫荡 3 次。

    关卡：要扫荡的起始关卡，例如 'H10-1'。
    关卡数：连续扫荡的关卡的数量，默认为 1，即只扫荡当前关卡。
    '''

    def __init__(self, 关卡: str, 扫荡次数: int, 关卡数=1):
        self.mode = 关卡[0]
        self.map, self.level = [int(item) for item in 关卡[1:].split('-')]
        self.times = 扫荡次数
        self.levels = 关卡数

    def __call__(self, device: uiautomator2.Device):
        print('[扫荡] 关卡 = %s%s-%s, 扫荡次数 = %s, 关卡数 = %s' % (self.mode, self.map, self.level, self.times, self.levels))

        Sequence(
            # 点击关卡
            Align(self.mode, self.map),
            Click(*MAP_POINTS[self.mode][self.map]),
            Go(self.level - 1, delay=False),

            # 扫荡
            *(Sequence(
                FindImage('new_img/quest_ticket.png', else_=Delay('未在关卡界面内，请手动选择关卡！'), retry=True),
                *(Click(880, 335, delay=False) for _ in range(self.times - 1)),
                Click(760, 330),
                FindImage('new_img/no_chance.png', if_=Click(0, 0)),
                FindImage('img/tilibuzu.jpg', if_=Click(0, 0)),
                FindImage('img/ok.bmp', if_=Sequence(
                    ClickImage('img/ok.bmp'),
                    ClickImage('img/tiaoguo.jpg', else_=Delay(Delay.network)),
                    FindImage('new_img/quest_ticket.png', else_=Click(0, 0), retry=True),
                )),
                Right(delay=False),
            ) for _ in range(self.levels)),

            # 返回主线关卡界面
            FindImage('img/normal.jpg' if self.mode == 'N' else 'img/hard.jpg', else_=Click(0, 0), retry=True),
        )(device)


class 挑战(Command):
    '''
    不使用扫荡券完成关卡。需要在进入主线关卡界面后调用。

    例如 扫荡('N12-1') 即挑战 N12-1 关卡。最终返回主线关卡界面。

    若 教程=True，则在挑战完毕后会调用教程处理指令，最终返回主线关卡界面。
    '''

    def __init__(self, 关卡: str, 教程: bool = False):
        self.mode = 关卡[0]
        self.map, self.level = [int(item) for item in 关卡[1:].split('-')]
        self.tutorial = 教程

    def __call__(self, device: uiautomator2.Device):
        print('[挑战] 关卡 = %s%s-%s, 教程 = %s' % (self.mode, self.map, self.level, self.tutorial))

        def battle(device: uiautomator2.Device):
            FindImage('img/wanjiadengji.jpg', at=(233, 168, 340, 194), else_=Sequence(
                ClickImage('img/kuaijin.jpg', at=(891, 478, 936, 517), delay=False),
                ClickImage('img/auto.jpg', at=(891, 410, 936, 438), delay=False),
                Click(0, 0, delay=Delay.loading),
            ), retry=True)(device)

            Click(0, 0)(device)

            if self.tutorial:
                教程()(device)
                主线关卡()(device)

            FindImage('img/normal.jpg' if self.mode == 'N' else 'img/hard.jpg',
                      else_=ClickImage('img/xiayibu.jpg', else_=Click(0, 0)), retry=5)(device)

        Sequence(
            # 点击关卡
            Align(self.mode, self.map),
            Click(*MAP_POINTS[self.mode][self.map]),
            Go(self.level - 1, delay=False),

            # 挑战
            ClickImage('img/tiaozhan.jpg', delay=Delay.loading, else_=Delay('未找到挑战按钮，请手动点击！'), retry=True),
            FindImage('img/tilibuzu.jpg', if_=Sequence(
                Delay('体力不足，尝试回复体力'),
                ClickImage('img/ok.bmp'),
                ClickImage('img/ok.bmp'),
                FindImage('img/tiaozhan.jpg', else_=Click(0, 0), retry=3),
                ClickImage('img/tiaozhan.jpg', delay=Delay.loading, else_=Delay('未找到挑战按钮，请手动点击！'), retry=True),
            )),

            FindImage('img/zhandoukaishi.jpg', if_=Sequence(
                # 进入战斗
                ClickImage('img/zhandoukaishi.jpg'),
                battle,
            ), else_=Sequence(
                # 无法开始挑战，可能是没有挑战次数或者没有体力。
            )),

            FindImage('img/normal.jpg' if self.mode == 'N' else 'img/hard.jpg', else_=Click(0, 0), retry=3),
        )(device)


class 主线关卡(Command):
    '''
    进入主线关卡界面。主线关卡内的其他逻辑必须在该函数执行后才能执行。
    '''
    扫荡 = 扫荡
    挑战 = 挑战

    def __call__(self, device: uiautomator2.Device):
        print('[主线关卡]')

        Sequence(
            FindImage('new_img/main_quest.png', else_=Click(480, 539, delay=Delay.loading), retry=5),
            FindImage('new_img/main_quest.png', else_=Delay('进入冒险界面失败，请手动进入！'), retry=True),
        )(device)

        while True:
            Click(570, 210)(device)
            if FindImage('img/normal.jpg')(device):
                break
            if FindImage('img/hard.jpg')(device):
                break

        Delay(Delay.loading)(device)
