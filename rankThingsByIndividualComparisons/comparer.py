from copy import deepcopy
import random

from userComparable import Item


class Comparer():
    """
    you pass in a collections of things you want to rank via individual comparisons,
    then call minimal_compare to create a ranking

    if you want to fine tune further, you can call neighbor_compare which will change ranks by at most 1 by doing n-1 comparisons
    """
    def __init__(self, things: list, randomize=False):
        """
        Args:
            things (list): items that will be ranked
            randomize (bool, optional): _description_. Defaults to False.
        """
        if (type(things) != list):
            things = list(things)
        
        if randomize:
            random.shuffle(things, inplace=False)

        self._collection = things
        self._wrapped = [Item(thing) for thing in things]

    def neighbor_compare(self):
        """
        compares each element to the one succeeding it, swapping if necessary
        swaps so that the best item will be first
        not the best comparer, but good for fine tuning when most wouldn't be off by much more than 1.

        updates list you passed into Comparer object, but also returns the list (in case you didn't pass in a list)
        """
        for i in range(len(self._collection) - 1):
            if self._wrapped[i] < self._wrapped[i + 1]:
                self._swap(i, i+1)
        
        return self._collection
    
    def minimal_compare(self):
        """
        The minimum necessary number of comparisons to accurately rank a list

        updates list you passed into Comparer object, but also returns the list (in case you didn't pass in a list)
        """

        sorted_section = {}  # type {item: float} --> {item: temp ranking}
        cpy = deepcopy(self._collection)  # definitely a list on the outside, unless someone manually changed it (please don't)
        wrap_cpy = deepcopy(self._wrapped)

        first = cpy.pop()
        second = cpy.pop()
        
        while cpy:
            pass

        return self._collection
    
    def _swap(self, index1, index2):
        self._collection[index1], self._collection[index2] = self._collection[index2], self._collection[index1]
        self.wrapped[index1], self.wrapped[index2] = self.wrapped[index2], self.wrapped[index1]
        