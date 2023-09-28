import random
import string

from django.contrib.contenttypes.models import ContentType


def random_password():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str