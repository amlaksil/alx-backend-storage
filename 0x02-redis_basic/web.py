#!/usr/bin/env python3

"""
Module: web

This module provides the get_page function and the cache_result
decorator, which can be used to fetch the HTML content of a URL
and cache the results with a specified expiration time.
"""

from functools import wraps
import requests
import time

CACHE = {}


def cache_result(expiration_time):
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
        @wraps(func)
        def wrapper(url):
            """
            Retrieves the HTML content of a given URL and caches the result.

            Args:
                url (str): The URL to fetch the HTML content from.

            Returns:
                str: The HTML content of the URL.

            """
            if url in CACHE and time.time() - CACHE[url]['timestamp']\
               < expiration_time:
                # Return the cached content if it is still valid
                CACHE[url]['count'] += 1
                return CACHE[url]['content']

            # Retrieve the content from the URL
            response = func(url)

            # Cache the content along with the timestamp and count
            CACHE[url] = {
                'content': response, 'count': 1, 'timestamp': time.time()}

            return response

        return wrapper
    return decorator


@cache_result(10)
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
    return response.text
