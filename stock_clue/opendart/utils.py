"""This module provides utility functions for OpenDart API."""
import requests

from stock_clue.error import HttpError


def str_to_int(v: str) -> int:
    """Converts a string to an integer.

    Args:
        v (str): The string to be converted.

    Returns:
        int: The integer value of the string. If the string is "-", returns 0.
    """
    if not v or v == "-":
        return 0
    return int(v.replace(",", ""))


def str_to_float(v: str) -> float:
    """Converts a string to a float value.

    Args:
        v (str): The string to be converted.

    Returns:
        float: The float value of the input string.
    """
    if not v or v == "-":
        return 0.0

    return float(v.replace(",", ""))


def extract_file_name(response: requests.Response) -> str:
    """Extracts the file name from the response header's Content-Disposition field.

    Args:
        response (requests.Response): The response object from the request.

    Returns:
        str: The extracted file name.

    Raises:
        HttpError: If the filename is not found in the response header's Content-Disposition field.
    """
    content_disposition: str = response.headers["Content-Disposition"]
    index_filename = content_disposition.find("filename=")
    if index_filename == -1:
        raise HttpError(
            f"Can't find filename in response header. Content-Disposition: {content_disposition}"
        )
    file_name = content_disposition[index_filename + 9 :]
    return file_name
