"""
The main goal of this script is to display risks and hedging ratios per client. This script combines data from various
resources and calculates the corresponding hedge ratio per client. Finally, the risks associated with the portfolios and 
the corresponding hedge ratios per client are displayed. 
"""

__author__ = "Linda Torn"

import sys  # Keep at top to add to add root dir to PYTHONPATH.
from pathlib import Path  # Keep at top to add to add root dir to PYTHONPATH.
import pandas as pd
from datetime import date
from api.derivatives import get_all as get_all_der
from api.derivatives import get_portfolio as get_portfolio_der
from api.fx import get_all as get_all_fx
from api.fx import get_portfolio as get_portfolio_fx

root = Path(__file__).parent.parent  # Keep at top to add to add root dir to PYTHONPATH.
sys.path.append(str(root))  # Keep at top to add to add root dir to PYTHONPATH.


def read_portfolio_data(file: [str], header: [int]):
    """
    Read portfolio data form xlsx file.

    :param file: portfolio.xlsx file
    :param header: declare row used for column headers
    :return: data from the portfolio.xlsx file
    """
    portfolios = pd.read_excel(file, header=header)

    return portfolios


def read_cashrisks_data(file: [str], header: [int]):
    """
    Load cashrisks from csv file and extract useful information.

    :param file: cashrisks.csv file
    :param header: declare row used for column headers
    :return: data from cashrisks.csv file
    """
    cashrisks = pd.read_csv(file, header=header)
    cashrisks = cashrisks[['portfolio', 'risk']]

    return cashrisks


def get_risks(portfolio, cashrisks):
    """
    Get risks for all portfolios using the input from :meth: `~api.derivatives.get_portfolio`,
    :meth: `~api.fx.get_portfolio` the :meth: `read_portfolio_data` and :meth: `read_cashrisks_data`.

    :param portfolio: info from portfolio file
    :param cashrisks: info from cashrisks file
    :return: portfolio data including risks per portfolio
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
    Find hedging ratio per client based on the output of :meth: `get_risks`.

    :param risk_portfolio: output from :meth: `get risks`
    :return: hedge ratio per client
    """
    hedge_ratio = risk_portfolio.groupby(by=['client'], dropna=True).apply(
        lambda x: abs(x[~x['scope'].isin(['Liabilities'])]['risk'].sum()
                      / x[x['scope'].isin(['Liabilities'])]['risk'].sum()))

    return hedge_ratio


def display(risk_portfolio, hedge_ratio):
    """
    Display risks per portfolio and display hedge ratios.

    :param risk_portfolio: output from :meth: `get_risks`
    :param hedge_ratio: output from :meth: `find_hedge_ratio`
    """
    print(risk_portfolio)
    print(hedge_ratio)


def main():
    """
    Main entry point of app.
    """
    portfolio = read_portfolio_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/portfolios.xlsx', header=0)
    cashrisks = read_cashrisks_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/cashrisks.csv', header=0)

    risk_portfolio = get_risks(portfolio, cashrisks)
    hedge_ratio = find_hedge_ratio(risk_portfolio)
    display(risk_portfolio, hedge_ratio)


if __name__ == '__main__':
    main()
