import random
from string import digits

from pypinyin import Style, pinyin


def chinese2pinyin_initials(name: str) -> str:
    """
    中文转拼音首字母
    """
    s = ""
    for letter in pinyin(name, style=Style.FIRST_LETTER, strict=False):
        s += letter[0][0]
    return s


def get_random_lower_str(length: int = 4) -> str:
    """
    获取指定长度的随机字符串(小写)
    :param length:
    :return:
    """
    return "".join(random.choice(digits) for _ in range(length))
