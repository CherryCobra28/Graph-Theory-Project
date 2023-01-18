def all_squares():
    num = 0
    while True:
        yield num**2
        num += 1

def test():
    
    A = (yield n)


A = all_squares()

print(A)
