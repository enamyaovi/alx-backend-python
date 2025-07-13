#!/usr/bin/env python3
import aiosqlite
import asyncio


async def async_fetch_users():
    """
    Coroutine to fetch all users from users.db.
    """
    async with aiosqlite.connect('users.db') as cnx:
        async with cnx.execute("SELECT * FROM users;") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """
    Coroutine to fetch users older than 40 from users.db.
    """
    async with aiosqlite.connect('users.db') as cnx:
        async with cnx.execute("SELECT * FROM users WHERE age > 40;") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """
    Runs both user-fetching coroutines concurrently.
    Returns:
        list: [all_users, older_users]
    """
    return await asyncio.gather(async_fetch_users(), async_fetch_older_users())

def display_results(all_users, older_users):
    """
    Display results from both user queries.
    """
    print("\n All Users:")
    for user in all_users:
        print(user)

    print("\n Users Older Than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    display_results(all_users, older_users)
