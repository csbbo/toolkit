from pypinyin import pinyin, Style


def chinese2pinyin_initials(name: str) -> str:
    """
    中文转拼音首字母
    """
    s = ''
    for letter in pinyin(name, style=Style.FIRST_LETTER, strict=False):
        s += letter[0][0]
    return s
