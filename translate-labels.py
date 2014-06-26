#!/usr/bin/env python

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

if not len(sys.argv) == 6:
  print('./translate-labels.py src_labels.txt translation_list.txt src_folder dst_folder src_mod_labels.txt')
  sys.exit()

map_filename = sys.argv[1]
translation_filename = sys.argv[2]
src_dirname = sys.argv[3]
dst_dirname = sys.argv[4]
dst_map_filename = sys.argv[5]

#################################################################################

print('loading translation map')
translation_map = []
with open(translation_filename, 'r') as f:
  def parse_translation(x):
    before, after = x.split('->')
    before = int(before)
    try:
      after = int(after)
    except:
      after = after.strip()
      after = 'empty' if after == 'REMOVE' else after
    print('  %s -> %s' % (before, str(after)))
    return before, after
  translation_map += list(map(parse_translation, filter(lambda x: len(x.split('->')) == 2, f)))

#################################################################################

print('loading labels')
src_index_to_src_name  = ['empty']
with open(map_filename, 'r') as f:
  src_index_to_src_name += [x.split(': ')[1].strip() for x in f]

#################################################################################

print('constructing source to temporary translation map')
src_index_to_tmp_name = copy.copy(src_index_to_src_name)
print('renaming labels')
for old_index, new_name in filter(lambda x: type(x[1]) is str, translation_map):
  print('  %s -> %s' % (src_index_to_tmp_name[old_index], new_name))
  src_index_to_tmp_name[old_index] = new_name
print('redirecting labels')
for old_index, new_index in filter(lambda x: type(x[1]) is int, translation_map):
  print('  %d -> %d (%s -> %s)' % (old_index, new_index, src_index_to_tmp_name[old_index], src_index_to_tmp_name[new_index]))
  src_index_to_tmp_name[old_index] = src_index_to_tmp_name[new_index]

#################################################################################

print('constructing new label map')
dst_index_to_dst_name = sorted(list(set(src_index_to_tmp_name)))
dst_index_to_dst_name.remove('empty')
dst_index_to_dst_name = ['empty'] + dst_index_to_dst_name
dst_name_to_dst_index = dict(zip(dst_index_to_dst_name, range(len(dst_index_to_dst_name))))
src_index_to_dst_index = [dst_name_to_dst_index[x] for x in src_index_to_tmp_name]

print('writing new map file %s' % dst_map_filename)
with open(dst_map_filename, 'w') as f:
  for i in range(1, len(dst_index_to_dst_name)):
    print('  %d: %s' % (i, dst_index_to_dst_name[i]))
    f.write('%d: %s\n' % (i, dst_index_to_dst_name[i]))

#################################################################################

# Get list of labels
for folder, subfolders, filenames in os.walk(src_dirname):
  for filename in sorted(filter(lambda x: x.endswith('.mat'), filenames)):
    label_filename = os.path.join(folder, filename)
    print('  processing %s' % label_filename)
    label_image = loadmat(label_filename)['Label']
    try:
      for label_int in np.unique(label_image):
        label_image[label_image == label_int] = src_index_to_dst_index[label_int]
    except Exception as e:
      print('ERROR: Encountered exception: %s' % str(e))
      print('  label_int=%d' % label_int)
      print('  unique=%s' % str(np.unique(label_image)))
      print('  src_index_to_dst_index[label_int]=%d' % src_index_to_dst_index[label_int])
    label_filename = os.path.relpath(label_filename, src_dirname)
    label_filename = os.path.join(dst_dirname, label_filename)
    label_dirname = os.path.split(label_filename)[0]
    if not os.path.exists(label_dirname):
      os.makedirs(label_dirname)
    print('    saving to %s' % label_filename)
    savemat(label_filename, {'Label': label_image})

