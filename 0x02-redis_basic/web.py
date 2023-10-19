#!/usr/bin/env python3

"""
Module: web
"""

import requests
import functools
import time


def cache(expiration_time):
    """
    A decorator that caches the result of a function with a given
    expiration time.

    Args:
        expiration_time (int): The expiration time in seconds for
        the cached result.

    Returns:
        function: The decorated function.

    """
    def decorator(func):
        cached_results = {}

        @functools.wraps(func)
        def wrapper(url):
            """
            Retrieves the HTML content of a given URL and caches the result.

            Args:
                url (str): The URL to fetch the HTML content from.

            Returns:
                str: The HTML content of the URL.

            """
            if url in cached_results:
                result, timestamp = cached_results[url]
                current_time = time.time()
                if current_time - timestamp < expiration_time:
                    return result

            result = func(url)
            cached_results[url] = (result, time.time())
            return result

        return wrapper

    return decorator


@cache(expiration_time=10)
def get_page(url):
    """
    Retrieves the HTML content of a particular URL.

    The function makes an HTTP request to the specified URL and
    returns the HTML content.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.

    """
    response = requests.get(url)
    content = response.text

    return content
