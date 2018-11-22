import numpy as np

def simplify_list(lst):
    """
    Recursive function to simplify a nested list to the most basic form.
    The nested list can have unknown depth and unknown content.
    In case of a single value, it will return a single value.
    In case of a list with more values, it will return a simple list.

    :param lst: list to simplify
    :return: lowest level object
    """
    list_obj = [list, np.ndarray]

    # Check if current lst is a list or array. If not, return it
    if type(lst) not in list_obj:
        return lst
    # lst is a list, so check if there is something in it. If not, return None
    elif lst.size == 0:
        return None
    # lst is a list with something in it. Go down recursively
    else:
        return simplify_list(lst[0])
