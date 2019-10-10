import multiprocessing
import timeit


start_time = timeit.default_timer()

d1 = dict( (i,tuple([i*0.1,i*0.2,i*0.3])) for i in range(500000) )
d2={}

def fun1(gn):
    x,y,z = d1[gn]
    d2.update({gn:((x+y+z)/3)})


if __name__ == '__main__':
    gen1 = [x for x in d1.keys()]

    # serial processing
    for gn in gen1:
        fun1(gn)

    # paralel processing
    p = multiprocessing.Pool(3)
    p.map(fun1, gen1)
    p.close()
    p.join()

    print('Script finished')
    stop_time = timeit.default_timer()
    print(stop_time - start_time)