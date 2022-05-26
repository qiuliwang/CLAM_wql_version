import torch
import torch.nn as nn
from math import floor
import os
import random
import numpy as np
import pdb
import time
from datasets.dataset_h5 import Dataset_All_Bags, Whole_Slide_Bag_FP
from torch.utils.data import DataLoader
from models.resnet_custom import resnet50_baseline
import argparse
from utils.utils import print_network, collate_features
from utils.file_utils import save_hdf5
from PIL import Image
import h5py
import openslide
import cv2 as cv 

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# def save_image(slide_id, numpy_file):
# 	print(slide_id)
# 	numpy_file = np.transpose(numpy_file, (0, 2, 3, 1))
# 	file_no = numpy_file.shape[0]
# 	print(file_no)
# 	print(numpy_file.shape)
	# for i in range(10):
	# 	image = numpy_file[i]
		# print(image)
		# cv.imwrite('Extracted_Patch/' + slide_id + '_' + str(i) + '.jpeg', image)



def compute_w_loader_(file_path, slide_id, output_path, wsi,
 	batch_size = 8, verbose = 0, print_every=20, pretrained=True, 
	custom_downsample=1, target_patch_size=-1):
	"""
	get patch images
	args:
		file_path: directory of bag (.h5 file)
		output_path: directory to save computed features (.h5 file)
		model: pytorch model
		batch_size: batch_size for computing features in batches
		verbose: level of feedback
		pretrained: use weights pretrained on imagenet
		custom_downsample: custom defined downscale factor of image patches
		target_patch_size: custom defined, rescaled image size before embedding
	"""
	dataset = Whole_Slide_Bag_FP(file_path=file_path, slide_id = slide_id, wsi=wsi, pretrained=False, 
		custom_downsample=custom_downsample, target_patch_size=target_patch_size)
	x, y = dataset[0]
	kwargs = {'num_workers': 4, 'pin_memory': True} if device.type == "cuda" else {}
	loader = DataLoader(dataset=dataset, batch_size=batch_size, **kwargs, collate_fn=collate_features)

	if verbose > 0:
		print('processing {}: total of {} batches'.format(file_path,len(loader)))

	mode = 'w'
	for count, (batch, coords) in enumerate(loader):
		# with torch.no_grad():	
		if count % print_every == 0:
			print('batch {}/{}, {} files processed'.format(count, len(loader), count * batch_size))
		# batch = batch.numpy()
		# print('shape of batch: ', batch.shape)

		# save_image(slide_id, batch)

			# features = model(batch)
			# features = features.cpu().numpy()
			# # print('shape of features: ', features.shape)

			# asset_dict = {'features': features, 'coords': coords}
			# save_hdf5(output_path, asset_dict, attr_dict= None, mode=mode)
			# mode = 'a'
	
	return output_path


parser = argparse.ArgumentParser(description='Feature Extraction')
parser.add_argument('--data_h5_dir', type=str, default=None)
parser.add_argument('--data_slide_dir', type=str, default=None)
parser.add_argument('--slide_ext', type=str, default= '.svs')
parser.add_argument('--csv_path', type=str, default=None)
parser.add_argument('--feat_dir', type=str, default='Extracted_Patch')
parser.add_argument('--batch_size', type=int, default=256)
parser.add_argument('--no_auto_skip', default=False, action='store_true')
parser.add_argument('--custom_downsample', type=int, default=1)
parser.add_argument('--target_patch_size', type=int, default=-1)
args = parser.parse_args()


if __name__ == '__main__':

	print('initializing dataset')
	csv_path = 'DataResult/process_list_autogen.csv'
	if csv_path is None:
		raise NotImplementedError

	bags_dataset = Dataset_All_Bags(csv_path)
	
	os.makedirs(args.feat_dir, exist_ok=True)
	os.makedirs(os.path.join(args.feat_dir, 'pt_files'), exist_ok=True)
	os.makedirs(os.path.join(args.feat_dir, 'h5_files'), exist_ok=True)
	dest_files = os.listdir(os.path.join(args.feat_dir, 'pt_files'))

	# print('loading model checkpoint')
	# model = resnet50_baseline(pretrained=True)
	# model = model.to(device)
	
	# # print_network(model)
	# if torch.cuda.device_count() > 1:
	# 	model = nn.DataParallel(model)
		
	# model.eval()
	total = len(bags_dataset)

	# for bag_candidate_idx in range(total):
	for bag_candidate_idx in range(10):
		slide_id = bags_dataset[bag_candidate_idx].split(args.slide_ext)[0]
		bag_name = slide_id+'.h5'
		h5_file_path = os.path.join(args.data_h5_dir, 'patches', bag_name)
		slide_file_path = os.path.join(args.data_slide_dir, slide_id+args.slide_ext)
		print('\nprogress: {}/{}'.format(bag_candidate_idx, total))
		print(slide_id)

		if not args.no_auto_skip and slide_id+'.pt' in dest_files:
			print('skipped {}'.format(slide_id))
			continue 

		output_path = os.path.join(args.feat_dir, 'h5_files', bag_name)
		time_start = time.time()
		wsi = openslide.open_slide(slide_file_path)
		output_file_path = compute_w_loader_(h5_file_path, slide_id, output_path, wsi, 
			batch_size = args.batch_size, verbose = 1, print_every = 20, 
			custom_downsample=args.custom_downsample, target_patch_size=args.target_patch_size)
		time_elapsed = time.time() - time_start
		print('\ncomputing features for {} took {} s'.format(output_file_path, time_elapsed))
		# file = h5py.File(output_file_path, "r")

		# features = file['features'][:]
		# print('features size: ', features.shape)
		# print('coordinates size: ', file['coords'].shape)
		# features = torch.from_numpy(features)
		# bag_base, _ = os.path.splitext(bag_name)
		# torch.save(features, os.path.join(args.feat_dir, 'pt_files', bag_base+'.pt'))


