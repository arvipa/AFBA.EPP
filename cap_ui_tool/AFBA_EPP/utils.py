"""
utility and helper functions.
"""


def add_product_attr(data, key_pr, attr_tup):
    """
    It creates an empty dictionary of product with attributes and its empty values.
    :param data: Dictionary in which product attribute and its default values to be created.
    :param key_pr: Product name string.
    :param attr_tup: Product attributes tuple.
    :return: It creates Product attributes and its empty values in main data dictionary.
    """
    for attr in attr_tup:
        data[0].setdefault(key_pr, {}).update({attr: None})
