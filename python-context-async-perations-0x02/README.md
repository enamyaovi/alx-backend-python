# Creating Custom Class-Based Context Managers and Coroutines

This project explores how to build reusable Python tools using custom class-based context managers and asynchronous coroutines. It focuses on practical ways to work with both MySQL and SQLite databases, execute queries safely, and run tasks concurrently. The goal is to manage complexity while keeping things clean and testable.

The `DatabaseConnection` class is a simple context manager that handles MySQL connections. It takes care of connecting to the database, committing or rolling back transactions, and closing the connection automatically. It uses a helper to load secrets from a `.env` file and a decorator to handle any exceptions that might come up in `__enter__` or `__exit__`.

The `ExecuteQuery` class builds on top of that. It inherits from `DatabaseConnection` and adds logic to execute a single parameterized SQL query using a prepared statement. This makes the query safer and avoids SQL injection. Right now, it works for basic one-parameter queries, which is enough for the current project scope, but it can be improved later.

There's also an async version of this idea using SQLite and `aiosqlite`. I wrote two coroutine functions: one fetches all users, and the other filters users older than 40. Both run concurrently using `asyncio.gather`, and results are displayed separately for clarity. This part shows how asynchronous database access can be done cleanly without a lot of boilerplate.

```
alx-backend-python/
├── utils/
│   ├── context_manager.py      # Contains DatabaseConnection and ExecuteQuery
│   ├── seed.py                 # Provides config loading and decorators
├── python-context-async-perations-0x02/
│   ├── 0-databaseconnection.py # Example usage of DatabaseConnection
│   ├── 1-execute.py            # Example usage of ExecuteQuery
│   ├── 3-concurrent.py         # Async coroutines using aiosqlite
├── users.db                    # Sample SQLite database
├── db_secrets.env              # Environment file for MySQL credentials
```

This project requires Python 3.10 or later. You’ll also need `mysql-connector-python`, `aiosqlite`, and `python-dotenv` for managing secrets. All dependencies are listed in the `requirements.txt` file. Just run:

```bash
pip install -r requirements.txt
```

To test the MySQL connection manager or query executor, make sure you’re in the project root and run:

```bash
PYTHONPATH=. python3 python-context-async-perations-0x02/1-execute.py
```

For the async SQLite example:

```bash
python3 python-context-async-perations-0x02/3-concurrent.py
```

All exception handling is centralized through a custom decorator to keep things clean. Sensitive info like login credentials is handled via `.env` files. Everything is written with real-world reuse in mind but focused enough for learning and quick experimentation.

## License

This project is licensed for educational and non-commercial use. Feel free to adapt the code with appropriate credit.
