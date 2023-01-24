import sys  # Keep at top to add to add root dir to PYTHONPATH.
from pathlib import Path  # Keep at top to add to add root dir to PYTHONPATH.

root = Path(__file__).parent.parent  # Keep at top to add to add root dir to PYTHONPATH.
sys.path.append(str(root))  # Keep at top to add to add root dir to PYTHONPATH.

# from app.read_data import read_portfolio_data
# from app.read_data import read_cashrisks_data

import pandas as pd
from datetime import date
from api.derivatives import get_all as get_all_der
from api.derivatives import get_portfolio as get_portfolio_der
from api.fx import get_all as get_all_fx
from api.fx import get_portfolio as get_portfolio_fx


# from .read_data import read_portfolio_data

def read_portfolio_data(file: [str], header: [int]):
    """
    Read data portfolios
    """
    portfolios = pd.read_excel(file, header=header)

    return portfolios


def read_cashrisks_data(file: [str], header: [int]):
    """
    Load cashrisks
    """
    cashrisks = pd.read_csv(file, header=header)
    cashrisks = cashrisks[['portfolio', 'risk']]

    return cashrisks


def get_risks(portfolio, cashrisks):
    """
    Get risks for all portfolios
    """
    risk_value_der = [{'portfolio': x, 'risk': get_portfolio_der(x, date.today())['Value']} for x in
                      (set(pd.Series(get_all_der()['Value'])) & set(portfolio.portfolio))]
    risk_value_fx = [{'portfolio': x, 'risk': get_portfolio_fx(x, date.today())['Value']} for x in
                     (set(pd.Series(get_all_fx()['Value'])) & set(portfolio.portfolio))]

    risks_der_fx = pd.DataFrame.from_records(risk_value_der + risk_value_fx)
    risks = pd.concat([risks_der_fx, cashrisks])
    risk_portfolio = portfolio.merge(risks, how='left', on='portfolio')

    return risk_portfolio


def find_hedge_ratio(risk_portfolio):
    """
    Find hedging ratio per client
    """
    hedge_ratio = risk_portfolio.groupby(by=['client'], dropna=True).apply(
        lambda x: abs(x[~x['scope'].isin(['Liabilities'])]['risk'].sum()
                      / x[x['scope'].isin(['Liabilities'])]['risk'].sum()))

    return hedge_ratio


def main():
    """
    Main entry point of app.
    """
    portfolio = read_portfolio_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/portfolios.xlsx', header=0)
    cashrisks = read_cashrisks_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/cashrisks.csv', header=0)

    risk_portfolio = get_risks(portfolio, cashrisks)
    hedge_ratio = find_hedge_ratio(risk_portfolio)

    pass


if __name__ == '__main__':
    main()
