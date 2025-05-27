# from copy import deepcopy  # might need, but not right now
import random

  # credit to me (I MADE THIS)
from .userComparable import Item

# https://github.com/PunkChameleon/ford-johnson-merge-insertion-sort/blob/master/fjmi.py
from .fjmi import merge_insertion_sort


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
            random.shuffle(things)

        self._collection = things
        self._wrapped = [Item(thing) for thing in things]

    def neighbor_compare(self):
        """ // TODO: make this into something actually useful. and fix minimal_compare docstring
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

        # utilize someone else's sorting algorithm,
        # but sorting based on wrapped Items()
        # so that it will use the overriden > operator to ask for user input.
        self._rememberWrappedIndices()
        self._wrapped[:] = merge_insertion_sort(self._wrapped)
        
        self._updateCollectionBasedOnWrappedIndicesPermutation()  # updates order of self._collection, based on the sort of _wrapped

        return self._collection
    
    def _rememberWrappedIndices(self):
        for i in range(len(self._wrapped)):
            self._wrapped[i].setIndex(i)

    def _updateCollectionBasedOnWrappedIndicesPermutation(self):
        old_indices = [w.getIndex() for w in self._wrapped]
        self._collection[:] = [self._collection[i] for i in old_indices]
    
    def _swap(self, index1, index2):
        self._collection[index1], self._collection[index2] = self._collection[index2], self._collection[index1]
        self._wrapped[index1], self._wrapped[index2] = self._wrapped[index2], self._wrapped[index1]

    def __repr__(self):
        return repr(self._collection)

    def __str__(self):
        return str(self._collection)


if __name__ == '__main__':
    print('Testing comparer.py\'s Comparer() class:')
    lst = ['thai', 'sushi', 'pizza', 'mexican', 'calamari']
    c = Comparer(lst)
    c.minimal_compare()
    print(c)

    print('\nfinished merge-insortion compare, onto neighbor compare:\n')
    c.neighbor_compare()
    print(c)
