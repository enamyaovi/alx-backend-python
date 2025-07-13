# ALX BackEnd Python Projects

Welcome to my ALX backend Python repository. This repo contains code from my learning journey with ALX, where I focused on backend web development using Python. It will grow as I complete more projects, and this README will evolve alongside it.

## 1. Introduction

This repository brings together multiple backend-focused Python projects I’ve worked on, emphasizing modularity, clean code, and database-driven design. The structure covers three core areas: generators, decorators, and asynchronous coroutines. Each directory represents hands-on practice with real backend concerns.

## 2. Generators

The `python-generators-0x00` directory covers how to use Python generators for memory-efficient data streaming. This includes streaming users row-by-row from a MySQL database, paginating results, and calculating aggregates like average age. Generators allow me to write functions that don’t load all data into memory at once, making things more scalable. The code here also includes consumer functions for filtering and aggregating streamed data.

## 3. Decorators

Inside `python-decorators-0x01`, I built custom decorators to reduce repetition in database code. These decorators log SQL queries to a file, inject database connections automatically, wrap functions in transactions, cache query results, and retry failed operations. Everything is designed to be modular and composable, so you can layer multiple decorators without messing with the logic inside the function.

## 4. Asynchronous Programming

The `python-context-async-perations-0x02` directory demonstrates simple asynchronous functions using `aiosqlite`. Here I tested how to run concurrent database queries using `async` and `await`. This shows how async code can help speed things up when making multiple IO-bound requests, especially with SQLite where concurrency needs careful handling.

## 5. Shared Utilities

There’s also a `utils` directory to hold shared logic across projects. This includes `seed.py`, which defines a custom `exception_handler` decorator and a function to load database secrets from a `.env` file. I used this so I wouldn’t have to rewrite the same code across all the generator and decorator projects.

Because some project folders use names with dashes (`-`), Python treats them as invalid packages. That made importing across folders tricky. To fix this, I added the shared logic to `utils` and recommended a workaround for imports.

## 6. Running the Projects

Due to the folder naming structure, please run scripts from the root of the repo using this pattern:

```bash
PYTHONPATH=. python3 path/to/script.py
```

This ensures Python can resolve imports correctly when using modules from `utils`.

## 7. Environment Configuration

Most database scripts expect a `.env` file containing DB secrets like user, password, host, and database name. The default filename is `db_secrets.env`, but you can override that in the call to `get_config_parameters()` if needed. Place the `.env` file in the same directory as your script or pass the correct path manually.

## 8. Closing Note

This repository represents my growing understanding of backend development with Python. Each section is self-contained but contributes to a larger toolkit for writing robust, efficient backend systems. Individual folders contain minimal README files, but this serves as the umbrella overview. More improvements and refactors will follow as the projects mature.
