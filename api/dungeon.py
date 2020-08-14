import uiautomator2

from .base import *
from .home import home
from .common import 教程


MAP_POINTS = {
    0: (250, 250),
}

LEVEL_POINTS = {
    0: [(670, 270)],
}


class 地下城(Command):
    '''
    挑战地下城。
    地图 0：云海的山脉，借用助战，只打一关。1：云海的山脉。2：密林的大树。3：断崖的遗迹。

    进入地下城界面后，若上一次未挑战完毕将会自动撤退。
    请在我的主页调用进入地下城。请确保地下城已经开放。
    TODO: 地下城进入时若有地下城币可能会有教程。
    '''

    def __init__(self, 地图=0):
        self.map = 地图

    def __str__(self):
        return '地下城(地图=%s)' % (self.map)

    def __call__(self, device: uiautomator2.Device):
        Sequence(
            Log(Log.INFO, str(self)),
            FindImage('new_img/main_quest.png', else_=Click(480, 539, delay=Delay.loading), retry=5),
            FindImage('new_img/main_quest.png', else_=Delay('进入冒险界面失败，请手动进入！'), retry=True),
        )(device)

        t = 0
        while t < 2:
            ClickImage('img/dixiacheng.jpg')(device)
            Click(0, 0)(device)

            if FindImage('img/yunhai.bmp', threshold=0.8)(device):
                t += 1
                continue

            if ClickImage('img/chetui.jpg')(device):
                ClickImage('img/ok.bmp')(device)

            t = 0

        # 进入地图
        if not ClickImage('img/ok.bmp', delay=Delay.network + Delay.loading * 3,
                          else_=Click(*MAP_POINTS[self.map]), retry=6)(device):
            Sequence(
                Log(Log.WARNING, '进入地下城地图失败，返回主页！'),
                home,
            )(device)
            return

        FindImage('img/chetui.jpg', else_=Click(0, 0), retry=True)(device)

        for i, point in enumerate(LEVEL_POINTS[self.map]):
            Click(*point)(device)

            if not FindImage('img/tiaozhan.bmp', else_=Click(*point), retry=5)(device):
                Sequence(
                    教程(),
                    FindImage('new_img/main_quest.png', else_=Click(480, 539, delay=Delay.loading), retry=5),
                    FindImage('new_img/main_quest.png', else_=Delay('进入冒险界面失败，请手动进入！'), retry=True),
                    ClickImage('img/dixiacheng.jpg', delay=Delay.network + Delay.loading)(device),
                    FindImage('img/tiaozhan.bmp', else_=Click(*point), retry=True),
                )(device)

            ClickImage('img/tiaozhan.bmp', delay=Delay.network, retry=5)(device)

            if i == 0:  # 第一次需要选人
                if self.map:
                    # 正常打，选择队伍，暂时没有实现
                    raise NotImplementedError()
                else:
                    Sequence(
                        Click(480, 90),  # 选择支援
                        Click(110, 180, delay=False),
                        Click(220, 180, delay=False),
                        Click(330, 180, delay=False),
                        Click(440, 180, delay=False),
                        Click(100, 90),  # 选择自己的角色
                        Click(110, 180, delay=False),
                        Click(220, 180, delay=False),
                        Click(330, 180, delay=False),
                        Click(440, 180, delay=False),
                    )(device)

            if FindImage('img/notzhandoukaishi.bmp', threshold=0.9)(device):
                # 无法出战，退出
                Sequence(
                    Log(Log.WARNING, '无法出战，退出地下城！'),
                    FindImage('img/chetui.jpg', else_=Click(0, 0)),
                )(device)
                break

            Sequence(
                ClickImage('img/zhandoukaishi.jpg', at=(758, 427, 917, 479), retry=3),
                ClickImage('img/ok.bmp', retry=3),

                # 战斗循环
                FindImage('img/shanghaibaogao.jpg', retry=True, else_=Sequence(
                    ClickImage('img/kuaijin.jpg', at=(891, 478, 936, 517), delay=False),
                    ClickImage('img/kuaijin_1.jpg', at=(880, 470, 950, 530), delay=False),
                    ClickImage('img/auto.jpg', at=(891, 410, 936, 438), delay=False),
                    Click(0, 0, delay=Delay.loading),
                )),

                # 战斗结束
                ClickImage('img/xiayibu.jpg'),
                FindImage('img/zhandou_ok.jpg', else_=Click(0, 0), retry=True),  # 奖励框跳出
                FindImage('img/chetui.jpg', else_=Click(0, 0), retry=True),
                Delay(Delay.loading * 3),  # 等待角色走过去
            )(device)

        Sequence(
            ClickImage('img/chetui.jpg'),
            ClickImage('img/ok.bmp'),
            home,
        )(device)
