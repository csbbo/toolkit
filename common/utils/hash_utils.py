import hashlib
from typing import Union


def get_md5(content: Union[str, bytes], encoding: str = "utf-8") -> str:
    if isinstance(content, str):
        content = content.encode(encoding)

    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()


def get_sha1(content: Union[str, bytes], encoding: str = "utf-8") -> str:
    if isinstance(content, str):
        content = content.encode(encoding)

    m = hashlib.sha1()
    m.update(content)
    return m.hexdigest()


def get_sha256(content: Union[str, bytes], encoding: str = "utf-8") -> str:
    if isinstance(content, str):
        content = content.encode(encoding)

    m = hashlib.sha256()
    m.update(content)
    return m.hexdigest()
