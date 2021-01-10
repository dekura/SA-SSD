'''
@Author: Guojin Chen
@Date: 2020-06-18 17:09:45
LastEditTime: 2021-01-08 19:44:52
@Contact: cgjhaha@qq.com
@Description: translate the gds to kitti format datasets
'''

import os
import time
import gdspy
import argparse
import numpy as np
from pathlib import Path
from utils.consts import *
from utils.utils import logtxt, predir
from utils.polys2vel import polys2vels, save_vels, hsd_polys2vels, save_labels
from utils.draw_vels import draw_velodyne, draw_velodyne_3d
from utils.gds2poly import _gds2poly, _csv2poly, _get_offset

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', type=str, default='case2', help='experiment name')
parser.add_argument('--in_dir', type=str, required=True, help='the input gds and txt path')
parser.add_argument('--log_dir', type=str, default='./log', help='dir to save logs')
parser.add_argument('--res_dir', type=str, default='./results', help='dir to save fr results')
parser.add_argument('--no_sep_hsd', default=False, action='store_true', help='do not seprate the hsd by layer')
args = parser.parse_args()
args.step = STEP
args.scale_down = SCALE_DOWN
args.hsd_wh = HSD_WH
print(args)
predir(args)


t = time.time()
logtxt('testing time : {} \n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), args)

'''
gds2kitti: transfer the hsd to kitti dataset
@input:
    gds
    hsd_txt
@output:
    kitti
'''

gds_paths = Path(args.in_dir).glob('*.gds')
for gds_path in gds_paths:
    gds_name = gds_path.stem
    csv_path = gds_name + '.csv'
    csv_path = args.in_dir / csv_path
# ================================================
# get gds and hsd poly information
# ================================================
    offsets = _get_offset(str(gds_path), args)
    gds_polys = _gds2poly(str(gds_path), offsets, args)
    hsd_polys = _csv2poly(csv_path, offsets, args)
    # print(hsd_polys)
# ================================================
# visualize the hsd in gds
# ================================================
    # gdspy.current_library = gdspy.GdsLibrary()
    # gdsii = gdspy.GdsLibrary(unit=1e-9)
    # cell = gdsii.new_cell('TOP')
    # for name, polyset in gds_polys.items():
    #     layer_num = LAYERS[name]
    #     polygons = gdspy.PolygonSet(polyset, layer=layer_num)
    #     cell.add(polygons)
    # for id, hsd_set in hsd_polys.items():
    #     if id == 'dup_removed':
    #         layer_num = LAYERS[id]
    #     else:
    #         layer_num = int(id)
    #     polygons = gdspy.PolygonSet(hsd_set, layer=layer_num)
    #     cell.add(polygons)
    # out_name = gds_path.name
    # out_path = args.res_gds_dir / out_name
    # gdsii.write_gds(str(out_path))
# ================================================
# save the polygons to the velodyne
# now we only take the wire the make the velodyne
# now all the polys are rects
# ================================================
    velsets = polys2vels(gds_polys['wire'])
# ================================================
# hsd_polys 2 velodyne
# ================================================
    hsd_velsets, hsd_labels = hsd_polys2vels(hsd_polys['dup_removed'], velsets)
    print('hsd_polys[dup_removed] len: ',len(hsd_polys['dup_removed']))
    print(velsets.shape)
    print(hsd_velsets.shape)
    # print(hsd_labels)
    velsets = np.concatenate((velsets, hsd_velsets))
    save_vels(velsets, gds_name, args)
# ================================================
# hsd_polys to label
# ================================================
    save_labels(hsd_labels, gds_name, args)

# ================================================
# also save the hotspots polygons to the velodyne
# because now we want the hotspots polygons higher than the others
# ================================================


# ================================================
# visualize the velodyne
# ================================================
    # draw_velodyne(velsets)
    # draw_velodyne_3d(velsets)

elapsed = time.time() - t
print('total running time: {}'.format(elapsed))
logtxt('total running time: {}\n\n'.format(elapsed), args)



# TODO:
# now we need to split the large gds to many small gds.
# so we can reduce the total point number


