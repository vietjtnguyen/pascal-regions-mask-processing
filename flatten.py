#!/usr/bin/env python

import array
import ast
import colorsys
import datetime
import os
import os.path
import pprint
import re
import string
import sys

import numpy as np
from scipy.io import savemat, loadmat

def preorderRecurse(node, parent_data, dataFunc, childrenFunc, *args):
  data = dataFunc(node, parent_data, *args)
  child_list = [preorderRecurse(child, data, dataFunc, childrenFunc, *args) for child in childrenFunc(node)]
  return (data, child_list)

def flattenLabelMat(filename):
  mat_contents = loadmat(filename)
  # Create a copy of the variables inside the `.mat` file so that we can
  # preserve non-`Label*` and non-`Hierarchy` variables when we save the
  # `.mat` file back.
  keys = list(filter(lambda x: not x.startswith('__'), mat_contents.keys()))

  # Try to load the hierarchy if it exists in the `.mat` file.
  if 'Hierarchy' in keys:

    # If it exists it should be in the form of a Matlab string which can be
    # turned into a cell array tree structure by using `eval()` in Matlab.
    # We can convert this into a Python list-style tree structure by
    # replace the braces with square brackets and evaluating it as a Python
    # literal using `ast.literal_eval`.
    # 
    # NOTE (Viet): As a design note I initially wanted to save and read the
    # cell array directly but the way `scipy.io` reads and writes cell
    # arrays is very unwieldy. Eventually I settled on this method which is
    # nice and simple but perhaps susceptible to bugs. Time will tell.
    # 
    # TODO: Make this conversion more robust.
    # print('Found "Hierarchy" variable in .mat file. Parsing saved hierarchy...')
    matlab_hierarchy_expression = mat_contents['Hierarchy'][0]
    # print('Hierarchy expression in .mat file: %s' % matlab_hierarchy_expression)
    translation_table = string.maketrans('{}', '[]')
    python_hierarchy_expression = str(matlab_hierarchy_expression).translate(translation_table)
    # print('Translated Python hierarchy expression: %s' % python_hierarchy_expression)
    mat_hierarchy = ast.literal_eval(python_hierarchy_expression)

  # If it doesn't exists then we'll load them flatly in alphabetical order..
  else:
    # print('Did not find "Hierarchy" variable in .mat file. Loading all label layers in flat, sorted hierarchy...')
    mat_hierarchy = [[x, []] for x in list(sorted(filter(lambda x: x.startswith('Label'), mat_contents.keys())))]
    mat_hierarchy.append(['Original', []])

  # print('Hierarchy after loading .mat file:\n%s' % # pprint.pformat(mat_hierarchy))

  layers = []
  layer_names = []
  def dataFunc(node, parent_data):
    index, (data, children) = node
    layer_name = data
    parent_layer = parent_data
    node_is_a_group_layer = layer_name not in keys
    if layer_name == 'Original':
      # print('Encountered Original layer, ignoring.')
      return None
    elif node_is_a_group_layer:
      # print('Encountered GroupLayer "%s", ignoring.' % layer_name)
      return None
    else:
      # print('Encountered Layer "%s"' % layer_name)
      # `layers` is available via closure.
      layers.append(mat_contents[layer_name])
      layer_names.append(layer_name)
      return None

  childrenFunc = lambda x: enumerate(x[1][1])

  # print('Traversing hierarchy...')
  [preorderRecurse(root_layer, None, dataFunc, childrenFunc) for root_layer in enumerate(mat_hierarchy)]
  # print(layer_names)
  # print(list(reversed(layer_names)))

  output = np.zeros(layers[-1].shape, dtype='uint16')
  # print(output)
  # print(np.sum(output))
  for layer in reversed(layers):
    # print('----')
    # print(layer)
    non_empty = layer > 0
    output[non_empty] = layer[non_empty]
    # print(output)
    # print(output.min(), output.max())

  return output

if __name__ == '__main__':
  if not len(sys.argv) == 3:
    print('./flatten.py label/2008_000002.mat flat/2008_000002.mat')
    sys.exit()

  input_filename = sys.argv[1]
  output_filename = sys.argv[2]
  output = flattenLabelMat(input_filename)

  print('%s -> %s' % (input_filename, output_filename))
  savemat(output_filename, {'Label': output}, do_compression=True)

