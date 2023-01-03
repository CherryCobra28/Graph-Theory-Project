import pandas as pd

class dict_zip_error(Exception):
    "The dictionaries must have the same keys"
    pass


def dict_zip(A: dict,B: dict) -> dict:
    """_summary_

    Args:
        A (dict): _description_
        B (dict): _description_

    Raises:
        dict_zip_error: _description_

    Returns:
        dict: _description_
    """    
    if  not (A.keys() == B.keys()):
        raise dict_zip_error
    return_dict = []
    final = {}
    keys = list(A.keys())
    for key in keys:
        if (type(A.get(key)) is list) and (type(B.get(key)) is list):
            items = [*A.get(key), *B.get(key)] 
        elif (type(A.get(key)) is list):
            items = [*A.get(key), B.get(key)] 
        else:   
            items = [A.get(key), B.get(key)]
        return_dict.append({key:items})
    for dic in return_dict:
        final = final | dic
    return (final)    



    #{'n':[2,5],'k':[3,6]}
    


if __name__ == '__main__':
    A = {'n': 30, 'P_i': 0.5, 'P_r': 0.6, 'Days_Taken': 13, 'Surviors': 19, 'Everyone_Dead': False, 'Graph_Type': 'barabasi'}
    B = {'n': 30, 'P_i': 0.5, 'P_r': 0.6, 'Days_Taken': 12, 'Surviors': 18, 'Everyone_Dead': False, 'Graph_Type': 'barabasi'}
    V = {'n': 30, 'P_i': 0.5, 'P_r': 0.6, 'Days_Taken': 16, 'Surviors': 8, 'Everyone_Dead': False, 'Graph_Type': 'barabasi'}
    C = dict_zip(A,B)
    print(C)
    K = dict_zip(C,V)
    print(K)
    D = pd.DataFrame.from_dict(C)
    print(D)