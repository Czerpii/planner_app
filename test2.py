def foo(first, second, **option):
    dict = option
    print(dict["dwa"])
    
foo(1,2,dwa="cham",trzy=5)