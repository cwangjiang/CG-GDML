#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2018 Stefan Chmiela
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, sys
import argparse
import numpy as np

from sgdml.utils import io,ui


# Assumes that the atoms in each molecule are in the same order.
def read_concat_ext_xyz(f):
	n_atoms = None

	R,z,E,F = [],[],[],[]
	for i,line in enumerate(f):
		line = line.strip()

		cols = line.split()

		if not n_atoms:
			n_atoms = len(cols)/2/3
			print 'Number atoms per geometry:      {:>7d}'.format(n_atoms)

		R.append(map(float,cols[0:(n_atoms*3)]))
		F.append(map(float,cols[(n_atoms*3):]))

		if i % 1000 == 0:
			sys.stdout.write("\rNumber geometries found so far: {:>7d}".format(i))
			sys.stdout.flush()
	sys.stdout.write("\rNumber geometries found so far: {:>7d}".format(i))
	sys.stdout.flush()
	print ''

	R = np.array(R).reshape(-1,n_atoms,3)
	z = np.ones((n_atoms,))
	E = np.ones((R.shape[0],))
	F = np.array(F).reshape(-1,n_atoms,3)

	f.close()
	return (R,z,E,F)


parser = argparse.ArgumentParser(description='Creates a dataset from NOE file format.')
parser.add_argument('dataset', metavar = '<dataset>',\
							   type    = argparse.FileType('r'),\
							   help	   = 'path to xyz dataset file')
parser.add_argument('-o','--overwrite', dest='overwrite', action='store_true', help = 'overwrite existing dataset file')
args = parser.parse_args()
dataset = args.dataset


name = os.path.splitext(os.path.basename(dataset.name))[0]
dataset_file_name = name + '.npz'

dataset_exists = os.path.isfile(dataset_file_name)
if dataset_exists and args.overwrite:	
	print ui.info_str('[INFO]') + ' Overwriting existing dataset file.'
if not dataset_exists or args.overwrite:
	print 'Writing dataset to \'%s\'...' % dataset_file_name
else:
	sys.exit(ui.fail_str('[FAIL]') + ' Dataset \'%s\' already exists.' % dataset_file_name)

R,z,E,F = read_concat_ext_xyz(dataset)

# Base variables contained in every model file.
base_vars = {'type':			'd',\
			 'R':				R,\
			 'z':				z,\
			 'E':				E[:,None],\
			 'F':				F,\
			 'name':			name,\
			 'theory':			'unknown'}
base_vars['md5'] = io.dataset_md5(base_vars)

np.savez_compressed(dataset_file_name, **base_vars)
print ui.pass_str('DONE')