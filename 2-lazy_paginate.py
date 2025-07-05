#!/usr/bin/python3
seed = __import__('seed2')


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
    current_page = []

    data = paginate_users(page_size=pages, offset= 0)

    for item in data:
        current_page.append(item)
        if len(current_page) == pagesize:
            yield current_page
            current_page = []
    if current_page:
        yield current_page
    