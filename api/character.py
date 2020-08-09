import time
import random
import uiautomator2

from .cv import UIMatcher
from .base import *
from .utils import *


class LevelUp(Command):
    '''
    自动强化一个角色，需要已经点击进入该角色的详情页时调用。
    '''

    def __init__(self, get_equipments=False):
        self.get_equipments = get_equipments

    def __call__(self, device: uiautomator2.Device):
        while True:
            if self.get_equipments:
                raise NotImplementedError()

            if ClickImage('img/ranktisheng.jpg', at=(206, 325, 292, 346))(device):
                Sequence(
                    ClickImage('img/queren.jpg'),  # 若已经装备则按钮是确认
                    ClickImage('img/ok.bmp'),  # 否则按钮是OK
                    Delay(Delay.network + 5.0),
                    Click(481, 369),
                )(device)
                continue

            Click(370, 440)(device)
            Click(540, 468, delay=Delay.network)(device)  # 能点击确认、OK、并且不能点到冒险、获取方法
            break


class 自动强化(Command):
    '''
    自动强化前 x 个角色，包括 RANK 提升。
    缺少装备时不自动刷取。
    请在我的主页或其他能点击角色的时候调用。
    '''

    def __init__(self, 角色数=5):
        self.x = 角色数

    def __call__(self, device: uiautomator2.Device):
        print('[自动强化] 角色数 = %s' % self.x)
        Sequence(
            Delay(Delay.click),
            Click(210, 520, delay=Delay.loading*2),  # 进入角色页面
            Click(200, 160, delay=Delay.loading*2),  # 点击第一个角色
            *(Sequence(
                LevelUp(),  # 强化
                Right(),  # 下一个角色
            ) for _ in range(self.x))
        )(device)


class 角色(Command):
    自动强化 = 自动强化

    def __call__(self, device: uiautomator2.Device):
        pass
