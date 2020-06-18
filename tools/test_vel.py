'''
@Author: Guojin Chen
@Date: 2020-06-18 10:02:08
@LastEditTime: 2020-06-18 10:14:12
@Contact: cgjhaha@qq.com
@Description: check the data structure of velodyne
'''
import numpy as np
np.set_printoptions(suppress=True)
from pathlib import Path

vel_path = Path('/Users/dekura/Downloads/kitti_example/velodyne/003015.bin')
num_features=4
points = np.fromfile(str(vel_path), dtype=np.float32, count=-1).reshape([-1, num_features])

print(points.shape)
print(points)
np.savetxt('./003015.txt', points, fmt="%s")
