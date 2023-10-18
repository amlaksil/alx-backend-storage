#!/usr/bin/env python3

"""
Module: 10-update_topics

This module contains a function called 'update_topics' that
changes all topics of a school document based on the name.
"""


def update_topics(mongo_collection, name, topics):
    '''Update the topics of a school document based on the name.

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
            collection object.
        name (str): The name of the school to update.
        topics (list): The list of topics approached in the school.

    Returns:
        int: The number of documents updated.

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

        # Call the function to update topics
        num_up = update_topics(
            collection, "Holberton School",
            ["Math", "Science", "Computer Science"])

        # Print the number of documents updated
        print(num_up)
    '''
    result = mongo_collection.update_many(
        {"name": name}, {"$set": {"topics": topics}})

    return result.modified_count


if __name__ == "__main__":
    update_topics(mongo_collection, name, topics)
