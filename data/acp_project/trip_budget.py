"""Расчёт стоимости перекуса; в исходном примере есть ошибка."""


def total_cost(items):
    """items — пары (цена в рублях, количество)."""
    return sum(price for price, quantity in items)
