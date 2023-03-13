import scipy
import networkx as nx
from typing import Callable
vals = []
numbers = range(1,10000000)
gamma = 2.5
for i in numbers:
    a = i*(i**(-gamma)/scipy.special.zeta(gamma))
    vals.append(a)
print(sum(vals))