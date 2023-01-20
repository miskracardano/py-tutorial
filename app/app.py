import sys  # Keep at top to add to add root dir to PYTHONPATH.
from pathlib import Path  # Keep at top to add to add root dir to PYTHONPATH.

root = Path(__file__).parent.parent  # Keep at top to add to add root dir to PYTHONPATH.
sys.path.append(str(root))  # Keep at top to add to add root dir to PYTHONPATH.

# from app.read_data import read_portfolio_data
# from app.read_data import read_cashrisks_data

import pandas as pd
from api.derivatives import get_all as get_all_der
from api.derivatives import get_portfolio as get_portfolio_der
from api.fx import get_all as get_all_fx
from api.fx import get_portfolio as get_portfolio_fx


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

def get_risks():
    """
    Get risks for all portfolios
    """
    show = get_portfolio_der(portfolio=get_all_der(), date=)
    return show



def main():
    """
    Main entry point of app.
    """
    read_portfolio_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/portfolios.xlsx', header=1)
    read_cashrisks_data('C:/Users/l.torn/PycharmProjects/py-tutorial/data/cashrisks.csv', header=1)
    get_risks()
    pass


if __name__ == '__main__':
    main()
