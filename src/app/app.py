import datetime as dt
import logging
import pandas as pd

import api.derivatives as derivatives_api
import api.fx as fx_api


def run_py_tutorial(file_path_xlsx: str, file_path_csv: str, yesterday: dt.date):
    """
    Imports and merges data from different sources, then prints the resulting DataFrame.

    Args:
        file_path_xlsx (str): The file path to the Excel file containing the main data.
        file_path_csv (str): The file path to the CSV file containing the cash risk data.
        yesterday (dt.date): The date object representing the 'yesterday' date for processing.
    """
    df = import_and_merge(data=file_path_xlsx, cashrisk=file_path_csv, derivatives="derivatives",
                          fx="fx", yesterday=yesterday)
    df.to_excel("portfolios.xlsx")
    hedge = calculate_hedge(df)
    hedge.to_excel("hedge_ratios.xlsx")


def main():
    """
    Main entry point of app.
    """
    run_date = dt.date.today()
    yesterday = run_date - dt.timedelta(days=1)

    file_path_xlsx = "C:/Users/m.boogaart/PycharmProjects/py-tutorial/resources/portfolios.xlsx"
    file_path_csv = "C:/Users/m.boogaart/PycharmProjects/py-tutorial/resources/cashrisks.csv"
    run_py_tutorial(file_path_xlsx=file_path_xlsx, file_path_csv=file_path_csv, yesterday=yesterday)


def import_file(file_path: str):
    """
    Imports data from an Excel or CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the file to import.

    Returns:
        pandas.DataFrame: The imported data.
    """
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, index_col=None)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, index_col=None)
        else:
            raise ValueError("Unsupported file format. Please provide an XLSX or CSV file.")
        return df
    except Exception as e:
        logging.error(f"An error occurred while importing the file: {e}")
        return pd.DataFrame()


def merge_df(portfolios: pd.DataFrame, add: pd.DataFrame) -> pd.DataFrame:
    """
    Merges two DataFrame objects on the 'portfolio' column using a left join.

    Args:
        portfolios (pd.DataFrame): The main DataFrame with portfolio information.
        add (pd.DataFrame): The DataFrame to be merged with the main DataFrame.

    Returns:
        pd.DataFrame: The merged DataFrame result of joining the two DataFrames on 'portfolio' column.
    """
    df_merged = pd.merge(portfolios, add, on='portfolio', how='left')
    return df_merged


def get_positions(api_module, yesterday: dt.date, api_name: str):
    """
    Fetches positions from a given API module.

    Args:
        api_module: The API module (derivatives or fx).
        yesterday: The date to get the positions for.
        api_name: The name of the API.

    Returns:
        pd.DataFrame: A DataFrame with the portfolio positions and risks.
    """
    portfolios = api_module.get_all_portfolios()
    portfolio_names = portfolios["Value"]
    risks = {portfolio: api_module.get_portfolio_risks(portfolio, yesterday) for portfolio in portfolio_names}
    portfolio_risks = {portfolio: data["Value"] for portfolio, data in risks.items()}
    df_risks = pd.DataFrame(list(portfolio_risks.items()), columns=["portfolio", api_name])
    return df_risks


def import_and_merge(data: str, cashrisk: str, derivatives: str, fx: str, yesterday: dt.date) -> pd.DataFrame:
    """
    Imports data from specified files and merges them.
    This function imports data from four different sources

    Args:
        data (str): Path to the main data file.
        cashrisk (str): Path to the cash risk data file.
        derivatives (str): Path to the derivatives data file.
        fx (str): Path to the fx data file.
        yesterday (dt.date): The date for which to retrieve positions in derivatives and fx.

    Returns:
        pd.DataFrame: The merged data frame, with NaN values filled with zero.
    """
    df_data = import_file(data)
    df_cashrisk = import_file(cashrisk)
    df_cashrisk.drop(columns=['id'], inplace=True)
    df_derivatives = get_positions(derivatives_api, yesterday, derivatives)
    df_fx = get_positions(fx_api, yesterday, fx)

    df = merge_df(df_data, df_cashrisk)
    df = merge_df(df, df_derivatives)
    df = merge_df(df, df_fx)
    df = df.fillna(0)
    return df


def calculate_hedge(df: pd.DataFrame):
    assets = df[df["scope"] != "Liabilities"]
    grouped_assets_sum = assets.groupby("client")[["size", "risk", "derivatives", "fx"]].sum()
    grouped_assets_sum["sum"] = grouped_assets_sum[["risk", "derivatives", "fx"]].sum(axis=1)

    liabilities = df[df["scope"] == "Liabilities"]
    grouped_liabilities_sum = liabilities.groupby("client")[["size", "risk"]].sum()
    grouped_liabilities_sum["sum"] = grouped_liabilities_sum["risk"]

    grouped_sum = grouped_assets_sum.join(grouped_liabilities_sum, lsuffix="_assets", rsuffix="_liabilities")
    grouped_sum["hedge"] = abs(grouped_sum["sum_assets"] / grouped_sum["sum_liabilities"])
    grouped_sum.sort_values(by="hedge", ascending=False, inplace=True)
    return grouped_sum


if __name__ == "__main__":
    main()
