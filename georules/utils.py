from pathlib import Path
from typing import List
import numpy as np 
import json

def save_bath_as_array(filename:Path, bath_map:List[np.ndarray]) -> None:
    """Serialize a list of bathymetry arrays into a 3D array.""" 
    _array = np.stack(bath_map)
    with open(filename, 'wb') as fh: 
        np.save(fh, _array)

def load_bath_binary(filename:Path) -> np.ndarray:
    """Load a serialized bathymetry."""
    with open(filename, 'rb') as fh: 
        res = np.load(filename)
    return res


def save_list_as_json(filename:Path,_list) -> None:
    """Saves a list like a json file"""
    with open(filename, "w") as fh:
        json.dump(filename,fh)

def load_list_json(filename:Path) -> list:
    """ Load list from json file"""
    with open(filename, "r") as file:
        loaded_list = json.load(file)
        return(loaded_list)


if __name__ == '__main__':
    # test case 
    l = [] 
    for _ in range(10): 
        l.append(np.zeros(shape=(5,5))) 

    test_file = Path("../test_array.npy")
    save_bath_as_array(test_file, l)

    bla = load_bath_binary(test_file)
    print(f"Arrays Equal: {np.array_equal(l, bla)}") 

    # cleanup
    test_file.unlink() 
