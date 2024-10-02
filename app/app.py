import sys                          # Keep at top to add to add root dir to PYTHONPATH.
from pathlib import Path            # Keep at top to add to add root dir to PYTHONPATH.

root = Path(__file__).parent.parent # Keep at top to add to add root dir to PYTHONPATH.
sys.path.append(str(root))          # Keep at top to add to add root dir to PYTHONPATH.


def main():
    """
    Main entry point of app.
    """
    pass


if __name__ == "__main__":
    main()
