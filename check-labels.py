#!/usr/bin/env python

'''check-labels.py

Performs various checks and gathers statistics on all labels in the specified path.

Usage:
  ./check-labels.py [options] <map> <folder>
  ./check-labels.py [options] findempty <map> <folder>

Arguments:
  <map>     Text file containing "%d: %s" pairs. Same file format used by GIMP
            toolbox.
  <folder>  Path to folder containing flattened, probably filled labels.

Options:
  -f LABELS --label-filter=LABELS  Comma-separated list of labels to filter.

Example:
  ./check-labels.py ./map/v1/aggregate-map.txt ./flattened/trainval
  ./check-labels.py ./map/v1/aggregate-map.txt ./filled/trainval
  ./check-labels.py ./map/v1/aggregate-map.txt ./remapped/v1.1/trainval
  ./check-labels.py ./map/v2/map.txt ./remapped/v2/trainval
'''

import ast
import copy
import pickle
import pprint
import os
import os.path
import random
import string
from cStringIO import StringIO
import sys

import numpy as np
from scipy.io import savemat, loadmat

#################################################################################

from docopt import docopt
args = docopt(__doc__, version='0.1')

map_filename  = args['<map>']
labels_dirname  = args['<folder>']
do_findempty = args['findempty']
label_filter = args['--label-filter']

if not label_filter is None:
  label_filter = [x.strip() for x in label_filter.split(',')]

#################################################################################

index_to_name  = ['empty']
with open(map_filename, 'r') as f:
  index_to_name += [x.split(': ')[1].strip() for x in f]
name_to_index = dict(zip(index_to_name, range(len(index_to_name))))

#################################################################################

file_buffer = StringIO()
layer_buffer = StringIO()
label_buffer = StringIO()

for folder, subfolders, filenames in os.walk(labels_dirname):
  for filename in sorted(filter(lambda x: x.endswith('.mat'), filenames)):
    label_filename = os.path.join(folder, filename)
    file_buffer.truncate(0)
    file_buffer.write('%s\n' % label_filename)
    label_mat = loadmat(label_filename)
    file_has_empty = False
    file_matches_filter = False
    for layer_name in filter(lambda x: x.startswith('Label'), label_mat.keys()):
      layer_buffer.truncate(0)
      layer_image = label_mat[layer_name]
      layer_area = layer_image.shape[0] * layer_image.shape[1]
      layer_buffer.write('  %s\n' % layer_name)
      layer_has_empty = False
      layer_matches_filter = False
      for label_int in np.unique(layer_image):
        label_name = index_to_name[label_int]
        layer_has_empty |= label_int == 0
        if label_filter is None or label_name in label_filter:
          label_buffer.truncate(0)
          label_area = np.sum(layer_image == label_int)
          label_area_percentage = float(label_area) / layer_area * 100.0
          label_buffer.write('    %d (%s), area=%d (%.6f%%)\n' % (label_int, label_name, label_area, label_area_percentage))
          layer_buffer.write(label_buffer.getvalue())
          layer_matches_filter = True
      if ( not do_findempty or layer_has_empty ) and layer_matches_filter:
        file_buffer.write(layer_buffer.getvalue())
      file_has_empty |= layer_has_empty
      file_matches_filter |= layer_matches_filter
    if ( not do_findempty or file_has_empty ) and file_matches_filter:
      sys.stdout.write(file_buffer.getvalue())

