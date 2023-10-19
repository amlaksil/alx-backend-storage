#!/usr/bin/env python3

"""
Module: exercise

This module provides a Cache class for storing data in Redis with random keys.
"""
import redis
import uuid
import functools
from typing import Union, Callable, Optional


def count_calls(fn: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called and
    stores the count in Redis.

    Args:
        fn (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(fn)
    def wrapper(self, data):
        key = fn.__qualname__
        self._redis.incr(key)
        return fn(self, data)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for
    a function using Redis.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Store the input arguments in Redis
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(output_key, output)

        return output

    return wrapper


class Cache:
    """
    Cache class for storing data in Redis with random keys.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client.
    """

    def __init__(self):
        """Initializes the Cache object.

        Creates an instance of the Redis client and flushes the Redis
        instance using flushdb.
        """
        self._redis = redis.Redis()

        # Clear any existing data before starting
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in
            Redis.
        Returns:
            str: The randomly generated key under which the data is stored
            in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieves the value associated with the given key from Redis.

        Args:
            key (str): The key for which to retrieve the value from Redis.
            fn (Optional[Callable]): An optional callable function to
            convert the retrieved value.
        Returns:
            Any: The retrieved value from Redis, optionally converted
            using the provided function.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the value associated with the given key from Redis and
        converts it to a string.

        Args:
            key (str): The key for which to retrieve the value from Redis.

        Returns:
            Optional[str]: The retrieved value from Redis as a string, or
            None if the key does not exist.
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the value associated with the given key from Redis and
        converts it to an integer.

        Args:
            key (str): The key for which to retrieve the value from Redis.
        Returns:
            Optional[int]: The retrieved value from Redis as an integer, or
            None if the key does not exist.
        """
        return self.get(key, int)
