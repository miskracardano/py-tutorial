from typing import TypeAlias

JsonDict: TypeAlias = dict[str, bool | int | str | list[str] | None]


def parse_response(value: int | list[str]) -> JsonDict:
    return {
        "Success": True,
        "Error": None,
        "Value": value
    }


def parse_error(error: str) -> JsonDict:
    return {
        "Success": False,
        "Error": error,
        "Value": None
    }
