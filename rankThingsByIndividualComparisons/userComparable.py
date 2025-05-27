from helpers import is_mutable, getch ,CONFIRMATIONS, TO_STRIP


# important thing:
class Item():
    def __init__(self, item, caching=True):
        """
        Args:
            item (any type): the item that you preserve but essentially modify the comparisons of.
                             it's accessible through item(). should not be set (but technically could be using ._item).
                             Hopefully, if item is mutable, it should NOT be edited if caching=True, otherwise caching could be incorrect.
            caching (bool, optional): determines whether comparisons that are equivalent are repeatedly asked to the user. Defaults to True.
        """
        self._item = item
            
        self._cache = {}
        self.caching = caching
        if caching and is_mutable(item):  # might not catch everything...
            raise ValueError("Item should NOT be mutable if caching is enabled.")
        
        self._index = None

    def setIndex(self, i):
        """Sets the _index field to remember its place in a container"""
        self._index = i

    def getIndex(self):
        return self._index

    def __lt__(self, other):
        if not isinstance(other, Item):
            return NotImplemented  # signal to Python that comparison with unknown types isn’t implemented

        if self.caching and (cached_info := self._cache.get(other)):
            if cached_info == 'lt':
                return True
            if cached_info in {'ge', 'eq', 'gt'}:
                return False

        print(end=f'Is "{str(other)}" better than "{str(self)}" (y/[n])? ', flush=True)
        user_input = getch()
        print(repr(user_input), flush=True)
        result = user_input.strip(TO_STRIP).lower() in CONFIRMATIONS  # with getch this is uncessary, but will still work——checks for 'y'

        if self.caching:
            if not other.caching:
                raise ValueError("All Item instances compared with each other must share the same 'caching' setting.")
            if result:
                self._cache[other] = 'lt'
                other._cache[self] = 'gt'
            else:
                if cached_info == 'le':
                    assert(other._cache[self] == 'ge')
                    self._cache[other] = 'eq'
                    other._cache[self] = 'eq'
                elif cached_info == 'ne':
                    assert(other._cache[self] == 'ne')
                    self._cache[other] = 'gt'
                    other._cache[self] = 'lt'
                else:
                    self._cache[other] = 'ge'
                    other._cache[self] = 'le'
        elif other.caching:  # other.caching enabled but self.caching not
            raise ValueError("All Item instances compared with each other must share the same 'caching' setting.")
        
        return result

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented

        if self.caching and (cached_info := self._cache.get(other)):
            if cached_info == 'eq':
                return True
            if cached_info in {'ne', 'lt', 'gt'}:
                return False
        
        comparison = input(f'Is "{str(other)}" roughly equivalent to "{str(self)}" (y/[n])? ')
        result = comparison.strip(TO_STRIP).lower() in CONFIRMATIONS

        if self.caching:
            if not other.caching:
                raise ValueError("All userComparable Items of the same category should have the same value for caching")
            if result:
                self._cache[other] = 'eq'
                other._cache[self] = 'eq'
            else:
                if cached_info == 'le':
                    assert(other._cache[self] == 'ge')
                    self._cache[other] = 'lt'
                    other._cache[self] = 'gt'
                elif cached_info == 'ge':
                    assert(other._cache[self] == 'le')
                    self._cache[other] = 'gt'
                    other._cache[self] = 'lt'
                else:
                    self._cache[other] = 'ne'
                    other._cache[self] = 'ne'
        elif other.caching:  # other.caching enabled but self.caching not
            raise ValueError("All userComparable Items of the same category should have the same value for caching")
        
        return result

    def item(self):
        return self._item

    # Below are defined in terms of the above comparisons functions, so that the caching logic is easier
    
    def __le__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        
        if self.caching and (cached_info := self._cache.get(other)):
            if cached_info in {'le', 'eq', 'lt'}:
                return True
            if cached_info == 'gt':
                return False
            # technically, 'lt' and 'gt' cases would be handled by below fine, but might as well be rigorous.
            # in following functions, all cases are handled by the returning function, so no caching logic.
        
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        
        return not self.__le__(other)
    
    def __ge__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        
        return not self.__lt__(other)
    
    def __ne__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        
        return not self.__eq__(other)
    
    # other stuff necessary for this to work:
    def __hash__(self):
        return hash(self.item())
    
    def __repr__(self):
        return repr(self.item())
    
    def __str__(self):
        return str(self.item())


if __name__ == '__main__':
    print('Testing userComparable\'s Item() class:')
    ch = Item("chicken")
    pork = Item("pork")
    print(ch > pork)
    print(ch < pork)
    print(ch == pork)


    print("NEW ITEMS")
    ch = Item("chicken")
    pork = Item("pork")
    print(ch < pork)
    print(ch == pork)
    print(ch > pork)

    mutable_input = [_ for _ in range(0)]  # size 0 failed before, now it works
    newItem = Item(mutable_input)  # expect an error
