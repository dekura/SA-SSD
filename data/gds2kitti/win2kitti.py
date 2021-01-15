'''
@Author: Guojin Chen
@Date: 2020-06-18 17:09:45
LastEditTime: 2021-01-12 16:20:09
@Contact: cgjhaha@qq.com
@Description: translate the gds windows to kitti datasets
'''

import os
import time
import gdspy
import argparse
import numpy as np
from tqdm import tqdm
from pathlib import Path
from utils.consts import *
from utils.utils import logtxt, predir, gen_imgset
from utils.polys2vel_win import polys2vels, save_vels, hsd_polys2vels, save_labels
from utils.draw_vels import draw_velodyne, draw_velodyne_3d
from utils.gds2poly import _gds2poly, _csv2poly, _get_offset, _win2poly

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', type=str, default='case2', help='experiment name')
# parser.add_argument('--in_dir', type=str, required=True, help='the input gds and txt path')
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
TODO:
1. clean the gds
    1. make the origin (0, 0)
2. get the label: if the hsd is zero, pass.
3. get the velodyne

4. train the model
5. produce the case3 and case4
'''

def bbox2poly(bbox):
    x1 = bbox[0][0]
    x2 = bbox[1][0]
    y1 = bbox[0][1]
    y2 = bbox[1][1]
    p0 = [x1, y1]
    p1 = [x1, y2]
    p2 = [x2, y2]
    p3 = [x2, y1]
    poly = [p0, p1, p2, p3]
    print(poly)
    return poly

'''
win2kitti

@input: the cleaned window gds
@output: the kitti dataset
'''
gds_paths = list(Path(args.win_clean_gds_dir).glob('*.gds'))

gen_imgset(args, len(gds_paths))
sum_w, sum_h, total_label = 0, 0, 0
for gds_path in tqdm(gds_paths):
    gds_name = gds_path.stem
# ================================================
# get the hsd label
# ================================================
    offsets, bbox = _get_offset(str(gds_path), args)
    gds_polys = _gds2poly(str(gds_path), offsets, args)
    # print(gds_polys)
# ================================================
# '''
# # hsd_polys 2 velodyne
# # use the gdspy power
# # hsds: [{
# #     'hsd_poly',
# #     'wire_in_hsd': [],
# #     'label_bbox': [ll, ur]
# # }]
# '''

    hsd_polys = gds_polys['dup_removed']
    wire_in_hsd_polys = gds_polys['wire_in_hsd']
    hsds = []
# ================================================
# visualize
# ================================================
    # gdspy.current_library = gdspy.GdsLibrary()
    # gdsii = gdspy.GdsLibrary(unit=1e-9)
    # cell = gdsii.new_cell('TOP')
    # for name, polyset in gds_polys.items():
    #     layer_num = LAYERS[name]
    #     wire_polygons = gdspy.PolygonSet(polyset, layer=layer_num)
    #     cell.add(wire_polygons)
# ================================================
# visualize end
# ================================================

    print(str(gds_path))
    for i, hsd_poly in enumerate(hsd_polys):
        hsd_layer_num = LAYERS['dup_removed'] + i + 1
        wire_in_hsd_layer_num = LAYERS['wire_in_hsd'] + i +1
        wire_in_hsd_bbox_layer_num = LAYERS['wire_in_hsd_bbox'] + i +1
        hsd_poly = gdspy.PolygonSet([hsd_poly], layer=hsd_layer_num)
        wire_in_hsd = gdspy.boolean(wire_in_hsd_polys, hsd_poly, 'and', layer=wire_in_hsd_layer_num)
        if wire_in_hsd is not None:
            # print(wire_in_hsd)
            wire_in_hsd_bbox = wire_in_hsd.get_bounding_box()
            # print(wire_in_hsd_bbox)
        # wire_in_hsd_bbox_poly = gdspy.PolygonSet([bbox2poly(wire_in_hsd_bbox)], layer=wire_in_hsd_bbox_layer_num)
            hsd = {
                'hsd_poly': hsd_poly,
                'wire_in_hsd': wire_in_hsd,
                'label_bbox': wire_in_hsd_bbox
            }
            hsds.append(hsd)
        else:
            # remove the empty hsd polygon
            pass
        # print('in {} hsd_poly, the len wire in hsd is {}'.format(i, len(wire_in_hsd)))
    # out_name = gds_path.name
    # out_path = Path('./results/case2/win_clean_bbox_gds') / out_name
    # gdsii.write_gds(str(out_path))
# ================================================
# generate and save label
# ================================================
    hsd_labels = [x['label_bbox'] for x in hsds]
    w, h, label_count = save_labels(hsd_labels, bbox, gds_name, args)
    sum_w += w
    sum_h += h
    total_label += label_count

# ================================================
# generate and save velsets
# ================================================
    velsets = polys2vels(gds_polys['wire'])
    # print(hsds[0]['wire_in_hsd'].polygons)
    # wire_in_hsds = [x['wire_in_hsd'].polygons for x in hsds]
    wire_in_hsds = []
    for x in hsds:
        wire_in_hsds += x['wire_in_hsd'].polygons
    # print(wire_in_hsds)
    # print(len(wire_in_hsds))
    hsd_velsets = hsd_polys2vels(wire_in_hsds, velsets)
    # print('hsd_polys[dup_removed] len: ',len(hsd_polys['dup_removed']))
    print(velsets.shape)
    print(hsd_velsets.shape)
    # # print(hsd_labels)
    velsets = np.concatenate((velsets, hsd_velsets))
    save_vels(velsets, gds_name, args)
    # break


mean_w = sum_w / total_label
mean_h = sum_h / total_label
logtxt('total data num: {}, total label num {}'.format(len(gds_paths), total_label), args)
logtxt('mean width: {}, mean_height: {}'.format(mean_w, mean_h), args)
elapsed = time.time() - t
logtxt('total running time: {}\n'.format(elapsed), args)