#!/usr/bin/env python3

"""
Module: 11-schools_by_topic

This module contains a function called 'schools_by_topic' that
returns the list of school having a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    '''Retrieve a list of schools that have a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
            collection object.
        topic (str): The topic to search for.

    Returns:
        list: A list of schools that have the specified topic.

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

        # Call the function to retrieve schools by topic
        schools = schools_by_topic(collection, "Math")

        # Print the list of schools
        for school in schools:
            print(school)
    '''
    result = mongo_collection.find({"topics": topic})
    return list(result)


if __name__ == "__main__":
    schools_by_topic(mongo_collection, topic)
