#!/usr/bin/env python3
import aiosqlite
import asyncio


async def fetch_all_users():
    async with aiosqlite.connect('users.db') as cnx:
        async with cnx.execute("SELECT * FROM users;") as cursor:
            row = await cursor.fetchall()
            return row

async def fetch_older_users():
    async with aiosqlite.connect('users.db') as cnx:
        async with cnx.execute("SELECT * FROM users WHERE age > 40;") as cursor:
            row = await cursor.fetchall()
            return row

async def fetch_concurrently():
    result = await asyncio.gather(fetch_all_users(), fetch_older_users())
    return result

if __name__ == "__main__":
    print(asyncio.run(fetch_concurrently()))
