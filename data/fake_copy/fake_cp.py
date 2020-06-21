'''
@Author: Guojin Chen
@Date: 2020-06-20 17:30:11
@LastEditTime: 2020-06-21 14:20:24
@Contact: cgjhaha@qq.com
@Description: copy one file to many
'''

import os
import shutil
from tqdm import tqdm
from pathlib import Path

dirs = [
    # 'calib',
    # 'image_2',
    'label_2',
    # 'velodyne'
]

in_root_dir = '/Users/dekura/chen/bei/cuhsd/SA-SSD/data/gds2kitti/results/case1/kitti'
out_root_dir = '/Users/dekura/Downloads/case1_fakekitti/'

for dir in dirs:
    in_dir = Path(in_root_dir) / dir
    out_dir = Path(out_root_dir) / dir
    Path.mkdir(out_dir, exist_ok=True)
    # print('in_dir:',in_dir)
    s_g = in_dir.glob('testcase*')
    # for i in s_g:
        # print(i)
    s_g = list(s_g)
    # print('s_g:',s_g)
    s_suffix = s_g[0].suffix
    s = in_dir / s_g[0]
    # t = out_dir /
    for i in tqdm(range(1, 201)):
        i_str = str(i)
        i_str = i_str.zfill(6)
        t_name = i_str+s_suffix
        t = out_dir / t_name
        shutil.copyfile(s, t)
