import multiprocessing
from functools import partial
from contextlib import contextmanager

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def merge_names(a, b,c):
    if c==1:
        return '{} & {}'.format(a, b)
    else:
        return '{} & {}'.format(b, a)
    
if __name__ == '__main__':
    names = ['Brown', 'Wilson', 'Bartlett', 'Rivera', 'Molloy', 'Opie']
    with poolcontext(processes=3) as pool:
        results = pool.map(partial(merge_names, b='lllllll',c=2), names)
    print(results)