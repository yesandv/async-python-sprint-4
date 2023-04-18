import random
import string


def get_char_id(length: int = 7) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))
