import datetime as dt
import pandas as pd
import pytest

from src.app.app import (
    import_file, merge_df, get_positions, import_and_merge, calculate_hedge
)


def test_import_file_excel(mocker):
    mock_read_excel = mocker.patch("src.app.app.pd.read_excel")
    mock_read_excel.return_value = pd.DataFrame({"A": [1, 2]})

    result = import_file("test.xlsx")

    mock_read_excel.assert_called_once_with("test.xlsx", index_col=None)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "A" in result.columns


def test_import_file_csv(mocker):
    mock_read_csv = mocker.patch("src.app.app.pd.read_csv")
    mock_read_csv.return_value = pd.DataFrame({"B": [3, 4]})

    result = import_file("test.csv")

    mock_read_csv.assert_called_once_with("test.csv", index_col=None)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "B" in result.columns


def test_merge_df():
    df1 = pd.DataFrame({"portfolio": ["A", "B"], "value1": [1, 2]})
    df2 = pd.DataFrame({"portfolio": ["A", "C"], "value2": [3, 4]})

    result = merge_df(df1, df2)

    expected = pd.DataFrame({"portfolio": ["A", "B"], "value1": [1, 2], "value2": [3, None]})
    pd.testing.assert_frame_equal(result, expected)


def test_get_positions(mocker):
    mock_api_module = mocker.patch("src.app.app.derivatives_api")
    mock_api_module.get_all_portfolios.return_value = pd.DataFrame({"Value": ["A", "B"]})
    mock_api_module.get_portfolio_risks.side_effect = lambda portfolio, date: {"Value": 10 if portfolio == "A" else 20}

    result = get_positions(mock_api_module, dt.date(2023, 1, 1), "derivatives")

    expected = pd.DataFrame({"portfolio": ["A", "B"], "derivatives": [10, 20]})
    pd.testing.assert_frame_equal(result, expected)


def test_import_and_merge(mocker):
    mock_import_file = mocker.patch("src.app.app.import_file")
    mock_import_file.side_effect = [
        pd.DataFrame({"portfolio": ["A", "B"], "value 1": [1, 2]}),
        pd.DataFrame({"portfolio": ["A", "C"], "id": [3, 4]})
    ]
    mock_get_positions = mocker.patch("src.app.app.get_positions")
    mock_get_positions.side_effect = [
        pd.DataFrame({"portfolio": ["A", "B"], "derivatives": [5, 6]}),
        pd.DataFrame({"portfolio": ["A", "B"], "fx": [7, 8]})
    ]

    result = import_and_merge("data.xlsx", "cashrisk.csv", "derivatives", "fx", dt.date(2023, 1, 1))

    expected = pd.DataFrame({
        "portfolio": ["A", "B"],
        "value 1": [1, 2],
        "derivatives": [5, 6],
        "fx": [7, 8]
    }).fillna(0)
    pd.testing.assert_frame_equal(result, expected)


def test_calculate_hedge():
    df = pd.DataFrame({
        "client": ["X", "Y", "X", "Y"],
        "scope": ["FX", "Bonds", "Liabilities", "Liabilities"],
        "size":         [100, 200, 150, 250],
        "risk":         [0, 0, -50, -50],
        "derivatives":  [0, 150, 0, 0],
        "fx":           [100, 0, 0, 0]
    })

    result = calculate_hedge(df)

    expected = pd.DataFrame({
        "size_assets": [100, 200],
        "risk_assets": [0, 0],
        "derivatives": [0, 150],
        "fx": [100, 0],
        "sum_assets": [100, 150],
        "size_liabilities": [150, 250],
        "risk_liabilities": [-50, -50],
        "sum_liabilities": [-50, -50],
        "hedge": [2.0, 3.0]
    }, index=["X", "Y"]).sort_values(by="hedge", ascending=False)
    expected.index.name = 'client'
    pd.testing.assert_frame_equal(result, expected)
