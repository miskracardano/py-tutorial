import sys                          # Keep at top to add to add root dir to PYTHONPATH.
from pathlib import Path            # Keep at top to add to add root dir to PYTHONPATH.

root = Path(__file__).parent.parent # Keep at top to add to add root dir to PYTHONPATH.
sys.path.append(str(root))          # Keep at top to add to add root dir to PYTHONPATH.

import pandas as pd

def load_portfolio_data(file: [str], header: [int]):
    """
    Load data portfolios
    """
    portfolios = pd.read_excel(file, header = header)

    return portfolios



def main():
    """
    Main entry point of app.
    """
    load_portfolio_data('C:\Users\l.torn\PycharmProjects\py-tutorial\data\portfolios.xlsx', header = 1)
    pass


if __name__ == '__main__':
    main()
