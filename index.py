#!/usr/bin/env python

import ast
import pickle
import pprint
import os
import os.path
import random
import string
import sys

import numpy as np
from scipy.io import savemat, loadmat

from skimage.io import imread, imsave
import skimage.measure
import skimage.segmentation

#################################################################################
## Setup
#################################################################################

if not len(sys.argv) == 4:
  print('./index.py image_path flattened_path map.txt')
  sys.exit()

image_dirname = sys.argv[1]
label_dirname = sys.argv[2]
map_filename = sys.argv[3]

# Load labels
print('loading labels')
label_names = ['empty']
with open(map_filename, 'r') as f:
  label_names += [x.split(': ')[1].strip() for x in f]

# Get list of labels
if os.path.exists('index.pickle'):
  print('index cache found, loading from cache')
  label_images = pickle.load(open('index.pickle', 'r'))
else:
  print('no index cache found, generating index')
  label_images = dict([(x, []) for x in label_names])
  for folder, subfolders, filenames in os.walk(label_dirname):
    for filename in filenames:
      print('  checking %s...' % os.path.join(folder, filename))
      label_filename = os.path.join(folder, filename)
      label_image = loadmat(label_filename)['Label']
      for label_int in np.unique(label_image):
        try:
          label_images[label_names[label_int]].append((os.path.splitext(filename)[0], label_filename, folder))
        except IndexError:
          print('ERROR: Label index %d is out of range!' % label_int)
  print('caching index')
  pickle.dump(label_images, open('index.pickle', 'w'))

# Get label sets
print('collecting label sets')
label_sets = set()
for label_name in label_names:
  for image_name, label_filename, folder in label_images[label_name]:
    label_sets.add(folder)

# Get list of changes
if os.path.exists('changes.pickle'):
  print('change cache found, loading from cache')
  changes = pickle.load(open('changes.pickle', 'r'))
else:
  print('no change cache found')
  changes = {}
  pickle.dump(changes, open('changes.pickle', 'w'))
  
#################################################################################
## Server
#################################################################################

from results_template import results_template

from flask import Flask, send_from_directory, request
app = Flask('Label Explorer')

@app.route('/change/<image_name>/<from_label>/to/', defaults={'to_label': ''})
@app.route('/change/<image_name>/<from_label>/to/<to_label>')
def change_label(image_name, from_label, to_label):
  global changes
  print('to_label = %s' % to_label)
  if to_label == '':
    if changes.has_key((image_name, from_label)):
      del changes[(image_name, from_label)]
  else:
    changes[(image_name, from_label)] = to_label
  pickle.dump(changes, open('changes.pickle', 'w'))
  return ''

@app.route('/regions/<path:filename>')
def get_image(filename):
  return send_from_directory('/home/vnguyen/labeling/staging/regions', filename)

@app.route('/query/<query_label>')
def get_label_examples(query_label):
  global label_names
  global label_sets
  global label_images
  global results_template

  if query_label not in label_names:
    return 'Could not find label "%s"!' % query_label
  query_image_index = label_names.index(query_label)

  query_image_list = label_images[query_label]
  if len(query_image_list) == 0:
    return 'No images found with label "%s"!' % query_label

  try:
    response_num = int(request.args.get('num'))
  except:
    response_num = 10

  query_label_sets = set(label_sets)
  set_filter = request.args.get('set')
  if set_filter:
    query_label_sets = set([set_filter])
    query_image_list = filter(lambda x: set_filter in x[2], query_image_list)

  change_filter = request.args.get('nochanges')
  if change_filter:
    query_image_list = filter(lambda x: not changes.has_key((x[0], query_label)) or changes[(x[0], query_label)] is '', query_image_list)

  response_num = min(len(query_image_list), response_num)
  random_images = random.sample(query_image_list, response_num)
  regions_metadata = []

  for image_name, label_filename, label_folder in random_images:
    image_filename = os.path.join(image_dirname, '%s.jpg' % image_name)
    image = imread(image_filename)
    label_image = loadmat(label_filename)['Label']
    image_rows, image_cols = label_image.shape
    regions = skimage.measure.regionprops(label_image)
    for region_index, region in enumerate(regions):
      if region.label != query_image_index:
        continue
      print('Processing image "%s", region %d...' % (label_filename, region_index))
      # min_row, min_col, max_row, max_col = region.bbox
      # min_row = max(min_row - 10, 0)
      # min_col = max(min_col - 10, 0)
      # max_row = min(max_row + 10, image_rows)
      # max_col = min(max_col + 10, image_cols)
      # region_image = image[min_row:max_row, min_col:max_col]
      region_image = skimage.segmentation.mark_boundaries(image, label_image == region.label, color=(0, 1, 0))
      region_filename = 'regions/%s-%s-%d.png' % (query_label, image_name, region_index)
      change_value = ''
      if changes.has_key((image_name, query_label)):
        change_value = changes[(image_name, query_label)]
      regions_metadata.append((image_name, region_filename, label_folder, change_value))
      if not os.path.exists(region_filename):
        imsave(region_filename, region_image)

  namespace = dict(locals())
  tmpl = results_template(searchList=[namespace])
  return str(tmpl)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8888, debug=True)

