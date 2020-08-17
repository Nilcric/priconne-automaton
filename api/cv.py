import numpy
import cv2


class UIMatcher:

    @classmethod
    def where(cls, screen, template, threshold=None, at=None):
        """
        在screen里寻找template，若找到则返回坐标，若没找到则返回False
        注：可以使用if where():  来判断图片是否存在
        :param threshold:
        :param screen:
        :param template:
        :param at: 缩小查找范围
        :return:
        """
        threshold = threshold or 0.84

        if at is not None:
            x1, y1, x2, y2 = at
            screen = screen[y1:y2, x1:x2]
        else:
            x1, y1 = 0, 0

        try:
            template = cv2.imread(template)
        except:
            pass

        th, tw = template.shape[:2]  # rows->h, cols->w
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        # print(template_path, max_val)

        if max_val >= threshold:
            x = x1 + max_loc[0] + tw // 2
            y = y1 + max_loc[1] + th // 2
            return x, y
        else:
            return False

    @classmethod
    def wheres(cls, screen, template_paths, threshold=0.84):
        """
        依次检测template_paths中模板是否存在，返回存在图片字典
        :param screen:
        :param template_paths:
        :param threshold:
        :return:
        """
        return_dic = {}
        for template_path in template_paths:
            pos = cls.where(screen, template_path, threshold)
            if pos:
                return_dic[template_path] = pos
        return return_dic

    @classmethod
    def highlight(cls, screen):
        """
        检测高亮位置(忽略了上板边,防止成就栏弹出遮挡)
        @return: 高亮中心相对坐标[x,y]
        """
        gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        ret, binary = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
        num_of_white = len(numpy.argwhere(binary == 255))
        index_1 = numpy.mean(numpy.argwhere(binary[63:, :] == 255), axis=0).astype(int)

        # screen = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
        # cv2.circle(screen, (index_1[1], index_1[0] + 63), 10, (255, 0, 0), -1)

        return num_of_white, int(index_1[1]), int(index_1[0] + 63)

    characters = cv2.imread('new_img/characters.png')

    @classmethod
    def whois(cls, screen, x, y, size):
        x1, y1, x2, y2 = x, y, x+size, y+size
        screen = screen[y1:y2, x1:x2]
        screen = cv2.resize(screen, (64, 64))
        ans = cls.where(cls.characters, screen, threshold=0.4)
        print(ans)
        if not ans:
            return 1000
        return 1000 + ans[1] // 64
