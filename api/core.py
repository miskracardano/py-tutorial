from typing import Any


def parse_response(value: Any) -> dict[str, Any]:
    return {
        'Success': True,
        'Error': None,
        'Value': value
    }


def parse_error(error: str) -> dict[str, Any]:
    return {
        'Success': False,
        'Error': error,
        'Value': None
    }
