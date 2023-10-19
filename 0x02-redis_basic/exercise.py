#!/usr/bin/env python3

"""
Module: exercise

This module provides a Cache class for storing data in Redis with random keys.
"""
import redis
import uuid
import functools
from typing import Union, Callable, Optional, List


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called and
    stores the count in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # Use the qualified name of the method
        self._redis.incr(key)  # Increment the count for the method key
        return method(self, *args, **kwargs)

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

    def get_all_inputs(self, method_name: str) -> List[str]:
        """
        Retrieves all the input arguments for a given method from Redis.

        Args:
            method_name (str): The name of the method.

        Returns:
            List[str]: The list of input arguments.
        """
        input_key = method_name + ":inputs"
        return self._redis.lrange(input_key, 0, -1)

    def get_all_outputs(self, method_name: str) -> List[str]:
        """
        Retrieves all the output values for a given method from Redis.

        Args:
            method_name (str): The name of the method.

        Returns:
            List[str]: The list of output values.
        """
        output_key = method_name + ":outputs"
        return self._redis.lrange(output_key, 0, -1)


def replay(func):
    """
    Displays the history of calls for a particular function.

    Args:
        func: The function whose history of calls to display.
    """
    cache = Cache()
    method_name = func.__qualname__

    inputs = cache.get_all_inputs(method_name)
    outputs = cache.get_all_outputs(method_name)

    print(f"{method_name} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{method_name}{input_args.decode()} -> {output.decode()}")
