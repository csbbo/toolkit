import logging
import os
from typing import Optional

import oss2

logger = logging.getLogger(__name__)

INTERVAL_TIME = 1
OSS_MAX_RETRY_COUNT = 3


def get_bucket() -> oss2.Bucket:
    accesskey_id = os.getenv("OSS_ACCESSKEY_ID")
    accesskey_secret = os.getenv("OSS_ACCESSKEY_SECRET")
    bucket = os.getenv("OSS_BUCKET")
    bucket_endpoint = os.getenv("OSS_BUCKET_ENDPOINT")

    auth = oss2.Auth(accesskey_id, accesskey_secret)
    return oss2.Bucket(auth, bucket_endpoint, bucket)


def upload_stream(key: str, stream: bytes) -> None:
    bucket = get_bucket()
    bucket.put_object(key, stream)


def upload_file(key: str, filename: str, headers: Optional[dict] = None) -> None:
    """
    https://help.aliyun.com/document_detail/88426.html
    """
    bucket = get_bucket()
    bucket.put_object_from_file(key, filename, headers)


def get_url(key: str, expires: int = 3600) -> str:
    bucket = get_bucket()
    return bucket.sign_url(method="GET", key=key, expires=expires, slash_safe=True)


def get_upload_url(
    key: str, *, expires: int = 60, content_type: str = ""
) -> Optional[str]:
    bucket = get_bucket()
    return bucket.sign_url(
        "PUT",
        key=key,
        expires=expires,
        headers={"Content-Type": content_type},
        slash_safe=True,
    )


def batch_delete(key_list: list) -> None:
    bucket = get_bucket()
    bucket.batch_delete_objects(key_list)


def upload_public_read_file(key: str, filename: str) -> None:
    """
    https://help.aliyun.com/document_detail/31986.html
    """
    upload_file(key, filename, {"x-oss-object-acl": oss2.OBJECT_ACL_PUBLIC_READ})
