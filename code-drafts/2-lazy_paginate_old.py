#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('use alx_prodev;')
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(pagesize):

    pages = pagesize

    data = paginate_users(page_size=pages, offset= 0)

    if data[-1] is not None:
        yield data
        while True:
            offset += 1
            next_page = paginate_users(page_size=pages, offset=offset)
            if next_page[-1] is not None:
                yield next_page
            else:
                break
    