from algorithms import *
#from random import randint
from time import time
from CatalanSquares import *



def test_coolex(n):
    start = time()
    for i, c in enumerate(coolex(n)):
        pass
    time_diff = time() - start
    return time_diff

def test_coolex2(n):
    start = time()
    for i, c in enumerate(coolex2(n)):
        pass
    time_diff = time() - start
    return time_diff

def test_dyck_gen(n):
    start = time()
    for i, c in enumerate(dyck_gen(n)):
        pass
    time_diff = time() - start
    return time_diff

def test_catalan_squares(n):
    cs = CatalanSquare(list(range(1,n+1)))
    start = time()
    try:
        while True:
            cs = cs.next()
    except AttributeError:
        pass
    time_diff = time() - start
    return time_diff

def test(n=[6, 7, 8, 9, 10]):

    for i in n:
        print("coolex", i, test_coolex(i))
        print("coolex2", i, test_coolex2(i))
        print("dyck_gen", i, test_dyck_gen(i))
        print("catalan_squares", i, test_catalan_squares(i))

if __name__=="__main__":
    test()
    #print(test_catalan_squares(3))
    #test_coolex(3)