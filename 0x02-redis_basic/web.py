#!/usr/bin/env python3

"""
Module: web

This module provides the get_page function and the cache_result
decorator, which can be used to fetch the HTML content of a URL
and cache the results with a specified expiration time.
"""

from functools import wraps
import requests
import redis
import time

# Initialize Redis client
redis_client = redis.Redis()


def cache_result(expiration_time: int):
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
            # Generate a unique cache key for the URL
            cache_key = f"cache:{url}"

            # Check if the URL is in Redis cache and the cache is still valid
            if redis_client.exists(cache_key) and\
               time.time() - float(redis_client.hget(
                   cache_key, 'timestamp')) < expiration_time:
                # Increase the cache hit count
                redis_client.hincrby(cache_key, 'count', 1)
                # Return the cached content
                return redis_client.hget(cache_key, 'content').decode('utf-8')

            # Retrieve the content from the URL
            response = func(url)

            # Cache the content in Redis along with the timestamp and count
            redis_client.hset(cache_key, 'content', response)
            redis_client.hincrby(cache_key, 'count', 1)
            redis_client.hset(cache_key, 'timestamp', time.time())

            # Set the expiration time for the cache key
            redis_client.expire(cache_key, expiration_time)

            return response

        return wrapper
    return decorator


@cache_result(10)
def get_page(url: str) -> str:
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
