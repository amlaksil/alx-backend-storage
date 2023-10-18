#!/usr/bin/env python3

"""
Module: 8-all

This module contains a function called 'insert_school' that
inserts a new document in the collection.
"""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document into a MongoDB collection based on
    keyword arguments.

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
            collection object.
        **kwargs: Keyword arguments representing the fields and values
            of the new document.
    Returns:
        str: The _id of the newly inserted document.

    Raises:
        pymongo.errors.PyMongoError: If any error occurs during the
        database operation.

    Example:
        from pymongo import MongoClient

        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017")

        # Select the database and collection
        db = client["your_database_name"]
        collection = db["school"]

        # Call the function to insert a new document
        new_document_id = insert_school(
        collection, name="Holberton School", address="123 Main St")

        # Print the _id of the newly inserted document
        print(new_document_id)
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id


if __name__ == "__main__":
    insert_school(mongo_collection, **kwargs)
