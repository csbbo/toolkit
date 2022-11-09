from stock.models import Stock


def batch_save_stocks(items: list, batch_size: int = 100) -> None:
    bulk_create_list = []
    for item in items:
        bulk_create_list.append(Stock(**item))
    Stock.objects.bulk_create(
        bulk_create_list, ignore_conflicts=True, batch_size=batch_size
    )
