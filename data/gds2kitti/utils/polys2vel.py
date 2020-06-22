'''
@Author: Guojin Chen
@Date: 2020-06-20 10:15:20
@LastEditTime: 2020-06-21 22:34:08
@Contact: cgjhaha@qq.com
@Description: transfer the polygons to the velodyne
'''
import numpy as np
from .consts import STEP
'''
@description: transfer the polygons to the velodyne
@param {type}
    args argparse.args
    polys polysets
@return:
    save the velodyne.

example of velodyne:
31.706 0.053 1.281 0.22
31.952 0.154 1.29 0.19
32.167 0.206 1.297 0.28
32.316 0.309 1.302 0.26
32.745 0.416 1.316 0.21
'''



def _ck_vertical(start, end):
    if start[0] == end[0]:
        return True
    else:
        return False

'''
@input: start, end
@output: a set of points
'''
def se2vels(s, e):
    # print('s:',s)
    # print('e:',e)
    if _ck_vertical(s, e):
        big = max(s[1], e[1])
        small = min(s[1], e[1])
        y = np.arange(small, big, STEP)
        # print('y:', y)
        x = np.linspace(s[0], e[0], y.shape[0])
        # print('x:', x)
        z = np.zeros(y.shape[0])
        z[:] = 0.5
        alpha = np.ones(y.shape[0])
    else:
        big = max(s[0], e[0])
        small = min(s[0], e[0])
        x = np.arange(small, big, STEP)
        # print('x:', x)
        y = np.linspace(s[1], e[1], x.shape[0])
        z = np.zeros(x.shape[0])
        z[:] = 0.5
        alpha = np.ones(x.shape[0])
    vels = np.row_stack((x, y, z, alpha))
    vels = vels.T
    return vels



'''
polys: [
    points: [x, y]
    ...
]
'''
def _polys2vels(polys):
    vels = np.array([])
    # print(polys)
    for i in range(len(polys) - 1):
        # if i>1:
            # break
        start = polys[i]
        end = polys[i+1]
        if vels.shape[0] > 0:
            vels = np.concatenate((vels, se2vels(start, end)), axis=0)
        else:
            vels = se2vels(start, end)
    # add the end to start
    start = polys[len(polys) - 1]
    end = polys[0]
    vels = np.concatenate((vels, se2vels(start, end)), axis=0)
    return vels





'''
polysets: [
    polys:[],
    polys: ...
]
'''
def polys2vels(polysets):
    velsets = np.array([])
    for polys in polysets:
        vels = _polys2vels(polys)
        if velsets.shape[0] > 0:
            velsets = np.concatenate((velsets, vels))
        else:
            velsets = vels
        # break
    return velsets


def save_vels(velsets, gds_name, args):
    vel_name = gds_name + '.bin'
    txt_name = gds_name + '.txt'
    vel_path = args.kitti_vel_dir / vel_name
    txt_path = args.kitti_txt_dir / txt_name
    velsets[:, 0] = velsets[:, 0]/100
    velsets[:, 1] = velsets[:, 1]/100
    velsets = velsets.astype(np.float32)
    velsets.tofile(vel_path)
    np.savetxt(txt_path, velsets, fmt='%.3f')