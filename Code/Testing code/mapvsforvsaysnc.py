from time import perf_counter

numbers = [x for x in range(100)]

def square(x):
    return x**2



t1= perf_counter()
L = []
for i in numbers:
    a = square(i)
    L.append(a)
print(f'{L},{perf_counter()-t1}')

t1 = perf_counter()
L = map(square, numbers)
print(f'{list(L)},{perf_counter()-t1}')