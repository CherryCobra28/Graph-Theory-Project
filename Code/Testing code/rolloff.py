import random as rand
import math


def modifier(x):
    mods = list(range(-5,6))
    #print(mods)
    index = math.floor(11*x)
    if index == 11:
        index -= 1
    return mods[index]

def rolloff(p_i,r_i):
    infecter = rand.randint(1,20) + modifier(p_i)
    resister = rand.randint(1,20) + modifier(r_i)
    print(f'{infecter=}, {resister=}')
    if infecter > resister:
        print('infected')
    else: 
        print('resisted')
        
rolloff(0.7,0.2)