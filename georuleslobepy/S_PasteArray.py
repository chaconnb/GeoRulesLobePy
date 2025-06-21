# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:31:56 2023

@author: Nataly Chacon-Buitrago
Functions taken from: https://stackoverflow.com/questions/7115437/how-to-embed-a-small-numpy-array-into-a-predefined-block-of-a-large-numpy-arra

wall = larger numpy array in which another numpy array is going to be paste
block = smaller numpy array that is paste into the wall
loc = tuple with the location of the uppermost corner of the block array paste in the wall array (row,column)
      The tuple can be negative meaning the uppermost corner of the wall is outside the block. 


"""

def paste_slices(tup):
  pos, w, max_w = tup
  wall_min = max(pos, 0)
  wall_max = min(pos+w, max_w)
  block_min = -min(pos, 0)
  block_max = max_w-max(pos+w, max_w)
  block_max = block_max if block_max != 0 else None
  return slice(wall_min, wall_max), slice(block_min, block_max)

def paste(wall, block, loc): 
  loc_zip = zip(loc, block.shape, wall.shape)
  wall_slices, block_slices = zip(*map(paste_slices, loc_zip))
  wall[wall_slices] = block[block_slices]
  return wall

  
# =============================================================================
# 
# # Example:
#    b = np.zeros([10, 10])
#    a = np.arange(1,33).reshape(4,8) 
#    paste(b, a, (-1, -3))
# 
# 
# =============================================================================






