import random


def generate_password():
    e_id = ''.join(random.choice('0123456789ABCDEFG') for _ in range(12))
    return e_id
