#!/usr/bin/env python

'''check-labels.py

Performs various checks and gathers statistics on all labels in the specified path.

Usage:
  ./check-labels.py [options] <map> <folder>
  ./check-labels.py [options] findempty <map> <folder>
  ./check-labels.py [options] labelstats <map> <folder>

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
from collections import namedtuple
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
do_labelstats = args['labelstats']
label_filter = args['--label-filter']

if not label_filter is None:
  label_filter = [x.strip() for x in label_filter.split(',')]

#################################################################################

index_to_name  = ['empty']
with open(map_filename, 'r') as f:
  index_to_name += [x.split(': ')[1].strip() for x in f]
name_to_index = dict(zip(index_to_name, range(len(index_to_name))))

LabelStat = namedtuple('LabelStat', ['images', 'layers_all', 'layers_by_image', 'areas', 'area_percentages'])
name_to_stat = dict(zip(index_to_name, [LabelStat(set(), [], {}, [], []) for i in range(len(index_to_name))]))

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
        stat_images, stat_layers_all, stat_layers_by_image, stat_areas, stat_area_percentages = name_to_stat[label_name]
        stat_images.add(label_filename)
        stat_layers_all.append((label_filename, layer_name))
        if not stat_layers_by_image.has_key(label_filename):
          stat_layers_by_image[label_filename] = []
        stat_layers_by_image[label_filename].append(layer_name)
        layer_has_empty |= label_int == 0
        if label_filter is None or label_name in label_filter:
          label_buffer.truncate(0)
          label_area = np.sum(layer_image == label_int)
          label_area_percentage = float(label_area) / layer_area * 100.0
          stat_areas.append(label_area)
          stat_area_percentages.append(label_area_percentage)
          label_buffer.write('    %d (%s), area=%d (%.6f%%)\n' % (label_int, label_name, label_area, label_area_percentage))
          layer_buffer.write(label_buffer.getvalue())
          layer_matches_filter = True
      if ( not do_findempty or layer_has_empty ) and layer_matches_filter:
        file_buffer.write(layer_buffer.getvalue())
      file_has_empty |= layer_has_empty
      file_matches_filter |= layer_matches_filter
    if ( not do_findempty or file_has_empty ) and file_matches_filter:
      sys.stdout.write(file_buffer.getvalue())

if do_labelstats:
  print('label statistics:')
  for label_name in index_to_name:
    stat_images, stat_layers_all, stat_layers_by_image, stat_areas, stat_area_percentages = name_to_stat[label_name]
    print('  %s' % label_name)
    print('    number of images: %d' % len(stat_images))
    print('    number of layers: %d' % len(stat_layers_all))
    if len(stat_images) > 0:
      layers_per_image = [len(x) for x in stat_layers_by_image.values()]
      print('    average number of layers per image: %f (std = %f)' % (np.mean(layers_per_image), np.std(layers_per_image)))
      print('    average area per layer: %f (std = %f)' % (np.mean(stat_areas), np.std(stat_areas)))
      print('    average area (percentage) per layer: %f%% (std = %f%%)' % (np.mean(stat_area_percentages), np.std(stat_area_percentages)))
