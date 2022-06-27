import api.fx as fx
import api.derivatives as der
import datetime as dt
from pathlib import Path
import os
import pandas as pd

this_dir = Path(os.path.dirname(os.path.abspath(__file__)))
parent_dir = this_dir.parent.absolute()


def load_client_data():
    """
    Loads all data from portfolios.xlsx. This represents the start of our report.
    """
    excel_dir = os.path.join(parent_dir, "data\portfolios.xlsx")
    client_df = pd.read_excel(excel_dir, sheet_name="Sheet1")
    client_df = client_df.copy()
    client_df.set_index('id', inplace=True)
    return client_df


def create_full_risk_table():
    """
    Based on the data from load_client_data, finds the risks associated with all portfolios.
    Sources to be used are the cashrisks.csv spreadsheet, and the two APIs.
    """
    risk_dict = _map_risk_data_for_all_pfs()
    risk_column = risk_dict.values()
    client_df = load_client_data()
    client_df['risk'] = risk_column
    return client_df


def calculate_hedge_ratio():
    """
    Per client, calculates the hedge ratio (risk of all liabilities over risks of all assets).
    """
    _df = create_full_risk_table()
    _df['weighted risk'] = _df['size'] * _df['risk']
    client_risk_all = {}
    for client in _df['client'].unique():
        client_df = _df.loc[_df['client'] == client]
        sum_liab_risk = 0
        sum_asset_risk = 0
        for pf in client_df['portfolio']:
            if client_df.loc[client_df['portfolio'] == pf, 'scope'].values[0] == 'Liabilities':
                sum_liab_risk += client_df.loc[client_df['portfolio'] == pf, 'weighted risk'].values[0]
            else:
                sum_asset_risk += client_df.loc[client_df['portfolio'] == pf, 'weighted risk'].values[0]

        if not sum_asset_risk == 0:
            total_client_risk = -sum_liab_risk/sum_asset_risk
            client_risk_all[client] = total_client_risk
        elif sum_asset_risk == 0:
            client_risk_all[client] = 'No asset exists'

    return client_risk_all


def _map_risk_data_for_all_pfs():
    """
    Maps risks for all portfolios in the table
    """
    pf_type_dict = _create_pf_type_dict()
    risk_dict = {}

    liab_risk_dict = _read_liability_risks()
    deri_risk_dict = _get_risk_api(derivatives=True)
    fx_risk_dict = _get_risk_api(derivatives=False)

    for pf, scope in pf_type_dict.items():
        if scope == 'CashBalance':
            risk_dict[pf] = 0

        elif scope == 'Liabilities':
            risk = liab_risk_dict[pf]
            risk_dict[pf] = risk

        elif scope == 'Bonds' or scope == 'FixedIncome' or scope == 'Exotics' or scope == 'Hybrids':
            risk = deri_risk_dict[pf]
            risk_dict[pf] = risk

        elif scope == 'FX':
            risk = fx_risk_dict[pf]
            risk_dict[pf] = risk

    return risk_dict


def _create_pf_type_dict():
    """
    Creates a dictionary that maps portfolio and its type/scope
    """
    client_df = load_client_data()
    pf_type_dict = dict(zip(client_df['portfolio'], client_df['scope']))
    return pf_type_dict


def _read_liability_risks():
    """
    Reads in risks for liability portfolios from cashrisks.csv file
    """
    csv_dir = os.path.join(parent_dir, "data\cashrisks.csv")
    my_df = pd.read_csv(csv_dir)
    liab_risk_dict = dict(zip(my_df['portfolio'], my_df['risk']))
    return liab_risk_dict


def _get_risk_api(derivatives: bool = True):
    """
    Gets risks of either derivatives assets or FX from api and maps the risks to the portfolios.
    """
    if derivatives:
        result = der.get_all()
    else:
        result = fx.get_all()
    all_pfs = result['Value']
    all_risk = []
    for pf in all_pfs:
        if derivatives:
            risk_result = der.get_portfolio(pf, dt.date.today())
        else:
            risk_result = fx.get_portfolio(pf, dt.date.today())
        risk = risk_result['Value']
        all_risk.append(risk)
    risk_dict = dict(zip(all_pfs, all_risk))
    return risk_dict
