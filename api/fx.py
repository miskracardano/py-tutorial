import datetime as dt
import random
from time import sleep
from typing import Any, Dict

from api.core import parse_error, parse_response

__cache: Dict[str, int] = {
    'PortfolioA2': 20,
    'PortfolioB2': 220,
    'PortfolioD3': 70
}


def get_all() -> Dict[str, Any]:
    sleep(1)
    result = list(__cache.keys())
    return parse_response(value=result)


def get_portfolio(portfolio: str, date: dt.date) -> Dict[str, Any]:
    sleep(10)
    if not _is_request_valid(portfolio=portfolio, date=date):
        return parse_error(error=f'Invalid portfolio {portfolio} or date {date}.')

    random.seed(10_000*date.year + 100*date.month + date.day)
    alpha = random.random() + 1

    result = int(__cache[portfolio] * alpha)
    return parse_response(value=result)


def _is_request_valid(portfolio: str, date: dt.date) -> bool:
    if portfolio not in __cache:
        return False

    if date > dt.date.today():
        return False

    return True