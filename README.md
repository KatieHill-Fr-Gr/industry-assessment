# In-Memory Database - Coding Interview Practice

**Time:** 90 minutes max. Complete as many of the 4 levels as you can.

## Scenario

Your task is to implement a simplified in-memory database. Records are identified by a key, and each record holds field-value pairs (string field, integer value). All operations that should be supported are listed below.

Run the tests often to see how many pass. Each test is worth the same amount, and partial credit is granted for each test passed. Please read the tests for requirements and argument types.

## Implementation Tips

Read the question all the way through before you start coding, but implement the operations and complete the levels one by one, not all together, keeping in mind that you will need to refactor to support additional functionality. Please do not change the existing method signatures (new optional parameters are allowed where a level says so).

## Setup

```
db_practice/
    my_db.py            <- your solution goes here
    Pipfile
    tests/
        test_level_1.py
        test_level_2.py
        test_level_3.py
        test_level_4.py
```

```
pipenv install            # or: pip install timeout-decorator
python -m unittest discover -s tests -p "test_level_*.py"
```

Notes:
- `timeout-decorator` relies on signals, so it does not work on Windows (use WSL).
- Each test has a short time limit (0.4s), so avoid anything needlessly slow.
- Keep all state in `self.db`. The Level 1 tests print it.
- Test files must not be modified. Levels 2-4 only run once you have written code for them, so work through the levels in order.

## Task

Example of database structure:

```
[MyDB]
    key "employee1"
    +- age: 31
    +- score: 90
    key "employee2"
    +- age: 27
    +- score: 75
    key "employee3"
    +- score: 82
```

`(key, field)` and `(field, key)` are different records. For example `set(t, 'a', 'b', 1)` does not affect `get(t, 'b', 'a')`.

## Level 1 - Initial Design & Basic Functions

* `set(timestamp, key, field, value)`
   * Insert a field-value pair into the record associated with `key`.
   * If the field already exists, replace its value.
   * If the record does not exist, create it.
* `get(timestamp, key, field)`
   * Return the value of `field` in the record for `key`.
   * Return `None` if the record or the field does not exist.
* `compare_and_set(timestamp, key, field, expected_value, new_value)`
   * Update `field` to `new_value` only if its current value equals `expected_value`.
   * Return `True` if the field was updated, otherwise `False`.
   * If the key or the field does not exist, return `False` and do **not** create anything.
* `compare_and_delete(timestamp, key, field, expected_value)`
   * Remove `field` only if its current value equals `expected_value`.
   * Return `True` if the field was removed, otherwise `False`.
   * If the key or the field does not exist, return `False`.

## Level 2 - Data Structures & Data Processing

* `find_median()`
   * Return the median of **all values currently stored in the database**, across every record and every field.
   * If the number of values is odd, return the middle value.
   * If it is even, return the **lower** of the two middle values (so the result is always an `int` that is actually stored).
   * Return `None` if the database holds no values.

## Level 3 - Refactoring & Encapsulation

Fields now might have a specified time to live in the database. Extend the existing methods, which inherit all existing functionality, with an optional `ttl` parameter (a positive integer number of seconds). No `ttl` means the lifetime is infinite.

* `set(timestamp, key, field, value, ttl=None)`
   * The field is alive for `timestamp <= t < timestamp + ttl`. At `t = timestamp + ttl` it is already expired.
   * Setting an existing field replaces both its value **and** its ttl (omitting `ttl` makes it infinite again).
* `compare_and_set(timestamp, key, field, expected_value, new_value, ttl=None)`
   * On success, the field's ttl is reset to the provided `ttl` (or to infinite if omitted), counted from `timestamp`.
   * On failure nothing changes, including the existing ttl.
* `get`, `compare_and_set`, `compare_and_delete`
   * Expired fields behave as if they do not exist: `get` returns `None`, and the compare operations return `False`.
   * Operations are called with non-decreasing timestamps.
* `find_median(timestamp=None)`
   * Ignores expired fields when `timestamp` is given.
   * When `timestamp` is omitted, TTLs are not considered at all and every stored value counts (this keeps Levels 1 and 2 working unchanged).

## Level 4 - Extending Design & Functionality

* `rollback(timestamp)`
   * Restore the database to the state it had at `timestamp`.
   * Every operation with a timestamp **greater than** `timestamp` is discarded. Operations at exactly `timestamp` are kept.
   * All TTLs should be recalculated accordingly: a field that is alive at `timestamp` keeps the remaining lifetime it had at that moment, and a field that had already expired by then is gone.
   * Operations discarded by a rollback stay discarded, even if you later roll back to a timestamp after the first rollback.
   * After a rollback, further operations are called with timestamps greater than or equal to the rollback timestamp.
