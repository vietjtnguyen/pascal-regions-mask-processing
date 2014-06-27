#!/usr/bin/env python

'''apply-corrections.py

Applies mask-level changes stored by the index.py website as changes.pickle to
flattened label images.

Usage:
  ./apply_corrections.py [options] <label_map> <changes_pickle> <src_dirname> <dst_dirname>

Arguments:
  <label_map>       Text file containing "%d: %s" pairs. Same file
                    format used by GIMP toolbox.
  <changes_pickle>  Python pickle file saved by index.py website.
                    Should be changes.pickle.
  <src_dirname>     Path to folder containing flattened, probably
                    filled labels.
  <dst_dirname>     Path to folder where corrected labels will be
                    saved.

Options:
  -n --dry-run      Do not actually apply corrections.

Example:
  ./apply-corrections.py ./map/v1/aggregate-map.txt ./changes.pickle ./filled/trainval ./remapped/v1.1/trainval
'''

import ast
import copy
import pickle
import pprint
import os
import os.path
import random
import string
import sys

import numpy as np
from scipy.io import savemat, loadmat

#################################################################################

from docopt import docopt
args = docopt(__doc__, version='0.1')

is_dry_run = args['--dry-run']
map_filename = args['<label_map>']
changes_filename = args['<changes_pickle>']
src_dirname = args['<src_dirname>']
dst_dirname = args['<dst_dirname>']

if not os.path.exists(dst_dirname):
  os.makedirs(dst_dirname)

#################################################################################

print('loading corrections')
with open(changes_filename, 'r') as f:
  changes = pickle.load(f)

print('aggregating corrections by image')
changes_by_image = {}
for (image, from_label), to_label in changes.items():
  if not changes_by_image.has_key(image):
    changes_by_image[image] = []
  changes_by_image[image].append((from_label, to_label))

#################################################################################

print('loading labels')
src_index_to_src_name  = ['empty']
with open(map_filename, 'r') as f:
  src_index_to_src_name += [x.split(': ')[1].strip() for x in f]

src_name_to_src_index = dict(zip(src_index_to_src_name, range(len(src_index_to_src_name))))

#################################################################################

print('applying corrections')
for image_name, changes in changes_by_image.items():
  from_label_filename = os.path.join(src_dirname, image_name+'.mat')
  to_label_filename = os.path.join(dst_dirname, image_name+'.mat')
  print('  "%s" -> "%s"' % (from_label_filename, to_label_filename))
  if not os.path.exists(from_label_filename):
      print('    skipping, label file does not exist')
      continue
  label_image = loadmat(from_label_filename)['LabelMap']
  for from_label_name, to_label_name in changes:
    if 'fix' in to_label_name.lower():
      print('    skipping "%s" -> "%s", only marked for fix' % (from_label_name, to_label_name))
      continue
    if not src_name_to_src_index.has_key(from_label_name):
      print('    skipping "%s" -> "%s", "%s" is unknown label' % (from_label_name, to_label_name, from_label_name))
      continue
    if not src_name_to_src_index.has_key(to_label_name):
      print('    skipping "%s" -> "%s", "%s" is a new label' % (from_label_name, to_label_name, to_label_name))
      continue
    print('    "%s" -> "%s"' % (from_label_name, to_label_name))
    from_label_int = src_name_to_src_index[from_label_name]
    to_label_int = src_name_to_src_index[to_label_name]
    label_image[label_image == from_label_int] = to_label_int
  if not is_dry_run:
    savemat(to_label_filename, {'LabelMap': label_image}, do_compression=True)

