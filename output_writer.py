#!/usr/bin/env python3

from pathlib import Path
import numpy as np
from PIL import Image

cur_dir = Path('.')

filename = [f.name for f in cur_dir.iterdir() if f.name.startswith('output_array_2024-04-22')][0]
out_dir = 'test'

vid_arr = np.load(filename)
num_frames = vid_arr.shape[0]
nz_count = 0
for i in range(num_frames):
    if np.any(vid_arr[i]):
        im = Image.fromarray(vid_arr[i,:,:,::-1])
        im_name = './'+'out_dir'+'/frame{0:0=2d}.png'.format(i)
        im.save(im_name)
        print('wrote {}'.format(im_name))

