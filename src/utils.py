'''
This file contains utility functions that are used in the project.
'''
# pylint: disable=C0115,C0116,C0301

import time


def write_error_log(error):
    current_unix_time = int(time.time())
    with open(f'error_{current_unix_time}.log', 'a', encoding='utf-8') as f:
        f.write(str(error) + '\n')
