import numpy as np 
from absl import app
from absl import flags
import os
import os.path as osp
import pickle 
FLAGS = flags.FLAGS

def get_crop_map(height, width): 
	height_count = np.ceil(float(height-FLAGS.crop_size)/FLAGS.crop_size)
	height_space = np.ceil(float(height-FLAGS.crop_size)/height_count)
	width_count = np.ceil(float(width-FLAGS.crop_size)/FLAGS.crop_size)
	width_space = np.ceil(float(width-FLAGS.crop_size)/width_count)

# return top left corner of random crops (N, 2), each loc is (y, x)
def random_crop(height, width): 
	locs = np.random.randint(low=0, high=[height-FLAGS.crop_size,width-FLAGS.crop_size], size=(FLAGS.crops_per_img, 2)) 
	return locs

# return two lists with file path and location of each sample and each sample to be labeled 
def sample_img(height, width): 
	if FLAGS.import_img_list: 
		with open('img_list.pkl', 'rb') as f: 
		 	img_list = pickle.load(f)
		with open('label_img_list.pkl', 'rb') as f: 
			label_img_list = pickle.load(f)
		return img_list, label_img_list
	img_list = []
	label_img_list = []
	p = 0.01*FLAGS.percent_labels
	for root, dirs, files in os.walk(FLAGS.data_dir, topdown=False):
		for name in files:
			# print(os.path.join(root, name))
			if root[-8:] == 'unsorted': 
				# print(os.path.join(root, name))
				continue 
			im_path = os.path.join(root, name)
			locs = random_crop(height, width)
			mask = np.random.random(FLAGS.crops_per_img)
			img_list.extend(list(map(lambda l: (im_path, l) , list(locs))))
			label_img_list.extend(list(map(lambda l: (im_path, l) , list(locs[mask<p, :]))))

		for name in dirs:
			pass
	# with open('img_list.pkl', 'wb') as f: 
	# 	pickle.dump(img_list, f)
	# with open('label_img_list.pkl', 'wb') as f: 
	# 	pickle.dump(label_img_list, f)
	return img_list, label_img_list


	