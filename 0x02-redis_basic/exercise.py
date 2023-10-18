#!/usr/bin/env python3

"""
Module: exercise

This module provides a Cache class for storing data in Redis with random keys.
"""
import redis
import uuid
from typing import Union


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
