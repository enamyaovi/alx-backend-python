
# MySQL Generator Project

## Overview

This project demonstrates how to use Python generators to interact with a MySQL database efficiently. By streaming data row-by-row, we minimize memory usage while performing operations like pagination, batch processing, and computing aggregate values.

## Features

This project showcases several generator-based approaches to interacting with a database. One function yields each user row from a table individually, another fetches and streams data in fixed-size batches, and yet another yields specific fields such as user ages.

Paired with consumer functions, these generators allow for efficient filtering and aggregation tasks, like selecting users above a certain age or calculating the average age. These operations are done incrementally, ensuring that the entire dataset is never loaded into memory.

Exception handling is streamlined using a reusable decorator applied across key functions. This approach helps maintain readability and consistency when managing errors during database operations.

## Technologies Used

* Python 3.10+
* MySQL
* mysql-connector-python
* dotenv (for managing credentials)

