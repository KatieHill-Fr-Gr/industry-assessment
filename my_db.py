from abc import ABC
# abc is essentially a documentation/convention here, it tells you that this class is meant to be subclassed, not used directly.
# You can use it with @abstractmethod for strict enforcement (i.e can't instantiate the base class)
# Or don't use it and just raise NotImplementedError if class skips a method - then it will fail only when the method is called


class MyDB(ABC):
    """
    `InMemoryDB` interface.
    """

    def __init__(self):
        self.db: dict[str, dict[str, dict[str, int]]] = {}
        # to add timestamp later { key { field: (value, timestamp) } } # * These design notes are useful for interviewers to see
        # or import dataclasses and create a Record class
        # versioned structure would be: field -> [(timestamp, value), (timestamp, value), ...], sorted by timestamp, then get() to access the latest version

     
    def set(self, timestamp: int, key: str, field: str, value: int) -> None:
        """
        Should insert a `field`-`value` pair to the record
        associated with `key`.
        If the `field` in the record already exists, replace the
        existing value with the specified `value`.
        If the record does not exist, a new one is created.
        """
        # TODO

        record = {
            "value" : value,
             "timestamp" : timestamp   
        } 

        self.db.setdefault(key, {})[field] = record


        # if key in self.db:
        #     self.db[key][field] = field
        # else:
        #     self.db[key] = {}
        #     self.db[key][field] = {
        #     "value" : value,
        #      "timestamp" : timestamp   
        # } 


    def compare_and_set(self, timestamp: int, key: str, field: str, expected_value: int, new_value: int) -> bool:
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
        if key not in self.db or field not in self.db[key]:
            return False
        
        if self.db[key][field]['value'] == expected_value:
          # self.db[key][field]['value'] = new_value
            # self.db[key][field]['timestamp'] = timestamp`
            self.db[key][field] = {
                "value" : new_value,
                "timestamp" : timestamp   
            } 
            return True
        return False


    def compare_and_delete(self, timestamp: int, key: str, field: str, expected_value: int) -> bool:
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
        if key not in self.db or field not in self.db[key]:
            return False
        
        if self.db[key][field]['value'] == expected_value:
            self.db[key].pop(field)
            return True
        return False

    def get(self, timestamp: int, key: str, field: str) -> int | None:
        """
        Should return the value contained within `field` of the
        record associated with `key`.
        If the record or the `field` does not exist, should return
        `None`.
        """
        # TODO
        if key not in self.db or field not in self.db[key]:
            return None
        
        return self.db[key][field]['value']
    
    
    def find_median(self):
        if not self.db: 
            return None

        # sorted_by_age = sorted(self.db.items(), key=lambda field: field["value"]) 

        sorted_by_age = sorted(
            field["value"]
            for key_data in self.db.values() # loops through the key-value pairs {"name": {"age": 20, "timestamp": 1600001 }}
            for field in key_data.values() # loops through the "values" in the key-values pairs, i.e the nested dict {"age": 20, "timestamp": 1600001 }
            )

        length = len(sorted_by_age)
        median_age = length // 2 

        if length % 2 == 1:
            return sorted_by_age[median_age] 
        else: 
            return sorted_by_age[median_age - 1] 
    

    
    
