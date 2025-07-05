#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination


try:
    page_count = 0
    total_rows = 0
    for page in lazy_paginator(100):
        page_count += 1
        for user in page:
            print(user)
            total_rows += 1
    
    per_page = total_rows/page_count
    print(f"{page_count} pages with {round(per_page):.0f} entries per page")

except BrokenPipeError:
    sys.stderr.close()