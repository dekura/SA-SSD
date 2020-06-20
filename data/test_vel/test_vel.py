'''
@Author: Guojin Chen
@Date: 2020-06-18 10:02:08
@LastEditTime: 2020-06-20 15:23:51
@Contact: cgjhaha@qq.com
@Description: check the data structure of velodyne
'''
import numpy as np
np.set_printoptions(suppress=True)
from pathlib import Path

vel_path = Path('/Users/dekura/Downloads/kitti_example/velodyne/003015.bin')
vel_path = Path('/Users/dekura/chen/bei/cuhsd/SA-SSD/data/gds2kitti/results/case1/kitti/velodyne/testcase1.bin')
num_features=4
points = np.fromfile(str(vel_path), dtype=np.float32, count=-1).reshape([-1, num_features])

print(points.shape)
# print(points)
np.savetxt('/Users/dekura/chen/bei/cuhsd/SA-SSD/data/gds2kitti/results/case1/kitti/velodyne/testcase1.txt', points, fmt="%s")
