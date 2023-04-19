import random
import string


def get_char_id(length: int = 9) -> str:
    pool = string.ascii_letters + string.digits
    return "".join(random.choice(pool) for _ in range(length))
