import pandas as pd


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
