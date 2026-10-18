from abc import ABC


class MyDB(ABC):
    """
    db interface
    """

    def __init__(self):
        # Keep all state in self.db (the Level 1 tests print it).
        self.db = {}

    def set(self, timestamp: int, key: str, field: str, value: int) -> None:
        """
        Should insert a `field`-`value` pair to the record
        associated with `key`.
        If the `field` in the record already exists, replace the
        existing value with the specified `value`.
        If the record does not exist, a new one is created.
        """
        # TODO
        pass

    def compare_and_set(self, timestamp: int, key: str, field: str,
                        expected_value: int, new_value: int) -> bool:
        """
        Should update the value of `field` in the record associated
        with `key` to `new_value` if the current value equals
        `expected_value`.
        If `expected_value` does not match the current value, or
        either `key` or `field` does not exist, this operation is
        ignored.
        This operation should return `True` if the `field` was
        updated and `False` otherwise.
        """
        # TODO
        pass

    def compare_and_delete(self, timestamp: int, key: str, field: str,
                           expected_value: int) -> bool:
        """
        Should remove the field `field` in the record associated
        with `key` if the previous value equals `expected_value`.
        If `expected_value` does not match the current value, or
        either `key` or `field` does not exist, this operation is
        ignored.
        This operation should return `True` if the `field` was
        removed and `False` otherwise.
        """
        # TODO
        pass

    def get(self, timestamp: int, key: str, field: str) -> int | None:
        """
        Should return the value contained within `field` of the
        record associated with `key`.
        If the record or the `field` does not exist, should return
        `None`.
        """
        # TODO
        pass

    def find_median(self) -> int | None:
        """
        Should return the median of all values currently stored in
        the database, across every record and field.
        For an even number of values, return the lower of the two
        middle values.
        If the database holds no values, should return `None`.
        """
        # TODO
        pass
        
    

    
    
