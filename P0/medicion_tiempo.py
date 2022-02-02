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
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

for k in range(menor, mayor):
    n = 2**k
    lista = [ randint(desde, hasta) for i in range(n)]
    antes = time()
    lista.sort()
    despues = time()
    diferencia = despues - antes
    print('ordenar', n, 'elementos toma', diferencia, 'segundos ',
          '\n y en conjunto pesan', get_size(lista), 'bytes')
print('bye')
