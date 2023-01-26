from app.app import read_portfolio_data
from app.app import read_cashrisks_data
from app.app import get_risks
from pathlib import Path
import pandas as pd
import sys

root = Path(__file__).parent.parent  # Keep at top to add to add root dir to PYTHONPATH.
sys.path.append(str(root))  # Keep at top to add to add root dir to PYTHONPATH.

cash_test = Path('C:/Users/l.torn/PycharmProjects/py-tutorial/tests/test_files/cashrisks.csv')
port_test = Path('C:/Users/l.torn/PycharmProjects/py-tutorial/tests/test_files/portfolios.xlsx')

data_cash = {
    'id': [1, 2],
    'portfolio': ['PortfolioA5', 'PortfolioC3'],
    'risk': [-200, -170]
}

data_port = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'portfolio': ['PortfolioA1', 'PortfolioA2', 'PortfolioA5', 'PortfolioA6', 'PortfolioB1', 'PortfolioB3',
                  'PortfolioC2', 'PortfolioC3', 'PortfolioC4'],
    'client': ['ClientA', 'ClientA', 'ClientA', 'ClientA', 'ClientB', 'ClientB', 'ClientC', 'ClientC', 'ClientC'],
    'scope': ['CashBalance', 'FX', 'Liabilities', 'Exotics', 'CashBalance', 'Bonds', 'FixedIncome', 'Liabilities',
              'Hybrids'],
    'size': [2, 20, 100, 30, 10, 100, 100, 85, 10]
}

data_port_risks = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'portfolio': ['PortfolioA1', 'PortfolioA2', 'PortfolioA5', 'PortfolioA6', 'PortfolioB1', 'PortfolioB3',
                  'PortfolioC2', 'PortfolioC3', 'PortfolioC4'],
    'client': ['ClientA', 'ClientA', 'ClientA', 'ClientA', 'ClientB', 'ClientB', 'ClientC', 'ClientC', 'ClientC'],
    'scope': ['CashBalance', 'FX', 'Liabilities', 'Exotics', 'CashBalance', 'Bonds', 'FixedIncome', 'Liabilities',
              'Hybrids'],
    'size': [2, 20, 100, 30, 10, 100, 100, 85, 10],
    'risk': [float('NaN'), 20, -200, 60, -170, 135, 130, float('NaN'), 30]
}



def test_read_cashrisks_data():
    df_1 = read_cashrisks_data(cash_test, header=0)
    df_expected = pd.DataFrame(data_cash)
    assert len(df_1) == 2
    assert df_expected.equals(df_1)


def test_read_portfolio_data():
    df_1 = read_portfolio_data(port_test, header=0)
    df_expected = pd.DataFrame(data_port)
    assert len(df_1) == 9
    assert df_expected.equals(df_1)


def test_get_risks():
    test_risk_pf = get_risks(port_test, cash_test)
    df_expected = pd.DataFrame(data_port_risks)
    assert df_expected.equals(test_risk_pf)


