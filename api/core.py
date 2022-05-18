from typing import Any, Dict


def parse_response(value: Any) -> Dict[str, Any]:
    return {
        'Success': True,
        'Error': None,
        'Value': value
    }


def parse_error(error: str) -> Dict[str, Any]:
    return {
        'Success': False,
        'Error': error,
        'Value': None
    }
