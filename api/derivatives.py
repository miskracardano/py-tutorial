import datetime as dt
import random
from time import sleep

from api.core import JsonDict, parse_error, parse_response

__CUTOFF_DATE = dt.date.today()
__CACHE: dict[str, int] = {
    "PortfolioA3": 75,
    "PortfolioA4": 75,
    "PortfolioA6": 60,
    "PortfolioB3": 135,
    "PortfolioC1": 100,
    "PortfolioC2": 130,
    "PortfolioC4": 30
}


def get_all_portfolios() -> JsonDict:
    sleep(1)
    result = list(__CACHE.keys())
    return parse_response(result)


def get_portfolio_risks(portfolio: str, date: dt.date) -> JsonDict:
    sleep(10)
    if not _is_request_valid(portfolio, date):
        return parse_error(f"Invalid portfolio {portfolio} or date {date}.")

    random.seed(10_000 * date.year + 100 * date.month + date.day)
    alpha = random.random() + 1

    result = int(__CACHE[portfolio] * alpha)
    return parse_response(result)


def _is_request_valid(portfolio: str, date: dt.date) -> bool:
    if portfolio not in __CACHE:
        return False

    return date <= __CUTOFF_DATE
