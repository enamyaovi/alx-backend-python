# Custom Decorators for Database Query Functions

This project showcases a set of reusable Python decorators designed to streamline and enhance database operations. The focus is on adding behavior such as query logging, connection injection, and automatic retrying without cluttering the core logic of your functions.

## Key Decorators

### 1. `@log_queries`

Automatically logs any SQL query passed to a function. It uses Python's `inspect` module to access function arguments and a configured `logging` handler to write logs to `app.log`.

**Used for:**

* Auditing which queries were executed
* Debugging during development

### 2. `@with_db_connection`

Injects a SQLite database connection into the target function. It uses `inspect` to check if a `conn` argument was passed — if not, it creates one. Also handles basic type enforcement and error logging.

**Used for:**

* Avoiding repetitive connection boilerplate
* Ensuring your function always has a valid DB connection

### 3. `@retry_on_failure(retries=3, delay=1)`

Retries a function when it raises a `sqlite3.Error`. You can configure how many times to retry and how long to wait between attempts.

**Used for:**

* Preventing app crashes on transient database issues
* Adding resilience to DB calls without extra logic in your function

## Example Use Case

```python
@with_db_connection
@log_queries
@retry_on_failure(retries=2, delay=1)
def fetch_user_by_email(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()
```

This function:

* Connects to the database (if no connection is passed)
* Logs the SQL query
* Retries on failure up to 2 times

## How to Run

Ensure your SQLite `users.db` exists with a `users` table, and run any of the decorator example files like:

```bash
python3 0-log_queries.py
```

---

These decorators aim to make your code modular, readable, and safer without giving up transparency or control.
