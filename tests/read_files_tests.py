from app.app import read_portfolio_data
from app.app import read_cashrisks_data
from pathlib import Path
import pandas as pd

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
    'client': ['ClientA', 'ClientA', 'ClientA', 'ClientA', 'ClientB', 'ClientB', 'ClientC', 'ClientC' 'ClientC'],
    'scope': ['CashBalance', 'FX', 'Liabilities', 'Exotics', 'CashBalance', 'Bonds', 'FixedIncome', 'Liabilities',
              'Hybrids'],
    'size': [2, 20, 100, 30, 10, 100, 100, 85, 10]
}


def test_read_cashrisks_data():
    df_1 = read_cashrisks_data(cash_test, header=0)
    df_expected = pd.DataFrame(data_cash)
    assert len(df_1) == 2
    assert df_expected.equals(df_1)


def test_cashrisks_no_header():
    data_no_header = read_cashrisks_data(cash_test, header=None)
    data_expected = {
        0: ['id', '1', '2'],
        1: ['portfolio', 'PortfolioA5', 'PortfolioC3'],
        2: ['risk', '-200', '-170']
    }
    assert data_no_header == data_expected


def test_read_portfolio_data():
    df_1 = read_portfolio_data(port_test, header=0)
    df_expected = pd.DataFrame(data_port)
    assert len(df_1) == 9
    assert df_expected.equals(df_1)


def test_portfolio_no_header():
    data_no_header = read_portfolio_data(port_test, header=None)
    data_expected = {
        0: ['id', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        1: ['portfolio', 'PortfolioA1', 'PortfolioA2', 'PortfolioA5', 'PortfolioA6', 'PortfolioB1', 'PortfolioB3',
            'PortfolioC2', 'PortfolioC3', 'PortfolioC4'],
        2: ['client', 'ClientA', 'ClientA', 'ClientA', 'ClientA', 'ClientB', 'ClientB', 'ClientC', 'ClientC' 'ClientC'],
        3: ['scope', 'CashBalance', 'FX', 'Liabilities', 'Exotics', 'CashBalance', 'Bonds', 'FixedIncome',
            'Liabilities', 'Hybrids'],
        4: ['size', '2', '20', '100', '30', '10', '100', '100', '85', '10']
    }
    assert data_no_header == data_expected
