import uiautomator2

from .base import *
from .utils import *
from .home import home


class 捐赠(Command):
    '''
    处理行会中所有捐赠请求。
    若行会中请求的人比较多，可以把 retry 调高。
    '''

    def __init__(self, retry=2):
        self.retry = retry

    def __call__(self, device: uiautomator2.Device):
        Log(Log.INFO, '[捐赠]')(device)
        t = 0
        while t < self.retry:
            if not ClickImage('img/juanzengqingqiu.jpg')(device):
                break
            if not ClickImage('new_img/donate.png', threshold=0.9)(device):
                t += 1
                continue

            Sequence(
                Click(650, 390, delay=False),  # MAX
                Click(590, 480),  # OK
                FindImage('img/hanghui.bmp', else_=Click(0, 0), retry=True),
            )(device)
            t = 0


class 点赞(Command):
    '''
    给行会中战力最高的成员点赞。
    需要确保已经进入行会界面，并且账号已经加入行会。
    '''

    def __call__(self, device: uiautomator2.Device):
        Sequence(
            Log(Log.INFO, '[点赞]'),
            Click(240, 350, delay=Delay.network),  # 成员信息
            Click(720, 95),  # 排序
            Click(290, 305, delay=False),  # 全角色战力
            Click(590, 370, delay=Delay.loading),  # OK
            Click(830, 200),  # 给第一名点赞
            ClickImage('img/ok.bmp'), # 点赞失败可能会需要点击 OK
            FindImage('img/hanghui.bmp', else_=Click(30, 30, delay=Delay.loading), retry=True),  # 返回行会
        )(device)


class 行会(Command):
    '''
    行会界面的相关操作。进入行会需要在我的主页或其他能点击到我的主页的情况下调用。

    成功返回 True，未加入行会或行会未解锁返回 False。
    '''

    点赞 = 点赞
    捐赠 = 捐赠

    def __call__(self, device: uiautomator2.Device):
        Sequence(
            Log(Log.INFO, '[行会]'),
            home,
            Click(690, 430, delay=Delay.network),
        )(device)

        t = 0
        while t < 2:
            Click(0, 0, delay=False)(device)
            if FindImage('img/hanghui.bmp')(device) or FindImage('img/zujianhanghui.bmp')(device):
                t += 1
            else:
                t = 0

        if not FindImage('img/hanghui.bmp')(device):
            Log(Log.WARNING, '该账号未加入行会')(device)
            return False

        return True
