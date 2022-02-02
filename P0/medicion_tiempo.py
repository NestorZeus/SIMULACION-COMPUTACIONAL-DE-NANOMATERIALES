from random import randint
from time import time
import sys
desde = 1
hasta = 1000
menor = 15
mayor = 22
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
