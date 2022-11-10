import xmltodict


def xml2dict(xml_text: str) -> dict:
    data = xmltodict.parse(xml_text)
    return data


def dict2xml(data: dict) -> str:
    """
    树状结构，必须指定一个根元素
    """
    xml_text = xmltodict.unparse(data, pretty=True)
    return xml_text
