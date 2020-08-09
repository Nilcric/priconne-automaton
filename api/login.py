import time
import random
import uiautomator2

from .cv import UIMatcher
from .base import *


class 登录(Command):
    '''
    在游戏的标题页面处登录的逻辑
    '''

    def __init__(self, 账号, 密码):
        self.account, self.password = str(账号), str(密码)

    def __call__(self, device: uiautomator2.Device):
        print('[登录] 账号 = %s, 密码 = %s' % (self.account, self.password))

        try:
            while True:
                if device(resourceId='com.bilibili.priconne:id/bsgamesdk_edit_username_login').exists():
                    break
                if device(resourceId='com.bilibili.priconne:id/bsgamesdk_id_welcome_change').exists():
                    device(resourceId='com.bilibili.priconne:id/bsgamesdk_id_welcome_change').click()
                else:
                    Click(0.965, 0.029)(device)

        except Exception as e:
            print(e)
            time.sleep(Delay.loading)

        device(resourceId='com.bilibili.priconne:id/bsgamesdk_edit_username_login').click()
        device.clear_text()
        device.send_keys(self.account)

        device(resourceId='com.bilibili.priconne:id/bsgamesdk_edit_password_login').click()
        device.clear_text()
        device.send_keys(self.password)

        device(resourceId='com.bilibili.priconne:id/bsgamesdk_buttonLogin').click()
        time.sleep(Delay.network * 2)

        if not device(resourceId='com.bilibili.priconne:id/bsgamesdk_edit_authentication_name').exists(timeout=0.1):
            # 无需实名认证
            return

        device(resourceId='com.bilibili.priconne:id/bsgamesdk_edit_authentication_name').click()
        device.clear_text()
        device.send_keys(self._random_name())

        device(resourceId='com.bilibili.priconne:id/bsgamesdk_edit_authentication_id_number').click()
        device.clear_text()
        device.send_keys(self._random_id())

        device(resourceId='com.bilibili.priconne:id/bsgamesdk_authentication_submit').click()
        device(resourceId='com.bilibili.priconne:id/bagamesdk_auth_success_comfirm').click()

    @staticmethod
    def _random_name():
        first_name = \
            '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜' \
            '戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐' \
            '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄' \
            '和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁' \
            '杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍' \
            '虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚' \
            '程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓' \
            '牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙' \
            '叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双' \
            '闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍卻璩桑桂濮牛寿通边扈燕冀郏浦尚农' \
            '温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘' \
            '匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空' \
            '曾毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逯盖益桓公万俟司马上官欧阳' \
            '夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠' \
            '公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空丌官司寇仉督子车' \
            '颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫法汝鄢涂钦' \
            '段干百里东郭南门呼延归海羊舌微生岳帅缑亢况郈有琴梁丘左丘东门西门' \
            '商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福百家姓终'

        last_name = \
            '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉' \
            '琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨' \
            '瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽伟' \
            '刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰' \
            '涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政' \
            '谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'

        return \
            (random.choice(first_name[:random.randrange(len(first_name))])) + \
            (random.choice(last_name)) + \
            (random.choice(last_name) if random.random() < 0.7 else '') + \
            (random.choice(last_name) if random.random() < 0.01 else '')

    @staticmethod
    def _random_id():
        provinces = [
            '11', '12', '13', '14', '15',
            '21', '22', '23',
            '31', '32', '33', '34', '35', '36', '37',
            '41', '42', '43', '44', '45', '46',
            '50', '51', '52', '53', '54',
            '61', '62', '63', '64', '65',
        ]

        region = '%s%02d%02d' % (random.choice(provinces), random.randrange(5), random.randrange(5))
        birthday = '%02d%02d%02d' % (random.randrange(1990, 2000), random.randint(1, 12), random.randint(1, 28))
        order = '%03d' % (random.randrange(1000))
        result = region + birthday + order

        checksum = 0
        for i in range(17):
            checksum += ((1 << (17 - i)) % 11) * int(result[i])
        check_digit = (12 - (checksum % 11)) % 11
        result += str(check_digit) if check_digit < 10 else 'X'

        return result


class 登出(Command):
    '''
    切换账号
    '''

    def __call__(self, device: uiautomator2.Device):
        print('[登出]')
        Sequence(
            FindImage('img/bangzhu.bmp', else_=Click(871, 513, Delay.loading), retry=3),  # 主菜单
            FindImage('img/bangzhu.bmp', else_=Delay('进入主菜单失败，请主动点击'), retry=True),
            Click(165, 411, delay=Delay.loading),  # 退出账号
            ClickImage('img/ok.bmp', else_=Delay('点击退出账号失败，请主动点击'), retry=True),  # OK
            Delay(Delay.network),
        )(device)
