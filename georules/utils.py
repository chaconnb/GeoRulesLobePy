from pathlib import Path
from typing import List
import numpy as np 
import math
import json


def save_bath_as_array(filename:Path, foldername:Path, bath_map:List[np.ndarray]) -> None:
    """Serialize a list of bathymetry arrays into a 3D array.""" 
    _array = np.stack(bath_map)
    file_path = Path(foldername) /Path(filename)  
    with open(file_path, 'wb') as fh:  # Open in binary mode ('wb')
        np.save(fh, _array)
    
    
def save_array(filename:Path, foldername:Path,_array:np.ndarray) -> None:
    """Saves array in .npy file.""" 
    file_path = Path(foldername) /Path(filename) 
    with open(file_path,'wb') as fh:
        np.save(fh, _array)
        
def save_centroids(filename:Path, foldername:Path,_list) -> None:
    """Saves list in .npy file.""" 
    for i in range(len(_list)):
         if not _list[i]:
             _list[i] = [math.nan, math.nan]       
    _array = np.stack(_list)          
    file_path = Path(foldername)/Path(filename) 
    with open(file_path,'wb') as fh:
        np.save(fh, _array)

def load_array(filename:Path, foldername:Path) -> np.ndarray:
    """Load a serialized array."""
    file_path = Path(foldername)/Path(filename)
    with open(file_path, 'rb') as fh: 
        res = np.load(fh)
    return res

def save_list_as_json(filename:Path, foldername:Path, _list) -> None:
    """Saves a list as a JSON file in a specific folder."""
    folder_path = Path(foldername)
    file_path = folder_path / (filename +".json")
    with open(file_path, "w") as fh:
        json.dump(_list, fh)


def load_list_json(filename:Path, foldername:Path) -> list:
    """ Load list from json file"""
    folder_path = Path(foldername)
    file_path = folder_path / (filename +".json")
    with open(file_path, "r") as file:
        loaded_list = json.load(file)
        return(loaded_list)


if __name__ == '__main__':
    # test case 
    l = [] 
    for _ in range(10): 
        l.append(np.zeros(shape=(5,5))) 

    save_bath_as_array("test_file.npy","results",l)

    bla = load_array("test_file.npy","results") #results is the folder name
    print(f"Arrays Equal: {np.array_equal(l, bla)}") 