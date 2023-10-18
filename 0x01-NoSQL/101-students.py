#!/usr/bin/env python3

"""
Module: 10-update_topics

This module contains a function called 'top_students' that
returns all students sorted by average score.
"""


def top_students(mongo_collection):
    """Retrieve all students sorted by average score in descending order.

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
        collection object.

    Returns:
        list: A list of students sorted by average score in
        descending order.

    Raises:
        pymongo.errors.PyMongoError: If any error occurs during
        the database operation.

    Example:
        from pymongo import MongoClient

        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017")

        # Select the database and collection
        db = client["your_database_name"]
        collection = db["students"]

        # Call the function to retrieve top students by average score
        top_students_list = top_students(collection)

        # Print the list of top students
        for student in top_students_list:
            print(student)
    """
    students = mongo_collection.aggregate(
            [{"$unwind": "$topics"},
             {"$group": {
                 "_id": "$_id",
                 "name": {"$first": "$name"},
                 "averageScore": {"$avg": "$topics.score"}
                 }},
             {"$project": {
                 "_id": 1,
                 "name": 1,
                 "averageScore": 1
                 }},
             {"$sort": {"averageScore": -1}}]
    )
    return list(students)


if __name__ == "__main__":
    top_students(mongo_collection)
