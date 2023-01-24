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

    return cashrisks


def get_risks(portfolio):
    """
    Get risks for all portfolios
    """
    risk_value_der = [{x: get_portfolio_der(x, date.today())['Value']} for x in (set(pd.Series(get_all_der()['Value'])) & set(portfolio.portfolio))]
    risk_value_fx = [{x: get_portfolio_fx(x, date.today())['Value']} for x in (set(pd.Series(get_all_fx()['Value'])) & set(portfolio.portfolio))]

    return risk_value_der, risk_value_fx

def add_risks(portfolio, risk_value_der, risk_value_fx, cashrisks):
    """
    Add obtained risk info to portfolios dataframe
    """
    portfolio['risk'] =

    return portfolio


def main():
    """
    Main entry point of app.
    """
    portfolio = read_portfolio_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/portfolios.xlsx', header=0)
    cashrisks = read_cashrisks_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/cashrisks.csv', header=0)

    risk_value_der, risk_value_fx = get_risks(portfolio)
    add_risks(portfolio, risk_value_der, risk_value_fx, cashrisks)



    print(portfolio, cashrisks, risk_value_der, risk_value_fx)

    pass


if __name__ == '__main__':
    main()
