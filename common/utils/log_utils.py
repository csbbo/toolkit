from common.constants.common import LogType
from common.models import Log


def save_stock_op_log(search: str, response: str, request_from: str, ip: str) -> None:
    info = {
        "search": search,
        "response": response,
        "request_from": request_from,
        "ip": ip,
    }
    Log.objects.create(info=info, type=LogType.STOCK_OP)
