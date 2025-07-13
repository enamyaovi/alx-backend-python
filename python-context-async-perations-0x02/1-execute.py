"""
Context manager for executing a parameterized query using a prepared cursor.
Builds on DatabaseConnection to manage the full query lifecycle cleanly.
"""

from utils import seed
from utils.context_manager import DatabaseConnection
from typing import Optional, Any

class ExecuteQuery(DatabaseConnection):
    """
    Context manager that inherits from DatabaseConnection to run a specific SQL query.

    - Takes a query and a parameter (basic single-parameter for now).
    - Uses a prepared statement for safety.
    - Not built for complex queries yet — fits current project needs.
    """

    def __init__(self, query: str, parameter: int) -> None:
        # Validate the query string
        if not isinstance(query, str) or not query.strip():
            raise ValueError("You must provide a non-empty SQL query string.")
        if not isinstance(parameter, int):
            raise ValueError("You must provide an integer parameter for the query.")

        self.query: str = query
        self.parameter: int = parameter
        self.result: Optional[list] = None
        self.config = seed.get_config_parameters()

        # Fallback to default DB if not in the config
        if not self.config['database']:
            self.config['database'] = 'alx_prodev'

    @seed.exception_handler
    def __enter__(self) -> list:  # type: ignore
        """
        Opens a connection, prepares a cursor, runs the query.

        Returns:
            list: The query result as a list of rows.
        """
        self.cursor = super().__enter__().cursor(prepared=True)  # type: ignore
        self.cursor.execute(self.query, (self.parameter,))
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
        """
        Closes the connection and handles commit/rollback.

        Returns:
            False to let exceptions bubble up.
        """
        return super().__exit__(exc_type, exc_value, traceback)  # type: ignore

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = 25
    with ExecuteQuery(query, param) as result:
        for row in result:
            print(row)
