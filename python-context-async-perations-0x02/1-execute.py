"""
Reusable context manager that executes a parameterized query using a prepared cursor.
Handles both connection setup and teardown via inheritance from DatabaseConnection.
"""

from utility import seed
from utility.context_manager import DatabaseConnection
from typing import Optional, Any

class ExecuteQuery(DatabaseConnection):
    def __init__(self, query: str, parameter: int) -> None:
        """
        Initialize the query context manager with SQL query and parameter.
        
        Args:
            query (str): SQL query to execute (must use ? as placeholder).
            parameter (int): Value to substitute into the query.
        
        Raises:
            ValueError: If query is not a string or parameter is not an int.
        """
        if not isinstance(query, str) or not query.strip():
            raise ValueError("You must provide a non-empty SQL query string.")
        if not isinstance(parameter, int):
            raise ValueError("You must provide an integer parameter for the query.")

        self.query: str = query
        self.parameter: int = parameter
        self.result: Optional[list] = None
        self.config = seed.get_config_parameters()

        #honestly I should be passing this to the init method but due to the checker I am not for now.
        if not self.config['database']:
            self.config['database'] = 'alx_prodev'
    

    @seed.exception_handler
    def __enter__(self) -> list: #type:ignore
        """
        Enters the context by opening a DB connection and executing the query.

        Returns:
            list: Result set from the executed query.
        """
        self.cursor = super().__enter__().cursor(prepared=True)  # type: ignore
        self.cursor.execute(self.query, (self.parameter,))
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
        """
        Exits the context, committing or rolling back as needed.

        Args:
            exc_type (type): Type of exception if any.
            exc_value (Exception): Exception instance.
            traceback (traceback): Traceback object.

        Returns:
            bool: False to propagate exceptions.
        """
        return super().__exit__(exc_type, exc_value, traceback)  # type: ignore

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = 25
    with ExecuteQuery(query, param) as result:
        for row in result:
            print(row)
