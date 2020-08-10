import re
import uiautomator2


from .base import *
from .adventure import 主线关卡


class 扫荡模板(Command):
    '''
    根据账号文件中要求生成扫荡指令。
    '''

    N_MAP_LEVELS = {
        'N': {
            1: 10, 2: 12, 3: 12, 4: 13, 5: 13, 6: 14,
            7: 14, 8: 15, 9: 15, 10: 17, 11: 17, 12: 17,
        },
        'H': {
            x: 3 for x in range(1, 13)
        }
    }

    def __init__(self, note: str):
        self.note = note

    def __call__(self, device: uiautomator2.Device):
        commands = []

        for arg in self.note.split():
            try:
                key, value = arg.split('=')
                assert key == '扫荡'
            except (TypeError, ValueError, AssertionError):
                continue

            for level in value.split(','):
                try:
                    level = level.upper()
                    match = re.match(r'^(N|H)(\d+)(-(\d+))?((~|～)(N|H)?(\d+)(-(\d+))?)?((\*|x|×)(\d+))?$', level)
                    assert match

                    mode0, map0, _, level0, _, _, mode1, map1, _, level1, _, _, times = match.groups()
                    assert not mode1 or mode0 == mode1
                    times = int(times) if times else 1

                    if level1:
                        if level0:  # H10-3~H11-4
                            command = 主线关卡.扫荡('%s%s-%s' % (mode0, map0, level0), times,
                                              关卡数=sum(self.N_MAP_LEVELS[mode0][x] for x in range(int(map0), int(map1))) + int(level1) - int(level0) + 1)
                        else:  # H10~H11-4
                            command = 主线关卡.扫荡('%s%s-%s' % (mode0, map0, 1), times,
                                              关卡数=sum(self.N_MAP_LEVELS[mode0][x] for x in range(int(map0), int(map1))) + int(level1))
                    elif map1:
                        if not level0:  # H10~H11
                            command = 主线关卡.扫荡('%s%s-%s' % (mode0, map0, 1), times,
                                              关卡数=sum(self.N_MAP_LEVELS[mode0][x] for x in range(int(map0), int(map1)+1)))
                        elif not mode1:  # H10-3~12
                            command = 主线关卡.扫荡('%s%s-%s' % (mode0, map0, level0), times,
                                              关卡数=int(map1)-int(level0)+1)
                        else:  # H10-3~H12
                            command = 主线关卡.扫荡('%s%s-%s' % (mode0, map0, level0), times,
                                              关卡数=sum(self.N_MAP_LEVELS[mode0][x] for x in range(int(map0), int(map1)+1)) - int(level0) + 1)
                    else:
                        if level0:  # H10-1
                            command = 主线关卡.扫荡('%s%s-%s' % (mode0, map0, level0), times)
                        else:  # H10
                            command = 主线关卡.扫荡('%s%s-%s' % (mode0, map0, 1), times,
                                              关卡数=self.N_MAP_LEVELS[mode0][int(map0)])

                    commands.append(command)

                except (TypeError, ValueError, AssertionError) as e:
                    Log(Log.WARNING, '扫荡参数 %s 无法识别：%s' % (level, e))(device)

        Sequence(*commands)(device)
