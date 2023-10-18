#!/usr/bin/env python3

"""
Module: 8-all

This module contains a function called 'list_all' that
lists all documents in a collection.
"""


def list_all(mongo_collection):
    """Lists all documents in a collection.

    Args:
        mongo_collection (object): pymongo collection object.
    Return:
        list: List of documents or empty list if no document in the collection.
    """
    doc_list = []
    for doc in mongo_collection.find():
        doc_list.append(doc)

    return doc_list


if __name__ == "__main__":
    list_all(mongo_collection)
