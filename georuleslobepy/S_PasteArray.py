# -*- coding: utf-8 -*-
"""
@author: Nataly Chacon-Buitrago
Functions taken from: https://stackoverflow.com/questions/7115437/how-to-embed-a-small-numpy-array-into-a-predefined-block-of-a-large-numpy-arra

"""

def paste_slices(tup):
  """
      Computes the slice indices for pasting a smaller array (block) into a larger array (wall).

      Given the position of the upper-left corner of the block within the wall, this function 
      returns the valid slice ranges for both the wall and the block arrays, handling negative 
      offsets and edge clipping as needed.

      Parameters
      ----------
      tup : tuple
          A tuple of three values:
          - pos : int
              Position of the block's uppermost corner in the wall (can be negative).
          - w : int
              Size of the block along a given dimension.
          - max_w : int
              Size of the wall along the same dimension.

      Returns
      -------
      wall_slice : slice
          Slice object representing the affected region in the wall.
      block_slice : slice
          Slice object representing the region of the block to be pasted into the wall.

      Notes
      -----
      This function supports partial overlaps, including when part of the block lies outside the wall.
  """

  pos, w, max_w = tup
  wall_min = max(pos, 0)
  wall_max = min(pos+w, max_w)
  block_min = -min(pos, 0)
  block_max = max_w-max(pos+w, max_w)
  block_max = block_max if block_max != 0 else None

  return slice(wall_min, wall_max), slice(block_min, block_max)

def paste(wall, block, loc): 
  """
    Pastes a smaller array (`block`) into a larger array (`wall`) at a specified location.

    This function embeds `block` into `wall` starting at `loc`, taking care to handle
    out-of-bounds pasting gracefully by clipping both arrays as needed.

    Parameters
    ----------
    wall : ndarray
        The larger array into which the block will be pasted.
    block : ndarray
        The smaller array to paste into the wall.
    loc : tuple of int
        Coordinates (row, column, ...) specifying the upper-left corner of the block
        within the wall. Negative values are allowed and handled via clipping.

    Returns
    -------
    wall : ndarray
        The modified wall array with the block pasted in.

    Notes
    -----
    - The shape of `block` must be compatible with the shape of `wall` at the insertion location.
    - Partial overlaps are supported: if the block extends beyond the wall’s boundaries, only the 
      overlapping region will be pasted.
    """
  loc_zip = zip(loc, block.shape, wall.shape)
  wall_slices, block_slices = zip(*map(paste_slices, loc_zip))
  wall[wall_slices] = block[block_slices]

  return wall

  






