#!/usr/bin/env python

'''translate-labels.py

Performs label-level changes from the map commands in column J of the following
Google Spreadsheet:

  https://docs.google.com/spreadsheets/d/1A7aUI0PLTOD4JfvCpZRy4bbyuhAHZvfHKYGc79ORzDo/edit#gid=358742821

Usage:
  ./translate-labels.py [options] <translation_list> <src_map> <src_dirname> <dst_map> <dst_dirname>

Arguments:
  <translation_list>  Text file containing "%d->%s" pairs from the spreadsheet
                      mentioned above.
  <src_map>           Text file containing "%d: %s" pairs for the "before"
                      ("source") labels. Same file format used by GIMP toolbox.
  <src_dirname>       Path to folder containing flattened, probably filled
                      labels. These will probably have been corrected by
                      apply-corrections.py.
  <dst_map>           Filename for where the new map file will be written.
  <dst_dirname>       Path to folder where corrected labels will be saved.
                      Path relative to <src_dirname> is preserved.

Options:
  -n --dry-run      Do not actually apply corrections.

Example:
  ./translate-labels.py ./map/v1-to-v2.txt ./map/v1/aggregate-map.txt ./remapped/v1.1/trainval ./map/v2/map.txt ./remapped/v2/trainval
'''

import ast
import copy
import pickle
import pprint
import os
import os.path
import random
import string
import StringIO
import sys

import numpy as np
from scipy.io import savemat, loadmat

#################################################################################

from docopt import docopt
args = docopt(__doc__, version='0.1')

is_dry_run = args['--dry-run']
translation_filename  = args['<translation_list>']
src_map_filename = args['<src_map>']
src_dirname = args['<src_dirname>']
dst_map_filename = args['<dst_map>']
dst_dirname = args['<dst_dirname>']

#################################################################################

print('loading source labels')
src_index_to_src_name  = ['empty']
with open(src_map_filename, 'r') as f:
  src_index_to_src_name += [x.split(': ')[1].strip() for x in f]

#################################################################################

print('loading source-to-destination translation map')
translation_map = []
removal_list = []
with open(translation_filename, 'r') as f:
  def parse_translation(x):
    before, after = x.split('->')
    before = int(before)
    after = after.strip()
    if after == 'empty':
      removal_list.append(before)
    print('  %s -> %s' % (before, str(after)))
    return before, after
  translation_map += list(map(parse_translation, filter(lambda x: len(x.split('->')) == 2, f)))

print('labels being removed')
for src_index in removal_list:
  print('  %d (%s)' % (src_index, src_index_to_src_name[src_index]))

#################################################################################

print('constructing source to temporary translation map')
src_index_to_tmp_name = copy.copy(src_index_to_src_name)
print('  renaming labels')
for old_index, new_name in translation_map:
  print('    %s -> %s' % (src_index_to_tmp_name[old_index], new_name))
  src_index_to_tmp_name[old_index] = new_name

print('source to temporary translation map')
for src_index in range(len(src_index_to_tmp_name)):
  print('  %d (%s) -> %s' % (src_index, src_index_to_src_name[src_index], src_index_to_tmp_name[src_index]))

#################################################################################

print('constructing new label map')
dst_index_to_dst_name = sorted(list(set(src_index_to_tmp_name)))
dst_index_to_dst_name.remove('empty')
dst_index_to_dst_name = ['empty'] + dst_index_to_dst_name
dst_name_to_dst_index = dict(zip(dst_index_to_dst_name, range(len(dst_index_to_dst_name))))
src_index_to_dst_index = [dst_name_to_dst_index[x] for x in src_index_to_tmp_name]

print('writing destination map file %s' % dst_map_filename)
with open(dst_map_filename, 'w') as f:
  for dst_index in range(1, len(dst_index_to_dst_name)):
    print('  %d: %s' % (dst_index, dst_index_to_dst_name[dst_index]))
    f.write('%d: %s\n' % (dst_index, dst_index_to_dst_name[dst_index]))
    
print('source to destination translation map')
for src_index in range(len(src_index_to_dst_index)):
  print('  %d (%s) -> %d (%s)' % (src_index, src_index_to_src_name[src_index], src_index_to_dst_index[src_index], dst_index_to_dst_name[src_index_to_dst_index[src_index]]))

#################################################################################

errors = StringIO.StringIO()
def err(x):
  print(x)
  errors.write(x+'\n')

print('translating label files')
for folder, subfolders, filenames in os.walk(src_dirname):
  for filename in sorted(filter(lambda x: x.endswith('.mat'), filenames)):
    label_filename = os.path.join(folder, filename)
    sys.stdout.write('  %s' % label_filename)
    label_image = loadmat(label_filename)['LabelMap']
    try:
      for src_index in np.unique(label_image):
        if src_index in removal_list:
          err('\n    ERROR: Encountered label %d (%s) for image %s which is being mapped to "empty" (0) which is equivalent to removal!' % (src_index, src_index_to_src_name[src_index], label_filename))
        label_image[label_image == src_index] = src_index_to_dst_index[src_index]
    except Exception as e:
      err('\n    ERROR: Encountered exception: %s' % str(e))
      err('    src_index=%d' % src_index)
      err('    unique=%s' % str(np.unique(label_image)))
      err('    src_index_to_dst_index[src_index]=%d' % src_index_to_dst_index[src_index])
    label_filename = os.path.relpath(label_filename, src_dirname)
    label_filename = os.path.join(dst_dirname, label_filename)
    label_dirname = os.path.split(label_filename)[0]
    if not os.path.exists(label_dirname):
      os.makedirs(label_dirname)
    sys.stdout.write(' -> %s\n' % label_filename)
    if not is_dry_run:
      savemat(label_filename, {'LabelMap': label_image}, do_compression=True)

print('errors:')
print(errors.getvalue())
